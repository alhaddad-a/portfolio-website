import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// ─── Security: Helmet with strict CSP ────────────────────────────────────────
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'"],
      imgSrc: ["'self'", 'data:'],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      upgradeInsecureRequests: [],
    },
  },
  crossOriginEmbedderPolicy: true,
  crossOriginOpenerPolicy: true,
  crossOriginResourcePolicy: { policy: 'same-origin' },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
}));

// ─── CORS: Only allow the configured frontend origin ─────────────────────────
const allowedOrigin = process.env.FRONTEND_URL || 'http://localhost:3000';
app.use(cors({
  origin: (origin, callback) => {
    // Allow requests with no origin (e.g., Postman/curl in dev), but lock down in prod
    if (!origin || origin === allowedOrigin) {
      callback(null, true);
    } else {
      callback(new Error('CORS policy: Origin not allowed'));
    }
  },
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type'],
  credentials: false, // No cookies needed; disabling prevents CSRF via cookie
}));

// ─── Body parsing: Strict size limit to prevent large payload attacks ─────────
app.use(express.json({ limit: '10kb' })); // Was '10mb' — far too large for a contact form

// ─── Rate limiting: Strict limits on the contact endpoint ────────────────────
const contactLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5,                    // Max 5 contact submissions per IP per window
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    success: false,
    error: 'Too many requests from this IP, please try again after 15 minutes.'
  }
});

const generalLimiter = rateLimit({
  windowMs: 60 * 1000,  // 1 minute
  max: 60,              // 60 requests/min for other endpoints
  standardHeaders: true,
  legacyHeaders: false,
});

app.use(generalLimiter);

// ─── Email transporter ────────────────────────────────────────────────────────
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS,
  },
});

// Verify email config on startup
transporter.verify((error) => {
  if (error) {
    console.warn('⚠️  Email configuration error:', error.message);
  } else {
    console.log('✅ Email server is ready to send messages');
  }
});

// ─── Helpers ──────────────────────────────────────────────────────────────────

/**
 * Sanitize a string by escaping HTML special characters to prevent XSS
 * in email HTML bodies.
 */
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

// Strict email regex (RFC 5322-inspired, practical subset)
const EMAIL_REGEX = /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/;

// Field length limits
const MAX_NAME_LEN    = 100;
const MAX_EMAIL_LEN   = 254; // RFC 5321 max
const MAX_MESSAGE_LEN = 2000;

// ─── Routes ───────────────────────────────────────────────────────────────────

// Contact form endpoint
app.post('/api/contact', contactLimiter, async (req, res) => {
  try {
    let { name, email, subject, message } = req.body;

    // ── Presence check ──
    if (!name || !email || !subject || !message) {
      return res.status(400).json({
        success: false,
        message: 'All fields are required.',
      });
    }

    // ── Type check ──
    if (typeof name !== 'string' || typeof email !== 'string' || typeof subject !== 'string' || typeof message !== 'string') {
      return res.status(400).json({
        success: false,
        message: 'Invalid field types.',
      });
    }

    // ── Trim whitespace ──
    name    = name.trim();
    email   = email.trim().toLowerCase();
    subject = subject.trim();
    message = message.trim();

    // ── Length limits ──
    if (name.length > MAX_NAME_LEN) {
      return res.status(400).json({ success: false, message: `Name must be under ${MAX_NAME_LEN} characters.` });
    }
    if (email.length > MAX_EMAIL_LEN) {
      return res.status(400).json({ success: false, message: 'Invalid email address.' });
    }
    if (subject.length > 200) {
      return res.status(400).json({ success: false, message: 'Subject must be under 200 characters.' });
    }
    if (message.length > MAX_MESSAGE_LEN) {
      return res.status(400).json({ success: false, message: `Message must be under ${MAX_MESSAGE_LEN} characters.` });
    }
    if (name.length === 0 || subject.length === 0 || message.length === 0) {
      return res.status(400).json({ success: false, message: 'Fields cannot be blank.' });
    }

    // ── Email format validation ──
    if (!EMAIL_REGEX.test(email)) {
      return res.status(400).json({
        success: false,
        message: 'Please provide a valid email address.',
      });
    }

    // ── Sanitize inputs before embedding in HTML ──
    const safeName    = escapeHtml(name);
    const safeEmail   = escapeHtml(email);
    const safeSubject = escapeHtml(subject);
    const safeMessage = escapeHtml(message).replace(/\n/g, '<br>');

    // ── Build email ──
    const mailOptions = {
      from: `"Portfolio Contact Form" <${process.env.EMAIL_USER}>`,
      to: process.env.CONTACT_EMAIL || process.env.EMAIL_USER,
      replyTo: email,  // Safe: email is validated above
      subject: `[Portfolio] ${safeSubject}`,
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <h2 style="color: #3b82f6;">New Contact Form Submission</h2>
          <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <p><strong>Name:</strong> ${safeName}</p>
            <p><strong>Email:</strong> ${safeEmail}</p>
            <p><strong>Subject:</strong> ${safeSubject}</p>
            <p><strong>Message:</strong></p>
            <p style="background-color: white; padding: 15px; border-radius: 4px; border-left: 4px solid #3b82f6;">
              ${safeMessage}
            </p>
          </div>
          <p style="color: #64748b; font-size: 14px;">
            This message was sent from your portfolio contact form.
          </p>
        </div>
      `,
      // Plain-text fallback
      text: `New Contact Form Submission\n\nName: ${name}\nEmail: ${email}\nSubject: ${subject}\n\nMessage:\n${message}`,
    };

    await transporter.sendMail(mailOptions);

    // Avoid logging the full message to protect user privacy
    console.log(`📧 Contact form submission received from ${email}`);

    return res.status(200).json({
      success: true,
      message: 'Thank you for your message! I will get back to you soon.',
    });

  } catch (error) {
    // Never expose internal error details to the client
    console.error('Error sending email:', error.message);
    return res.status(500).json({
      success: false,
      message: 'Sorry, there was an error sending your message. Please try again later.',
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'Portfolio backend is running',
    timestamp: new Date().toISOString(),
  });
});

// 404 handler — catch all unknown routes
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    message: 'Endpoint not found',
  });
});

// Global error handler
app.use((error, req, res, _next) => {
  console.error('Unhandled server error:', error.message);
  res.status(500).json({
    success: false,
    message: 'Internal server error',
  });
});

app.listen(PORT, () => {
  console.log(`🚀 Portfolio backend running on port ${PORT}`);
  console.log(`🩺 Health check: http://localhost:${PORT}/api/health`);
});

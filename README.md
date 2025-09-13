# Modern Portfolio Website

A modern, responsive personal portfolio website built with React, TypeScript, Tailwind CSS, and Node.js. Features smooth animations, contact form functionality, and is optimized for deployment on Cloudflare Pages.

## 🚀 Features

- **Modern Design**: Clean, professional design with smooth animations
- **Responsive Layout**: Fully responsive design that works on all devices
- **Interactive Sections**:
  - Hero section with call-to-action buttons
  - About section with skills and experience
  - Certificates section with clickable links
  - Contact form with backend integration
  - Footer with social links
- **Animations**: Smooth scroll animations and hover effects using Framer Motion
- **Contact Form**: Functional contact form with email integration
- **SEO Optimized**: Meta tags and semantic HTML structure
- **Performance**: Optimized for fast loading and smooth interactions

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **React Intersection Observer** for scroll animations

### Backend
- **Node.js** with Express
- **Nodemailer** for email functionality
- **CORS** for cross-origin requests
- **Helmet** for security headers
- **Rate limiting** for API protection

## 📦 Installation

### Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
touch .env
```

4. Update `.env` with your email credentials:
```env
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
CONTACT_EMAIL=contact@yourdomain.com
PORT=3001
FRONTEND_URL=http://localhost:3000
```

5. Start the backend server:
```bash
npm run dev
```

## 🚀 Deployment

### Cloudflare Pages (Frontend)

1. Connect your GitHub repository to Cloudflare Pages
2. Set build command: `npm run build`
3. Set build output directory: `dist`
4. Deploy!

### Backend Deployment

The backend can be deployed to any Node.js hosting service:

- **Railway**: Easy deployment with automatic environment variable management
- **Heroku**: Traditional PaaS with good Node.js support
- **DigitalOcean App Platform**: Simple deployment with good performance
- **Vercel**: Serverless functions (modify for serverless architecture)

### Environment Variables for Production

Update the frontend's contact form to point to your deployed backend URL:

```typescript
// In src/components/Contact.tsx
const response = await fetch('https://your-backend-domain.com/api/contact', {
  // ... rest of the code
});
```

## 🎨 Customization

### Personal Information

Update the following files with your information:

1. **Personal Details**:
   - `src/components/Hero.tsx` - Name, title, bio
   - `src/components/About.tsx` - Skills, experience, bio
   - `src/components/Contact.tsx` - Contact information
   - `src/components/Footer.tsx` - Social links and contact info

2. **Certificates**:
   - `src/components/Certificates.tsx` - Add your certificates

3. **Styling**:
   - `tailwind.config.js` - Customize colors and theme
   - `src/index.css` - Global styles and custom CSS

### Images

Replace placeholder images with your own:
- Profile images in Hero and About sections
- Certificate images in Certificates section

## 📱 Responsive Design

The website is fully responsive and optimized for:
- Mobile devices (320px and up)
- Tablets (768px and up)
- Desktop (1024px and up)
- Large screens (1280px and up)

## 🔧 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Project Structure

```
portfolio-website/
├── src/
│   ├── components/
│   │   ├── Hero.tsx
│   │   ├── About.tsx
│   │   ├── Certificates.tsx
│   │   ├── Contact.tsx
│   │   ├── Footer.tsx
│   │   └── Navigation.tsx
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── backend/
│   ├── server.js
│   ├── package.json
│   └── README.md
├── public/
├── dist/
└── README.md
```

## 🛡️ Security Features

- Rate limiting on contact form submissions
- Input validation and sanitization
- CORS protection
- Security headers with Helmet
- Email validation

## 📈 Performance

- Optimized images and assets
- Lazy loading for animations
- Efficient bundle splitting
- Minimal dependencies
- Fast loading times

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

If you have any questions or need help with customization, feel free to reach out!

---

Built with ❤️ using React, TypeScript, and Tailwind CSS
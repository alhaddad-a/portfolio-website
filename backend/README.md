# Portfolio Backend

This is the backend API for the portfolio website contact form.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create the environment file:
```bash
touch .env
```

3. Update the `.env` file with your email credentials:
   - `EMAIL_USER`: Your Gmail address
   - `EMAIL_PASS`: Your Gmail app password (not your regular password)
   - `CONTACT_EMAIL`: Email where contact form submissions will be sent
   - `FRONTEND_URL`: URL of your frontend (for CORS)

## Gmail App Password Setup

1. Enable 2-factor authentication on your Gmail account
2. Go to Google Account settings > Security > App passwords
3. Generate an app password for "Mail"
4. Use this app password in the `EMAIL_PASS` field

## Running the Server

Development:
```bash
npm run dev
```

Production:
```bash
npm start
```

## API Endpoints

- `POST /api/contact` - Submit contact form
- `GET /api/health` - Health check

## Environment Variables

- `PORT` - Server port (default: 3001)
- `NODE_ENV` - Environment (development/production)
- `EMAIL_USER` - Gmail username
- `EMAIL_PASS` - Gmail app password
- `CONTACT_EMAIL` - Email to receive contact form submissions
- `FRONTEND_URL` - Frontend URL for CORS

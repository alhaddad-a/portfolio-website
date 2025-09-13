# 🚀 Cloudflare Pages Deployment Guide

## Prerequisites
- Cloudflare account (free)
- Git repository (GitHub, GitLab, or Bitbucket)
- Node.js installed locally

## Method 1: Deploy via Cloudflare Dashboard (Recommended)

### Step 1: Push to Git Repository
1. Initialize git repository (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Create a repository on GitHub/GitLab/Bitbucket
3. Push your code:
   ```bash
   git remote add origin https://github.com/yourusername/portfolio-website.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Connect to Cloudflare Pages
1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to **Pages** in the sidebar
3. Click **"Create a project"**
4. Choose **"Connect to Git"**
5. Select your Git provider (GitHub/GitLab/Bitbucket)
6. Authorize Cloudflare to access your repositories
7. Select your `portfolio-website` repository

### Step 3: Configure Build Settings
- **Project name**: `portfolio-website` (or your preferred name)
- **Production branch**: `main`
- **Framework preset**: `Vite`
- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Root directory**: `/` (leave empty)

### Step 4: Environment Variables (Optional)
If you want to use the backend API in production:
- Go to **Settings** → **Environment variables**
- Add your email configuration:
  - `EMAIL_USER`: your-email@gmail.com
  - `EMAIL_PASS`: your-app-password
  - `CONTACT_EMAIL`: your-email@gmail.com

### Step 5: Deploy
1. Click **"Save and Deploy"**
2. Cloudflare will automatically build and deploy your site
3. You'll get a URL like: `https://portfolio-website.pages.dev`

## Method 2: Deploy via Wrangler CLI

### Step 1: Install Wrangler
```bash
npm install -g wrangler
```

### Step 2: Login to Cloudflare
```bash
wrangler login
```

### Step 3: Deploy
```bash
# Build the project first
npm run build

# Deploy to Cloudflare Pages
wrangler pages deploy dist --project-name=portfolio-website
```

## Method 3: Deploy via GitHub Actions (Advanced)

### Step 1: Create GitHub Actions Workflow
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: portfolio-website
          directory: dist
```

### Step 2: Add Secrets to GitHub
1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:
   - `CLOUDFLARE_API_TOKEN`: Get from Cloudflare Dashboard → My Profile → API Tokens
   - `CLOUDFLARE_ACCOUNT_ID`: Get from Cloudflare Dashboard → Right sidebar

## Post-Deployment Configuration

### Custom Domain (Optional)
1. In Cloudflare Pages dashboard, go to **Custom domains**
2. Click **"Set up a custom domain"**
3. Enter your domain name
4. Follow the DNS configuration instructions

### Performance Optimization
- Cloudflare automatically provides:
  - Global CDN
  - SSL certificates
  - Image optimization
  - Minification
  - Caching

## Troubleshooting

### Build Fails
- Check that all dependencies are in `package.json`
- Ensure build command is correct: `npm run build`
- Check build output directory is `dist`

### Contact Form Not Working
- The contact form will fall back to email client if backend is not available
- For production, consider using a service like Formspree or Netlify Forms

### Images Not Loading
- Ensure images are in the `public` folder
- Check image paths are correct (should start with `/`)

## Your Live URL
Once deployed, your portfolio will be available at:
`https://portfolio-website.pages.dev`

Replace `portfolio-website` with your actual project name.

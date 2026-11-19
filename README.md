# Abdullah Alhaddad — Data Engineer Portfolio

Personal portfolio: <https://alhaddad-a.vercel.app>

A fast, **fully static** site. Every page is plain HTML with all content inside it,
so search engines can read it without running JavaScript.

```
build.py              ← ALL content lives here (about, projects, certificates, contact)
public/               ← the website that gets deployed
  index.html            homepage (generated)
  projects/*/index.html one case-study page per project (generated)
  404.html              real 404 page (generated)
  sitemap.xml           (generated, dates update on every build)
  robots.txt            (generated)
  assets/css/style.css  design system (light + dark)
  assets/js/main.js     theme toggle + mobile menu only
  assets/img/           optimized photo, share image, icons
  .well-known/security.txt  security contact (generated)
vercel.json           ← hosting config: security headers, caching, redirects
source-assets/        original full-size photo (not deployed)
```

## Editing content

1. Open `build.py` and edit the CONTENT section (text, projects, certificates, links).
2. Run `python build.py` (Python 3.8+, no packages needed).
3. Commit and push. Vercel redeploys automatically.

> Don't edit the generated `.html` files by hand. The next build overwrites them.

To add a project, copy one entry in `PROJECTS`. It automatically gets its own page,
a homepage card, a diagram, and a sitemap entry.

Preview locally: `cd public && python -m http.server 8000` → <http://localhost:8000>

## Deploying (Vercel)

`vercel.json` already tells Vercel everything: no install, no build, serve `public/`.
In Vercel, the project only needs to be connected to this GitHub repo:

**Vercel dashboard → your project (alhaddad-a) → Settings → Git → Connect Git Repository →
`alhaddad-a/portfolio-website`.** (Disconnect the old `portfolio-website_temp` first.)
Under *Settings → Build and Deployment*, set Framework Preset to **Other** and turn off any
overrides; `vercel.json` takes care of the rest.

If you move to a custom domain, change `SITE_URL` at the top of `build.py` and rebuild so
canonical URLs, sitemap and structured data point to the new domain.

## Security

The site is static: no server code, no database, no forms, no npm dependencies, and no
secrets. That leaves almost nothing to attack. On top of that:

| Protection | Where |
|---|---|
| **Strict Content-Security-Policy.** Only this site's own scripts, styles, fonts and images can load. No inline scripts or styles, no third parties. It blocks injected code (XSS) even if something slips in. | `vercel.json` |
| **HSTS.** Browsers always use HTTPS. | `vercel.json` |
| **Clickjacking protection.** The site can't be framed (`frame-ancestors 'none'`, `X-Frame-Options: DENY`). | `vercel.json` |
| `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Cross-Origin-Opener-Policy`, and a `Permissions-Policy` that turns off the camera, microphone, location and other sensors. | `vercel.json` |
| **Self-hosted fonts.** No requests to Google Fonts, so visitors' IPs aren't shared with third parties. | `public/assets/fonts/` |
| **External links** use `rel="noopener"`. | `build.py` |
| **Images are stripped of EXIF metadata** (no camera or location data). The full-size original isn't committed. | `public/assets/img/` |
| **`/.well-known/security.txt`** tells researchers how to report a problem. | generated |

After deploying, you can check the grade at <https://securityheaders.com> and
<https://developer.mozilla.org/en-US/observatory>.

Keep it that way:
- Never commit `.env` files, API keys or passwords. The site needs none.
- If you add a third-party script (analytics, for example), add its domain to the
  Content-Security-Policy in `vercel.json`, or the browser will block it.
- Turn on two-factor authentication for GitHub and Vercel. Whoever controls those accounts controls the site.

---

## Getting the site onto Google — checklist

What the code already handles, and what only you can do:

| # | Reason a portfolio doesn't appear | Status |
|---|---|---|
| 1 | Google hasn't indexed it yet | **You:** request indexing in Search Console (step B). It can take a few days to a few weeks. |
| 2 | Not submitted to Search Console | Verification ✅ kept. **You:** submit the new sitemap (step B). |
| 3 | `noindex` tag | ✅ Every page has `robots: index, follow` (only `404.html` is `noindex`, which is correct). |
| 4 | robots.txt blocks Google | ✅ `robots.txt` allows everything and links to the sitemap. |
| 5 | Weak SEO | ✅ A unique `<title>` and meta description per page, one `<h1>`, a semantic heading order, canonical URLs, Open Graph/Twitter cards, and structured data (`Person`, `ProfilePage`, `WebSite`, `BreadcrumbList`, `SoftwareSourceCode`). |
| 6 | Too little content | ✅ About 960 words on the homepage plus three 400–550-word case studies built from the real project repos. |
| 7 | No external links | **You:** steps C–D below. The site links out to LinkedIn and GitHub with `rel="me"`, and structured data lists both under `sameAs`. |
| 8 | Technical problems | ✅ Static HTML (the old site was an empty `<div id="root">` until JavaScript ran), a 27 KB portrait instead of 1.9 MB, a real 404 status instead of a catch-all rewrite, a share image that exists, and a layout that works at 360px wide. |

**A. Verify ownership.** ✅ Already done: your existing Search Console verification tag for
`alhaddad-a.vercel.app` is kept in `GOOGLE_SITE_VERIFICATION` in `build.py`.

**B. Submit the sitemap.** In Search Console → *Sitemaps* → enter `sitemap.xml` → *Submit*.
Then use *URL inspection* on the homepage and each `/projects/...` page → *Request indexing*.

**C. Link to the site from your profiles.** This is the fastest way for Google to discover the site:
- LinkedIn → *Edit intro* → *Website*, and add it to the *Featured* section.
- GitHub → profile *Website* field (github.com/settings/profile), plus a line in your profile README.
- Add a link back to the matching case-study page in each project repo's README.

**D. Optional extras:** Bing Webmaster Tools (it can import from Search Console), and
a custom domain whose name matches yours.

Search for `"Abdullah Alhaddad" data engineer` after indexing. Exact-name searches show up first.

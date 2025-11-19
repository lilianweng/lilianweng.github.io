# How to Reuse This Repository as Your Own Webpage

This repository contains the **built output** of a Hugo static site. Here's how to adapt it for your own use:

## Understanding What You Have

- **Type**: Hugo-generated static site (Hugo v0.139.3)
- **Current state**: Pre-built HTML/CSS/JS files (not source files)
- **Theme**: Appears to be PaperMod or similar
- **Original**: Lilian Weng's personal blog

## Steps to Make It Your Own

### 1. Update Site Metadata

You'll need to do a global find-and-replace for these items:

```bash
# Replace author name
find . -type f -name "*.html" -o -name "*.xml" -exec sed -i 's/Lilian Weng/YOUR NAME/g' {} +

# Replace site URL
find . -type f \( -name "*.html" -o -name "*.xml" -o -name "*.json" \) -exec sed -i 's|https://lilianweng.github.io|https://yourusername.github.io|g' {} +

# Replace site title
find . -type f -name "*.html" -exec sed -i "s/Lil'Log/YOUR SITE TITLE/g" {} +
```

### 2. Update Branding

- Replace favicon files: `favicon_wine.ico`, `favicon_peach.ico`
- Update logo/images in `/assets/` directory
- Modify CSS if needed in `/assets/css/`

### 3. Remove or Replace Content

- Delete existing posts in `/posts/` directory
- Clear `/archives/`, `/categories/`, `/tags/` directories
- Update `index.html` with your own content

### 4. Update GitHub Pages Settings

If using GitHub Pages:

1. Rename repository to `yourusername.github.io`
2. Go to Settings → Pages
3. Set source to deploy from the branch you're using
4. Ensure `CNAME` file (if present) matches your domain

### 5. Test Locally

```bash
# Serve with Python
python3 -m http.server 8000

# Or with Node.js
npx serve .
```

Visit `http://localhost:8000` to preview

## Better Approach: Build From Source

Since this repo only has built files, a better approach is to:

### 1. Install Hugo

```bash
# macOS
brew install hugo

# Linux
sudo apt-get install hugo

# Windows
choco install hugo-extended
```

### 2. Create a New Hugo Site

```bash
hugo new site my-blog
cd my-blog
```

### 3. Install PaperMod Theme

```bash
git init
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

### 4. Configure Your Site

Create `hugo.toml`:

```toml
baseURL = 'https://yourusername.github.io/'
languageCode = 'en-us'
title = 'Your Blog Title'
theme = 'PaperMod'

[params]
  author = "Your Name"
  description = "Your site description"

[params.homeInfoParams]
  Title = "Hi there 👋"
  Content = "Welcome to my blog"

[[menu.main]]
  name = "Archive"
  url = "/archives"
  weight = 5

[[menu.main]]
  name = "Search"
  url = "/search"
  weight = 10

[[menu.main]]
  name = "Tags"
  url = "/tags"
  weight = 10
```

### 5. Create Content

```bash
hugo new posts/my-first-post.md
```

### 6. Build and Deploy

```bash
# Build site
hugo

# The output is in /public directory
# Commit and push the public directory to your gh-pages branch
```

## Deployment Workflow

### Option A: Manual Build

```bash
# Build
hugo

# Copy public/ contents to your gh-pages branch
cp -r public/* /path/to/gh-pages-branch/
```

### Option B: GitHub Actions (Automated)

Create `.github/workflows/hugo.yml` in your **source repository**:

```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.139.3'
          extended: true

      - name: Build
        run: hugo --minify

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```

## Key Files to Update

- `index.html` - Home page
- `sitemap.xml` - Update URLs
- `robots.txt` - Update if needed
- All HTML files in `/posts/` - Your content
- `/assets/` - Your branding assets

## Important Notes

1. **This approach is limited**: You can't easily add new posts without Hugo
2. **Hard to maintain**: Every change requires manual HTML editing
3. **Recommended**: Set up proper Hugo source files instead

## Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [PaperMod Theme](https://github.com/adityatelange/hugo-PaperMod)
- [GitHub Pages Guide](https://docs.github.com/en/pages)

## Questions?

- What's your goal? (Blog, portfolio, documentation site?)
- Do you want to keep the same design/theme?
- Do you need to preserve any existing content?

Let me know and I can help you set up the right approach!

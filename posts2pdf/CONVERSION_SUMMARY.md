# Blog to PDF Conversion Summary

## Overview
Successfully converted all 50 blog posts from HTML to LaTeX and PDF format.

## Conversion Process
1. **HTML Extraction**: Extracted metadata (title, date, reading time, tags) from each HTML blog post
2. **LaTeX Conversion**: Used `pandoc` to convert HTML content to LaTeX format
3. **Template Integration**: Created custom `main.tex` files for each post using the template
4. **PDF Compilation**: Compiled PDFs using `pdflatex`

## Tools Used
- `pandoc` - HTML to LaTeX conversion
- `pdflatex` - LaTeX to PDF compilation
- `beautifulsoup4` - HTML parsing and metadata extraction
- Custom Python script: `convert_with_pandoc.py`

## Results
- **Total blog posts**: 50
- **Successfully converted**: 50 (100%)
- **Failed**: 0

## Previously Converted (7 posts)
These were converted earlier using the OpenAI API-based approach:
1. 2017-10-15-word-embedding
2. 2018-06-24-attention
3. 2021-05-31-contrastive
4. 2021-07-11-diffusion-models
5. 2023-01-27-the-transformer-family-v2
6. 2024-04-12-diffusion-video
7. 2025-05-01-thinking

## Newly Converted (43 posts)
All remaining 43 blog posts were converted using the `pandoc`-based automated script.

## File Structure
Each converted post has:
- `index.html` - Original HTML file (copied for reference)
- `content.tex` - LaTeX content extracted from HTML
- `main.tex` - Complete LaTeX document with metadata and formatting
- `main.pdf` - Final PDF output

## Notes
- PDF sizes range from ~140KB to ~11MB depending on content and images
- All auxiliary LaTeX files (.aux, .log, .out, .toc) have been cleaned up
- The conversion preserves the original blog structure including sections, code blocks, equations, and references

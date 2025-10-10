#!/usr/bin/env python3
"""
Automated script to convert all remaining HTML blog posts to LaTeX and PDF.
This script:
1. Extracts metadata from HTML (title, date, reading time, tags, etc.)
2. Creates directory structure in posts2pdf/
3. Copies HTML file
4. Runs blog_to_latex.py to convert HTML to LaTeX content
5. Creates customized main.tex from template
6. Compiles PDF using pdflatex
"""

import os
import re
import shutil
import subprocess
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm


def extract_metadata(html_path):
    """Extract metadata from HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title_tag = soup.find('h1', class_='post-title')
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"
    
    # Extract date
    date_tag = soup.find('time')
    date_str = date_tag.get_text(strip=True) if date_tag else ""
    
    # Extract reading time
    reading_time = ""
    reading_tag = soup.find('span', class_='post-reading-time')
    if reading_tag:
        reading_time = reading_tag.get_text(strip=True).replace('min read', 'min').strip()
    
    # Extract tags
    tags = []
    tag_elements = soup.find_all('a', rel='tag')
    for tag in tag_elements:
        tags.append(tag.get_text(strip=True))
    
    # Extract URL from post path
    post_name = os.path.basename(os.path.dirname(html_path))
    url = f"https://lilianweng.github.io/posts/{post_name}/"
    
    # Extract year and month from post name
    match = re.match(r'(\d{4})-(\d{2})-\d{2}-', post_name)
    year = match.group(1) if match else ""
    month = match.group(2) if match else ""
    
    month_names = {
        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
    }
    month_name = month_names.get(month, "")
    
    return {
        'title': title,
        'date': date_str,
        'reading_time': reading_time,
        'tags': tags,
        'url': url,
        'year': year,
        'month': month_name,
        'post_name': post_name
    }


def create_main_tex(metadata, output_dir, template_path):
    """Create main.tex file from template with metadata."""
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace placeholders
    tags_str = ', '.join(metadata['tags']) if metadata['tags'] else 'general'
    
    # Update title
    template = template.replace('Example Title', metadata['title'])
    
    # Update URL
    template = template.replace('https://example.com/post', metadata['url'])
    
    # Update date and reading time
    date_line = f"    \\textbf{{Date:}} {metadata['date']} \\quad\n    \\textbf{{Estimated Reading Time:}} {metadata['reading_time']} \\quad"
    template = re.sub(
        r'\\textbf\{Date:\}.*?\\textbf\{Author:\}',
        date_line + '\n    \\textbf{Author:}',
        template
    )
    
    # Update keywords
    template = re.sub(
        r'pdfkeywords=\{.*?\}',
        f'pdfkeywords={{{tags_str}}}',
        template
    )
    
    # Update citation
    title_escaped = metadata['title'].replace('_', '\\_').replace('&', '\\&').replace('#', '\\#')
    template = re.sub(
        r'Weng, Lilian\. ``\\textcolor\{cyan\}\{Title\}\'\'',
        f'Weng, Lilian. ``\\\\textcolor{{cyan}}{{{title_escaped}}}\'\'',
        template
    )
    
    # Update citation date
    if metadata['month'] and metadata['year']:
        template = re.sub(
            r"Lil 'Log \(May 2025\)",
            f"Lil'Log ({metadata['month']} {metadata['year']})",
            template
        )
    
    # Update BibTeX year and month
    template = re.sub(r'year\s*=\s*\{2025\}', f'year    = {{{metadata["year"]}}}', template)
    template = re.sub(r'month\s*=\s*\{May\}', f'month   = {{{metadata["month"]}}}', template)
    
    # Update tags section
    if metadata['tags']:
        tag_links = ' \\quad\n'.join([f'\\href{{{metadata["url"]}}}{{#{tag}}}' for tag in metadata['tags']])
        template = re.sub(
            r'\\href\{https://example\.com/post\}\{tag1\}.*?\\href\{https://example\.com/post\}\{tag2\}',
            tag_links,
            template,
            flags=re.DOTALL
        )
    
    # Write to file
    output_path = os.path.join(output_dir, 'main.tex')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    return output_path


def convert_post(post_name, posts_dir, output_base_dir, template_path, script_path):
    """Convert a single blog post to LaTeX and PDF."""
    html_path = os.path.join(posts_dir, post_name, 'index.html')
    output_dir = os.path.join(output_base_dir, post_name)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy HTML file
    shutil.copy2(html_path, os.path.join(output_dir, 'index.html'))
    
    # Extract metadata
    metadata = extract_metadata(html_path)
    
    # Convert HTML to LaTeX content using blog_to_latex.py
    content_tex_path = os.path.join(output_dir, 'content.tex')
    try:
        subprocess.run(
            ['python3', script_path, html_path, content_tex_path],
            check=True,
            capture_output=True,
            timeout=300
        )
    except subprocess.TimeoutExpired:
        print(f"  Warning: Conversion timed out for {post_name}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"  Warning: Conversion failed for {post_name}: {e.stderr.decode()}")
        return False
    
    # Create main.tex
    main_tex_path = create_main_tex(metadata, output_dir, template_path)
    
    # Read content.tex and insert into main.tex
    if os.path.exists(content_tex_path):
        with open(content_tex_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(main_tex_path, 'r', encoding='utf-8') as f:
            main_tex = f.read()
        
        # Insert content before the Citation section
        main_tex = main_tex.replace('\\section{Citation}', content + '\n\n\\section{Citation}')
        
        with open(main_tex_path, 'w', encoding='utf-8') as f:
            f.write(main_tex)
    
    # Compile PDF
    try:
        # Run pdflatex twice for proper references
        for _ in range(2):
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'main.tex'],
                cwd=output_dir,
                check=True,
                capture_output=True,
                timeout=60
            )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"  Warning: PDF compilation failed for {post_name}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Convert all remaining blog posts to LaTeX and PDF')
    parser.add_argument('--posts-dir', default='posts', help='Directory containing blog posts')
    parser.add_argument('--output-dir', default='posts2pdf', help='Output directory')
    parser.add_argument('--skip-existing', action='store_true', help='Skip posts that already have PDFs')
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent
    template_path = script_dir / 'template' / 'main.tex'
    script_path = script_dir / 'blog_to_latex.py'
    
    # Get list of all posts
    posts_dir = Path(args.posts_dir)
    all_posts = sorted([d.name for d in posts_dir.iterdir() if d.is_dir() and d.name.startswith('20')])
    
    # Filter out already converted posts if requested
    output_dir = Path(args.output_dir)
    if args.skip_existing:
        existing_posts = set([d.name for d in output_dir.iterdir() if d.is_dir() and d.name.startswith('20')])
        posts_to_convert = [p for p in all_posts if p not in existing_posts]
    else:
        posts_to_convert = all_posts
    
    print(f"Found {len(posts_to_convert)} posts to convert")
    
    successful = 0
    failed = []
    
    for post_name in tqdm(posts_to_convert, desc="Converting posts"):
        try:
            if convert_post(post_name, str(posts_dir), str(output_dir), str(template_path), str(script_path)):
                successful += 1
            else:
                failed.append(post_name)
        except Exception as e:
            print(f"  Error converting {post_name}: {e}")
            failed.append(post_name)
    
    print(f"\nConversion complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {len(failed)}")
    if failed:
        print(f"Failed posts: {', '.join(failed)}")


if __name__ == '__main__':
    main()

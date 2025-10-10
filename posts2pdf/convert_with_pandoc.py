#!/usr/bin/env python3
"""
Convert HTML blog posts to LaTeX and PDF using pandoc instead of OpenAI API.
This script:
1. Extracts metadata from HTML
2. Creates directory structure
3. Uses pandoc to convert HTML to LaTeX
4. Customizes main.tex with metadata
5. Compiles PDF
"""

import os
import re
import shutil
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup
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
    
    # Extract post content (main article)
    article = soup.find('article', class_='post-content')
    if article:
        # Remove header/footer elements that aren't part of the main content
        for elem in article.find_all(['header', 'footer']):
            elem.decompose()
        content_html = str(article)
    else:
        content_html = html_content
    
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
        'post_name': post_name,
        'content_html': content_html
    }


def html_to_latex_pandoc(html_content, output_path):
    """Convert HTML to LaTeX using pandoc."""
    # Write HTML to temp file
    temp_html = output_path + '.tmp.html'
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    try:
        # Run pandoc
        result = subprocess.run(
            ['pandoc', '-f', 'html', '-t', 'latex', '--wrap=none', temp_html, '-o', output_path],
            check=True,
            capture_output=True,
            timeout=60
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"Pandoc conversion failed: {e}")
        return False
    finally:
        # Clean up temp file
        if os.path.exists(temp_html):
            os.remove(temp_html)


def create_main_tex(metadata, output_dir, template_path, content_tex_path):
    """Create main.tex file from template with metadata and content."""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Read converted content
        if os.path.exists(content_tex_path):
            with open(content_tex_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "% Content conversion failed"
        
        # Replace placeholders
        tags_str = ', '.join(metadata['tags']) if metadata['tags'] else 'general'
        
        # Use simple title without complex escaping for now
        title_safe = metadata['title']
        
        # Update title (appears in multiple places)
        template = template.replace('Example Title', title_safe)
        
        # Update URL
        template = template.replace('https://example.com/post', metadata['url'])
        
        # Simple string replacements to avoid regex issues
        template = template.replace('June 24, 2018', metadata['date'] if metadata['date'] else 'Unknown')
        template = template.replace('21 min', metadata['reading_time'] if metadata['reading_time'] else 'Unknown')
        template = template.replace('pdfkeywords={example, pdf, latex}', f'pdfkeywords={{{tags_str}}}')
        
        # Update citation date
        if metadata['month'] and metadata['year']:
            template = template.replace("Lil'Log (May 2025)", f"Lil'Log ({metadata['month']} {metadata['year']})")
            template = template.replace("year    = {2025}", f"year    = {{{metadata['year']}}}")
            template = template.replace("month   = {May}", f"month   = {{{metadata['month']}}}")
        
        # Insert content before Citation section
        template = template.replace('\\section{Citation}', content + '\n\n\\section{Citation}')
        
        # Write to file
        output_path = os.path.join(output_dir, 'main.tex')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        return output_path
    except Exception as e:
        print(f"  Error creating main.tex: {e}")
        import traceback
        traceback.print_exc()
        return None


def compile_pdf(tex_dir, max_runs=2):
    """Compile LaTeX to PDF using pdflatex."""
    try:
        # Remove old PDF if it exists
        pdf_path = os.path.join(tex_dir, 'main.pdf')
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        
        # Run pdflatex multiple times for references
        for run in range(max_runs):
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'main.tex'],
                cwd=tex_dir,
                capture_output=True,
                timeout=90
            )
        
        # Check if PDF was created (ignore exit code as pdflatex can return 1 with warnings)
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            return True
        return False
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        # Still check if PDF was created
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            return True
        return False


def clean_aux_files(tex_dir):
    """Remove auxiliary LaTeX files."""
    aux_extensions = ['.aux', '.log', '.out', '.toc', '.tmp.html']
    for ext in aux_extensions:
        for file in Path(tex_dir).glob(f'*{ext}'):
            try:
                file.unlink()
            except:
                pass


def convert_post(post_name, posts_dir, output_base_dir, template_path):
    """Convert a single blog post to LaTeX and PDF using pandoc."""
    html_path = os.path.join(posts_dir, post_name, 'index.html')
    output_dir = os.path.join(output_base_dir, post_name)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy HTML file
    shutil.copy2(html_path, os.path.join(output_dir, 'index.html'))
    
    # Extract metadata and content
    metadata = extract_metadata(html_path)
    
    # Convert HTML to LaTeX using pandoc
    content_tex_path = os.path.join(output_dir, 'content.tex')
    if not html_to_latex_pandoc(metadata['content_html'], content_tex_path):
        print(f"  Failed to convert HTML for {post_name}")
        return False
    
    # Create main.tex with metadata
    main_tex_path = create_main_tex(metadata, output_dir, template_path, content_tex_path)
    
    # Compile PDF
    if compile_pdf(output_dir):
        clean_aux_files(output_dir)
        return True
    else:
        print(f"  PDF compilation failed for {post_name}")
        return False


def main():
    script_dir = Path(__file__).parent
    posts_dir = script_dir.parent / 'posts'
    output_dir = script_dir
    template_path = script_dir / 'template' / 'main.tex'
    
    # Get list of all posts
    all_posts = sorted([d.name for d in posts_dir.iterdir() if d.is_dir() and d.name.startswith('20')])
    
    # Filter out posts that already have PDFs
    posts_with_pdfs = set()
    for d in output_dir.iterdir():
        if d.is_dir() and d.name.startswith('20'):
            pdf_path = d / 'main.pdf'
            if pdf_path.exists():
                posts_with_pdfs.add(d.name)
    
    posts_to_convert = [p for p in all_posts if p not in posts_with_pdfs]
    
    print(f"Found {len(posts_to_convert)} posts to convert")
    
    successful = 0
    failed = []
    
    for post_name in tqdm(posts_to_convert, desc="Converting posts"):
        try:
            if convert_post(post_name, str(posts_dir), str(output_dir), str(template_path)):
                successful += 1
            else:
                failed.append(post_name)
        except Exception as e:
            print(f"  Error converting {post_name}: {e}")
            failed.append(post_name)
    
    print(f"\nConversion complete!")
    print(f"Successful: {successful}/{len(posts_to_convert)}")
    if failed:
        print(f"\nFailed posts ({len(failed)}):")
        for post in failed:
            print(f"  - {post}")


if __name__ == '__main__':
    main()

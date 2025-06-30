import re
import os
import argparse
import time
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv(override=True)


def split_html_by_h1_sections(html_content):
    """
    Splits the HTML content into sections, each starting with <h1> and ending before the next <h1>.
    Returns a list of HTML section strings, each including its <h1> and the content up to the next <h1>.
    """
    # Find all <h1 ...>...</h1> positions
    h1_pattern = re.compile(r"<h1[^>]*>.*?</h1>", re.IGNORECASE | re.DOTALL)
    matches = list(h1_pattern.finditer(html_content))
    sections = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(html_content)
        section = html_content[start:end]
        sections.append(section)
    return sections


def openai_gpt_latex(prompt, max_retries=3, retry_delay=10):
    """
    Calls OpenAI API to convert an HTML section prompt to LaTeX.
    Uses API key and model name from .env.
    Retries on server errors (e.g., 502 Bad Gateway).
    """
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("MODEL")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    client = OpenAI(api_key=api_key)
    system_message = (
        "You are a helpful assistant that converts HTML blog sections (starting with <h1>) to LaTeX. "
        "Convert <h1> to \\section, and convert all content inside the section to appropriate LaTeX. "
        "Return only the LaTeX code, no explanations or formatting."
    )
    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                max_tokens=15000,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(
                f"Error during OpenAI API call (attempt {attempt}/{max_retries}): {e}"
            )
            if attempt == max_retries:
                print("Max retries reached. Skipping this section.")
                return f"% ERROR: Failed to convert section due to API error: {e}"
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)


def main():
    parser = argparse.ArgumentParser(
        description="Split HTML by <h1> sections and convert each section to LaTeX, saving as a .tex file.\n\nExample usage:\n    python blog_to_latex.py path/to/input.html [output.tex]\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input_html", help="Path to the input HTML file")
    parser.add_argument(
        "output_tex",
        nargs="?",
        help="Path to save the output LaTeX file",
    )
    args = parser.parse_args()

    with open(args.input_html, "r", encoding="utf-8") as f:
        html_content = f.read()
    sections = split_html_by_h1_sections(html_content)
    with open(args.output_tex, "w", encoding="utf-8") as f:
        for section in tqdm(
            sections, desc="Converting HTML sections to LaTeX and writing to file"
        ):
            prompt = (
                "Convert the following HTML section (starting with <h1>) to LaTeX. "
                "Convert <h1> to \\section, and convert all content inside the section to appropriate LaTeX. "
                "Return only the LaTeX code, no explanations or formatting.\n\n"
                f"{section}"
            )
            latex = openai_gpt_latex(prompt)
            f.write(latex.strip() + "\n\n")
            f.flush()


if __name__ == "__main__":
    main()

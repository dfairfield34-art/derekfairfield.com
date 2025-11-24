#!/usr/bin/env python3
"""
eBook Generator for Alcohol-Related Liver Damage Guide
Generates EPUB and PDF versions from markdown source
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from ebooklib import epub
from markdown import markdown
from weasyprint import HTML, CSS

# Metadata
BOOK_TITLE = "Alcohol-Related Liver Damage: The Complete Guide"
BOOK_AUTHOR = "Health Guide"
BOOK_LANGUAGE = "en"
BOOK_IDENTIFIER = "liver-health-guide-2024"

def read_manuscript(file_path):
    """Read the markdown manuscript"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def create_epub(markdown_content, output_path):
    """Generate EPUB from markdown content"""
    print("Creating EPUB...")

    # Create EPUB book
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier(BOOK_IDENTIFIER)
    book.set_title(BOOK_TITLE)
    book.set_language(BOOK_LANGUAGE)
    book.add_author(BOOK_AUTHOR)

    # Convert markdown to HTML
    html_content = markdown(markdown_content, extensions=['extra', 'nl2br'])

    # Split into chapters based on "# **CHAPTER" markers
    chapters = []
    chapter_parts = markdown_content.split('\n# **CHAPTER ')

    # Handle introduction (before first chapter)
    if chapter_parts[0].strip():
        intro_html = markdown(chapter_parts[0], extensions=['extra', 'nl2br'])
        intro = epub.EpubHtml(
            title='Introduction',
            file_name='intro.xhtml',
            lang=BOOK_LANGUAGE
        )
        intro.content = f'<html><body>{intro_html}</body></html>'
        book.add_item(intro)
        chapters.append(intro)

    # Process each chapter
    for i, chapter_text in enumerate(chapter_parts[1:], 1):
        chapter_content = '# **CHAPTER ' + chapter_text
        chapter_html = markdown(chapter_content, extensions=['extra', 'nl2br'])

        # Extract chapter title
        first_line = chapter_text.split('\n')[0]
        chapter_title = f"Chapter {i}"

        chapter = epub.EpubHtml(
            title=chapter_title,
            file_name=f'chapter_{i}.xhtml',
            lang=BOOK_LANGUAGE
        )
        chapter.content = f'<html><body>{chapter_html}</body></html>'
        book.add_item(chapter)
        chapters.append(chapter)

    # Add CSS
    style = '''
    @namespace epub "http://www.idpf.org/2007/ops";
    body {
        font-family: Georgia, serif;
        line-height: 1.6;
        margin: 2em;
    }
    h1, h2, h3 {
        color: #2c3e50;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }
    h1 {
        font-size: 2em;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.3em;
    }
    h2 {
        font-size: 1.5em;
        color: #34495e;
    }
    h3 {
        font-size: 1.2em;
        color: #7f8c8d;
    }
    ul, ol {
        margin: 1em 0;
        padding-left: 2em;
    }
    li {
        margin: 0.5em 0;
    }
    p {
        margin: 1em 0;
        text-align: justify;
    }
    strong {
        color: #2c3e50;
    }
    blockquote {
        border-left: 4px solid #3498db;
        padding-left: 1em;
        margin: 1em 0;
        color: #555;
        font-style: italic;
    }
    '''

    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style
    )
    book.add_item(nav_css)

    # Add table of contents
    book.toc = tuple(chapters)

    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define spine
    book.spine = ['nav'] + chapters

    # Write EPUB file
    epub.write_epub(output_path, book)
    print(f"EPUB created: {output_path}")

def create_pdf(markdown_content, output_path):
    """Generate PDF from markdown content"""
    print("Creating PDF...")

    # Convert markdown to HTML
    html_content = markdown(markdown_content, extensions=['extra', 'nl2br'])

    # Create full HTML document with styling
    full_html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{BOOK_TITLE}</title>
        <style>
            @page {{
                size: Letter;
                margin: 1in;
                @bottom-center {{
                    content: counter(page);
                    font-size: 10pt;
                }}
            }}
            body {{
                font-family: Georgia, 'Times New Roman', serif;
                line-height: 1.6;
                color: #333;
                font-size: 11pt;
            }}
            h1 {{
                font-size: 24pt;
                color: #1a1a1a;
                border-bottom: 2px solid #2c3e50;
                padding-bottom: 0.3em;
                margin-top: 2em;
                margin-bottom: 1em;
                page-break-before: always;
            }}
            h1:first-of-type {{
                page-break-before: avoid;
            }}
            h2 {{
                font-size: 18pt;
                color: #2c3e50;
                margin-top: 1.5em;
                margin-bottom: 0.8em;
            }}
            h3 {{
                font-size: 14pt;
                color: #34495e;
                margin-top: 1.2em;
                margin-bottom: 0.6em;
            }}
            p {{
                margin: 0.8em 0;
                text-align: justify;
            }}
            ul, ol {{
                margin: 1em 0;
                padding-left: 2em;
            }}
            li {{
                margin: 0.5em 0;
            }}
            strong {{
                color: #1a1a1a;
                font-weight: bold;
            }}
            em {{
                font-style: italic;
            }}
            blockquote {{
                border-left: 4px solid #3498db;
                padding-left: 1em;
                margin: 1.5em 0;
                color: #555;
                font-style: italic;
            }}
            hr {{
                border: none;
                border-top: 1px solid #ccc;
                margin: 2em 0;
            }}
            .cover {{
                text-align: center;
                margin-top: 40%;
            }}
            .cover h1 {{
                font-size: 32pt;
                border: none;
                page-break-before: avoid;
            }}
            .cover p {{
                font-size: 14pt;
                margin-top: 2em;
            }}
        </style>
    </head>
    <body>
        <div class="cover">
            <h1>{BOOK_TITLE}</h1>
            <p><em>A Comprehensive Guide to Understanding, Treating, and Recovering from Alcohol-Related Liver Disease</em></p>
        </div>
        {html_content}
    </body>
    </html>
    '''

    # Generate PDF
    HTML(string=full_html).write_pdf(output_path)
    print(f"PDF created: {output_path}")

def create_html(markdown_content, output_path):
    """Generate standalone HTML version"""
    print("Creating HTML...")

    html_content = markdown(markdown_content, extensions=['extra', 'nl2br'])

    full_html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{BOOK_TITLE}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: Georgia, 'Times New Roman', serif;
                line-height: 1.8;
                color: #333;
                background: #f5f5f5;
                padding: 20px;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }}
            h1 {{
                font-size: 2.5em;
                color: #1a1a1a;
                border-bottom: 3px solid #2c3e50;
                padding-bottom: 0.3em;
                margin: 1.5em 0 0.8em 0;
            }}
            h2 {{
                font-size: 1.8em;
                color: #2c3e50;
                margin: 1.3em 0 0.7em 0;
            }}
            h3 {{
                font-size: 1.3em;
                color: #34495e;
                margin: 1.1em 0 0.5em 0;
            }}
            p {{
                margin: 1em 0;
                text-align: justify;
            }}
            ul, ol {{
                margin: 1em 0;
                padding-left: 2em;
            }}
            li {{
                margin: 0.5em 0;
            }}
            strong {{
                color: #1a1a1a;
                font-weight: bold;
            }}
            blockquote {{
                border-left: 4px solid #3498db;
                padding-left: 1.5em;
                margin: 1.5em 0;
                color: #555;
                font-style: italic;
                background: #f9f9f9;
                padding: 1em 1em 1em 1.5em;
            }}
            hr {{
                border: none;
                border-top: 2px solid #ddd;
                margin: 2em 0;
            }}
            .header {{
                text-align: center;
                margin-bottom: 3em;
                padding-bottom: 2em;
                border-bottom: 2px solid #ddd;
            }}
            .header h1 {{
                border: none;
                margin: 0;
                font-size: 2.8em;
            }}
            .header p {{
                font-size: 1.1em;
                color: #666;
                font-style: italic;
                margin-top: 1em;
            }}
            @media print {{
                body {{
                    background: white;
                    padding: 0;
                }}
                .container {{
                    box-shadow: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{BOOK_TITLE}</h1>
                <p>A Comprehensive Guide to Understanding, Treating, and Recovering from Alcohol-Related Liver Disease</p>
            </div>
            {html_content}
        </div>
    </body>
    </html>
    '''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"HTML created: {output_path}")

def main():
    """Main execution function"""
    # Set up paths
    script_dir = Path(__file__).parent
    manuscript_path = script_dir / "manuscript.md"
    output_dir = script_dir / "output"

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Read manuscript
    print(f"Reading manuscript from: {manuscript_path}")
    markdown_content = read_manuscript(manuscript_path)

    # Generate all formats
    epub_path = output_dir / "liver-health-guide.epub"
    pdf_path = output_dir / "liver-health-guide.pdf"
    html_path = output_dir / "liver-health-guide.html"

    try:
        create_epub(markdown_content, epub_path)
        create_pdf(markdown_content, pdf_path)
        create_html(markdown_content, html_path)

        print("\n" + "="*60)
        print("eBook generation complete!")
        print("="*60)
        print(f"\nGenerated files:")
        print(f"  EPUB: {epub_path}")
        print(f"  PDF:  {pdf_path}")
        print(f"  HTML: {html_path}")
        print("\nAll formats are ready for distribution.")

    except Exception as e:
        print(f"\nError generating eBook: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

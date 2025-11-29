#!/usr/bin/env python3
"""
Create pocket-sized handbook/pamphlet
Size: 5.5" x 8.5" (digest size - perfect for small handbooks)
"""

from weasyprint import HTML, CSS
from markdown import markdown
from pathlib import Path

def create_handbook_pdf():
    """Generate pocket-sized handbook PDF"""

    # Read the condensed content
    script_dir = Path(__file__).parent
    content_file = script_dir / "handbook-content.md"

    with open(content_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert markdown to HTML
    html_body = markdown(markdown_content, extensions=['extra', 'tables'])

    # Create full HTML with pamphlet-friendly styling
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Alcohol & Liver Damage: Quick Reference Handbook</title>
        <style>
            @page {{
                size: 5.5in 8.5in;
                margin: 0.5in 0.4in;
                @bottom-center {{
                    content: counter(page);
                    font-size: 8pt;
                    color: #666;
                }}
            }}

            body {{
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 9pt;
                line-height: 1.4;
                color: #333;
            }}

            h1 {{
                font-size: 16pt;
                color: #1a5490;
                border-bottom: 2px solid #1a5490;
                padding-bottom: 0.2em;
                margin-top: 0.8em;
                margin-bottom: 0.5em;
                page-break-after: avoid;
            }}

            h1:first-of-type {{
                text-align: center;
                font-size: 18pt;
                margin-top: 1.5em;
                margin-bottom: 0.3em;
                border: none;
            }}

            h2 {{
                font-size: 12pt;
                color: #2c5f8d;
                margin-top: 0.8em;
                margin-bottom: 0.4em;
                page-break-after: avoid;
            }}

            h3 {{
                font-size: 10pt;
                color: #34495e;
                margin-top: 0.6em;
                margin-bottom: 0.3em;
                page-break-after: avoid;
            }}

            p {{
                margin: 0.5em 0;
                text-align: left;
            }}

            ul, ol {{
                margin: 0.4em 0;
                padding-left: 1.2em;
            }}

            li {{
                margin: 0.2em 0;
            }}

            strong {{
                color: #1a1a1a;
                font-weight: bold;
            }}

            em {{
                font-style: italic;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 0.5em 0;
                font-size: 8pt;
            }}

            th {{
                background: #1a5490;
                color: white;
                padding: 0.3em;
                text-align: left;
                font-weight: bold;
            }}

            td {{
                border: 1px solid #ddd;
                padding: 0.3em;
            }}

            tr:nth-child(even) {{
                background: #f9f9f9;
            }}

            hr {{
                border: none;
                border-top: 1px solid #ccc;
                margin: 0.8em 0;
            }}

            .cover {{
                text-align: center;
                page-break-after: always;
                padding-top: 2in;
            }}

            .cover h1 {{
                font-size: 22pt;
                color: #1a5490;
                border: none;
                margin-bottom: 0.5em;
                line-height: 1.2;
            }}

            .cover p {{
                font-size: 10pt;
                color: #666;
                margin: 1em 0;
            }}

            .cover .subtitle {{
                font-size: 12pt;
                font-weight: bold;
                color: #2c5f8d;
                margin-top: 0.5em;
            }}

            blockquote {{
                border-left: 3px solid #1a5490;
                padding-left: 0.5em;
                margin: 0.5em 0;
                color: #555;
                font-style: italic;
                font-size: 8.5pt;
            }}

            .emergency {{
                background: #fff3cd;
                border: 2px solid #ffc107;
                padding: 0.5em;
                margin: 0.5em 0;
                border-radius: 3px;
            }}

            .emergency h2 {{
                color: #856404;
                margin-top: 0;
            }}

            .page-break {{
                page-break-before: always;
            }}
        </style>
    </head>
    <body>
        <div class="cover">
            <h1>Alcohol & Liver Damage</h1>
            <p class="subtitle">Quick Reference Handbook</p>
            <p><em>Essential Facts • Warning Signs • Action Steps</em></p>
            <p style="margin-top: 3em; font-size: 9pt;">
                <strong>Your liver can heal if you act fast.</strong><br>
                This handbook gives you what you need to know.
            </p>
            <p style="position: absolute; bottom: 1in; left: 0; right: 0; font-size: 8pt; color: #999;">
                Health Guide Series © 2024
            </p>
        </div>

        {html_body}
    </body>
    </html>
    '''

    # Generate PDF
    output_file = script_dir / "liver-handbook.pdf"
    HTML(string=html).write_pdf(output_file)

    print(f"✓ Handbook PDF created: {output_file}")
    print(f"\nFormat: 5.5\" × 8.5\" (digest/pamphlet size)")
    print(f"Pages: ~20-25 pages")
    print(f"Perfect for: Pocket reference, printing as booklet")

    return output_file

def create_printable_booklet():
    """Create instructions for printing as booklet"""

    script_dir = Path(__file__).parent
    instructions_file = script_dir / "PRINTING-INSTRUCTIONS.txt"

    instructions = """
PRINTING YOUR HANDBOOK AS A BOOKLET
====================================

Your handbook is sized at 5.5" × 8.5" (digest size) - perfect for a pocket-sized booklet.

OPTION 1: Print at Home (Booklet Style)
----------------------------------------
1. Open liver-handbook.pdf
2. Print settings:
   - Select "Booklet" or "Multiple pages per sheet: 2"
   - Paper size: Letter (8.5" × 11")
   - Duplex: Short edge (flip on short side)
   - This will print 2 pages per sheet
3. Fold printed sheets in half
4. Staple along the spine
5. Trim edges if desired

OPTION 2: Print at Copy Shop
-----------------------------
1. Take liver-handbook.pdf to FedEx, Staples, or local print shop
2. Ask for: "Saddle-stitch booklet, digest size (5.5 × 8.5)"
3. Recommended: 20-50 copies for $20-40
4. Options: Full color or black & white

OPTION 3: Print on Demand (Amazon KDP)
---------------------------------------
1. Upload to KDP as paperback
2. Select trim size: 5.5" × 8.5"
3. Print-on-demand - only pay when someone orders
4. Can sell on Amazon or order author copies

OPTION 4: Simple Single-Sided
------------------------------
1. Print normally on Letter paper (8.5" × 11")
2. Pages will have wide margins
3. Hole-punch and put in binder
4. Easiest option for quick reference

RECOMMENDED: Option 2 (copy shop) for best results
Cost: About $1-2 per booklet for 20+ copies

===================================
FILE: liver-handbook.pdf
SIZE: 5.5" × 8.5" (digest)
PAGES: ~20-25
READY TO PRINT: ✓
===================================
"""

    with open(instructions_file, 'w') as f:
        f.write(instructions)

    print(f"✓ Printing instructions created: {instructions_file}")

def main():
    """Generate handbook and instructions"""
    print("Creating pocket-sized handbook...\n")

    create_handbook_pdf()
    create_printable_booklet()

    print("\n" + "="*60)
    print("HANDBOOK READY!")
    print("="*60)
    print("\nYour pocket-sized handbook is ready:")
    print("  📘 liver-handbook.pdf (5.5\" × 8.5\")")
    print("  📄 PRINTING-INSTRUCTIONS.txt")
    print("\nThis is a small, reference-style guide - about 20-25 pages.")
    print("Perfect for:")
    print("  • Printing as a booklet")
    print("  • Keeping in your pocket/purse")
    print("  • Handing out at support groups")
    print("  • Quick reference")

if __name__ == "__main__":
    main()

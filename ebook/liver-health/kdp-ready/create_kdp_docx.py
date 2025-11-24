#!/usr/bin/env python3
"""
Create KDP-optimized Word document from markdown manuscript
Properly formatted for Kindle Direct Publishing
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import re

def read_manuscript(file_path):
    """Read the markdown manuscript"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def setup_styles(doc):
    """Set up custom styles for the document"""

    # Modify Normal style
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Georgia'
    font.size = Pt(11)

    # Create or modify Heading 1
    if 'Heading 1' not in doc.styles:
        heading1 = doc.styles.add_style('Heading 1', WD_STYLE_TYPE.PARAGRAPH)
    else:
        heading1 = doc.styles['Heading 1']

    heading1.font.name = 'Arial'
    heading1.font.size = Pt(24)
    heading1.font.bold = True
    heading1.font.color.rgb = RGBColor(0, 0, 0)

    # Create or modify Heading 2
    if 'Heading 2' not in doc.styles:
        heading2 = doc.styles.add_style('Heading 2', WD_STYLE_TYPE.PARAGRAPH)
    else:
        heading2 = doc.styles['Heading 2']

    heading2.font.name = 'Arial'
    heading2.font.size = Pt(18)
    heading2.font.bold = True
    heading2.font.color.rgb = RGBColor(44, 62, 80)

    # Create or modify Heading 3
    if 'Heading 3' not in doc.styles:
        heading3 = doc.styles.add_style('Heading 3', WD_STYLE_TYPE.PARAGRAPH)
    else:
        heading3 = doc.styles['Heading 3']

    heading3.font.name = 'Arial'
    heading3.font.size = Pt(14)
    heading3.font.bold = True
    heading3.font.color.rgb = RGBColor(52, 73, 94)

def parse_markdown_to_docx(markdown_content, output_path):
    """Convert markdown to Word document with proper formatting"""

    print("Creating KDP-optimized Word document...")

    doc = Document()
    setup_styles(doc)

    # Set document margins (KDP recommendation: 0.5" minimum)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Add title page
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run('\n\n\n\n')

    title_run = title.add_run('ALCOHOL-RELATED LIVER DAMAGE')
    title_run.font.size = Pt(28)
    title_run.font.bold = True
    title_run.font.name = 'Arial'

    title.add_run('\n\n')

    subtitle_run = title.add_run('The Complete Guide')
    subtitle_run.font.size = Pt(18)
    subtitle_run.font.italic = True
    subtitle_run.font.name = 'Georgia'

    title.add_run('\n\n\n')

    tagline_run = title.add_run('Prevention • Treatment • Recovery')
    tagline_run.font.size = Pt(14)
    tagline_run.font.name = 'Georgia'

    title.add_run('\n\n')

    approach_run = title.add_run('Integrating Western, Eastern & Holistic Medicine')
    approach_run.font.size = Pt(12)
    approach_run.font.italic = True
    approach_run.font.name = 'Georgia'

    # Page break after title
    doc.add_page_break()

    # Add copyright/disclaimer page
    copyright_para = doc.add_paragraph()
    copyright_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    copyright_run = copyright_para.add_run('Copyright © 2024 - All Rights Reserved')
    copyright_run.font.size = Pt(10)

    doc.add_paragraph()

    disclaimer = doc.add_paragraph()
    disclaimer_title = disclaimer.add_run('MEDICAL DISCLAIMER\n\n')
    disclaimer_title.font.bold = True
    disclaimer_title.font.size = Pt(12)

    disclaimer_text = disclaimer.add_run(
        'This book is for informational purposes only and does not constitute medical advice. '
        'The information provided should not be used as a substitute for professional medical care. '
        'Always consult with qualified healthcare professionals for medical diagnosis, treatment, '
        'and advice specific to your individual situation.\n\n'
        'The author and publisher disclaim any liability for any adverse effects arising from the '
        'use or application of the information contained in this book.'
    )
    disclaimer_text.font.size = Pt(10)
    disclaimer_text.font.italic = True

    doc.add_page_break()

    # Process content
    lines = markdown_content.split('\n')
    in_list = False
    skip_title = True  # Skip the first title as we already added it

    for line in lines:
        line = line.strip()

        if not line:
            if not in_list:
                doc.add_paragraph()
            continue

        # Skip the main title on first occurrence
        if skip_title and '# **Alcohol-Related Liver Damage' in line:
            skip_title = False
            continue

        # Skip subtitle and draft note
        if '*Draft Book' in line or '*E‑Book' in line or 'Working Manuscript' in line:
            continue

        # Skip horizontal rules
        if line.strip() == '---':
            doc.add_paragraph()
            continue

        # H1 - Main chapters (# **CHAPTER or # **INTRODUCTION)
        if re.match(r'^#\s+\*\*[A-Z]', line):
            if in_list:
                in_list = False
            doc.add_page_break()
            text = re.sub(r'^#\s+\*\*|\*\*$', '', line).strip()
            para = doc.add_heading(text, level=1)
            continue

        # H2 - Major sections (## **Section)
        if re.match(r'^##\s+\*\*', line):
            if in_list:
                in_list = False
            text = re.sub(r'^##\s+\*\*|\*\*$', '', line).strip()
            doc.add_heading(text, level=2)
            continue

        # H3 - Subsections (### **)
        if re.match(r'^###\s+\*\*', line):
            if in_list:
                in_list = False
            text = re.sub(r'^###\s+\*\*|\*\*$', '', line).strip()
            doc.add_heading(text, level=3)
            continue

        # H4 - Sub-subsections (####)
        if re.match(r'^####\s+\*\*', line):
            if in_list:
                in_list = False
            text = re.sub(r'^####\s+\*\*|\*\*$', '', line).strip()
            para = doc.add_paragraph(text)
            para.style = doc.styles['Heading 3']
            continue

        # Bullet lists
        if re.match(r'^\*\s+', line) or re.match(r'^•\s+', line):
            text = re.sub(r'^\*\s+|^•\s+', '', line)
            # Remove markdown bold
            text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
            para = doc.add_paragraph(text, style='List Bullet')
            in_list = True
            continue

        # Blockquotes
        if line.startswith('>'):
            if in_list:
                in_list = False
            text = line.lstrip('> ').strip()
            text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
            para = doc.add_paragraph(text)
            para.paragraph_format.left_indent = Inches(0.5)
            para.paragraph_format.right_indent = Inches(0.5)
            run = para.runs[0]
            run.font.italic = True
            run.font.size = Pt(11)
            continue

        # Regular paragraphs
        if in_list and not line.startswith('*') and not line.startswith('•'):
            in_list = False

        # Add regular paragraph with bold formatting preserved
        para = doc.add_paragraph()

        # Split by bold markers
        parts = re.split(r'(\*\*[^*]+\*\*)', line)

        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                # Bold text
                text = part.strip('*')
                run = para.add_run(text)
                run.bold = True
            elif part:
                # Regular text
                para.add_run(part)

    # Add back matter page
    doc.add_page_break()

    back_matter = doc.add_heading('About This Book', level=1)

    about_para = doc.add_paragraph(
        'This comprehensive guide provides evidence-based information about alcohol-related '
        'liver damage, covering prevention, diagnosis, treatment, and recovery. The book '
        'integrates Western medical approaches with Eastern medicine practices and holistic '
        'healing tools, offering readers a complete roadmap for liver health and recovery from '
        'alcohol-related liver disease.'
    )

    doc.add_paragraph()

    review_heading = doc.add_heading('Enjoyed This Book?', level=2)

    review_para = doc.add_paragraph(
        'If you found this guide helpful, please consider leaving a review on Amazon. '
        'Your feedback helps others discover this information and supports the creation of '
        'more comprehensive health guides.\n\n'
        'Thank you for reading, and best wishes on your healing journey.'
    )

    # Save document
    doc.save(output_path)
    print(f"✓ Created: {output_path}")

def main():
    """Main execution"""
    import os
    from pathlib import Path

    script_dir = Path(__file__).parent
    manuscript_path = script_dir.parent / "manuscript.md"
    output_path = script_dir / "liver-health-guide-KDP.docx"

    # Read and process
    markdown_content = read_manuscript(manuscript_path)
    parse_markdown_to_docx(markdown_content, output_path)

    print("\n" + "="*60)
    print("KDP Word document created successfully!")
    print("="*60)
    print(f"\nFile: {output_path}")
    print("\nFormat: Microsoft Word (.docx)")
    print("Optimized for: Kindle Direct Publishing")
    print("\nFeatures:")
    print("  ✓ Proper heading hierarchy")
    print("  ✓ Professional formatting")
    print("  ✓ Title page and copyright page")
    print("  ✓ Medical disclaimer")
    print("  ✓ Page breaks between chapters")
    print("  ✓ KDP-compliant margins")
    print("  ✓ Back matter with review request")
    print("\nReady to upload to KDP!")

if __name__ == "__main__":
    main()

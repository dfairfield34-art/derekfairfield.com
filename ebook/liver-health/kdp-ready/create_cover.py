#!/usr/bin/env python3
"""
Create a professional book cover for KDP
Dimensions: 2560 × 1600 pixels (ideal for KDP)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# KDP ideal dimensions (1.6:1 ratio)
WIDTH = 2560
HEIGHT = 1600

def create_cover():
    """Generate professional book cover"""

    # Create base image with gradient background
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    # Create gradient background (dark blue to teal)
    for y in range(HEIGHT):
        # RGB gradient from dark blue-gray to teal
        r = int(20 + (y / HEIGHT) * 30)
        g = int(40 + (y / HEIGHT) * 100)
        b = int(60 + (y / HEIGHT) * 80)
        draw.rectangle([(0, y), (WIDTH, y+1)], fill=(r, g, b))

    # Add subtle texture overlay
    for i in range(0, WIDTH, 100):
        for j in range(0, HEIGHT, 100):
            alpha = 10
            draw.rectangle(
                [(i, j), (i+50, j+50)],
                fill=(255, 255, 255, alpha)
            )

    # Try to use system fonts, fall back to default if not available
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 140)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 80)
        author_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 70)
        tagline_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
    except:
        # Fallback to default font with larger sizes
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        author_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()

    # Add decorative elements
    # Top accent bar
    draw.rectangle([(0, 0), (WIDTH, 40)], fill=(218, 165, 32))

    # Bottom accent bar
    draw.rectangle([(0, HEIGHT-40), (WIDTH, HEIGHT)], fill=(218, 165, 32))

    # Central design element - subtle liver outline
    center_x = WIDTH // 2
    center_y = HEIGHT // 2 - 100

    # Draw medical cross symbol
    cross_color = (100, 200, 180, 128)
    cross_size = 200
    line_width = 30
    draw.rectangle(
        [(center_x - line_width//2, center_y - cross_size),
         (center_x + line_width//2, center_y + cross_size)],
        fill=(100, 200, 180)
    )
    draw.rectangle(
        [(center_x - cross_size, center_y - line_width//2),
         (center_x + cross_size, center_y + line_width//2)],
        fill=(100, 200, 180)
    )

    # Title text
    title_text = "ALCOHOL-RELATED\nLIVER DAMAGE"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]

    # Position title in upper third
    title_y = 200

    # Draw title with shadow for depth
    shadow_offset = 5
    draw.text(
        (center_x - title_width//2 + shadow_offset, title_y + shadow_offset),
        title_text,
        fill=(0, 0, 0, 128),
        font=title_font,
        align='center'
    )
    draw.text(
        (center_x - title_width//2, title_y),
        title_text,
        fill=(255, 255, 255),
        font=title_font,
        align='center'
    )

    # Subtitle
    subtitle_text = "The Complete Guide"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]

    subtitle_y = title_y + title_height + 60
    draw.text(
        (center_x - subtitle_width//2, subtitle_y),
        subtitle_text,
        fill=(218, 165, 32),
        font=subtitle_font
    )

    # Tagline
    tagline_text = "Prevention • Treatment • Recovery"
    tagline_bbox = draw.textbbox((0, 0), tagline_text, font=tagline_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]

    tagline_y = HEIGHT - 300
    draw.text(
        (center_x - tagline_width//2, tagline_y),
        tagline_text,
        fill=(200, 200, 200),
        font=tagline_font
    )

    # Integrative approach badge
    badge_text = "Integrating Western, Eastern & Holistic Medicine"
    badge_bbox = draw.textbbox((0, 0), badge_text, font=tagline_font)
    badge_width = badge_bbox[2] - badge_bbox[0]

    badge_y = tagline_y + 80

    # Draw badge background
    padding = 30
    draw.rectangle(
        [(center_x - badge_width//2 - padding, badge_y - padding//2),
         (center_x + badge_width//2 + padding, badge_y + 60 + padding//2)],
        fill=(40, 80, 100),
        outline=(218, 165, 32),
        width=3
    )

    draw.text(
        (center_x - badge_width//2, badge_y),
        badge_text,
        fill=(255, 255, 255),
        font=tagline_font
    )

    # Author placeholder
    author_text = "Health Guide Series"
    author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
    author_width = author_bbox[2] - author_bbox[0]

    author_y = HEIGHT - 150
    draw.text(
        (center_x - author_width//2, author_y),
        author_text,
        fill=(180, 180, 180),
        font=author_font
    )

    return img

def main():
    """Generate and save cover"""
    print("Generating KDP book cover...")

    cover = create_cover()

    # Save in multiple formats
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # High-quality JPEG for KDP
    jpeg_path = os.path.join(output_dir, "liver-health-cover.jpg")
    cover.save(jpeg_path, "JPEG", quality=95, optimize=True)
    print(f"✓ Created: {jpeg_path}")

    # PNG version
    png_path = os.path.join(output_dir, "liver-health-cover.png")
    cover.save(png_path, "PNG", optimize=True)
    print(f"✓ Created: {png_path}")

    # Create thumbnail for preview
    thumb = cover.copy()
    thumb.thumbnail((800, 500))
    thumb_path = os.path.join(output_dir, "liver-health-cover-thumbnail.jpg")
    thumb.save(thumb_path, "JPEG", quality=85)
    print(f"✓ Created: {thumb_path}")

    print("\n" + "="*60)
    print("Book cover generated successfully!")
    print("="*60)
    print(f"\nDimensions: {WIDTH} × {HEIGHT} pixels")
    print(f"Format: JPEG (KDP-ready)")
    print(f"Aspect ratio: 1.6:1 (KDP ideal)")
    print("\nReady for upload to KDP!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Create application icons for Course Link Getter
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create a simple icon with the app name"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw background circle
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=(0, 122, 255, 255), outline=(0, 102, 204, 255), width=2)
    
    # Add text (simplified for small sizes)
    if size >= 64:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", size//8)
        except:
            font = ImageFont.load_default()
        text = "CLG"
    else:
        font = ImageFont.load_default()
        text = "CLG"
    
    # Get text size and center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Save icon
    img.save(filename)
    print(f"Created {filename} ({size}x{size})")

def main():
    """Create all required icon formats"""
    assets_dir = "course_link_getter/assets"
    
    # Create different sizes for different platforms
    sizes = [16, 32, 48, 64, 128, 256, 512]
    
    for size in sizes:
        create_icon(size, f"{assets_dir}/icon_{size}.png")
    
    # Create ICO file for Windows
    create_icon(256, f"{assets_dir}/icon.ico")
    
    # Create ICNS file for macOS (simplified - in real scenario you'd use iconutil)
    create_icon(512, f"{assets_dir}/icon.icns")
    
    print("✅ All icons created successfully!")

if __name__ == "__main__":
    main()

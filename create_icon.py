from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a 256x256 image with a white background
    size = 256
    image = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a circle
    circle_color = '#1f538d'  # A nice blue color
    draw.ellipse([20, 20, size-20, size-20], fill=circle_color)
    
    # Add text
    try:
        font = ImageFont.truetype("Arial", 100)
    except:
        font = ImageFont.load_default()
    
    text = "$"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    draw.text((x, y), text, fill='white', font=font)
    
    # Save as PNG
    image.save('app_icon.png')
    print("Icon created successfully!")

if __name__ == "__main__":
    create_icon() 
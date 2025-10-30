"""
Generate polished PNG toolbar icons into assets/icons using Pillow.
Run this script (python assets/generate_icons.py) to create icon files.

This is intentionally small and deterministic; it produces 64x64 PNGs for each toolbar icon.
"""
from PIL import Image, ImageDraw
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "icons")
os.makedirs(OUT_DIR, exist_ok=True)

SIZE = 64

def save(img, name):
    path = os.path.join(OUT_DIR, name)
    img.save(path, format="PNG")
    print("Wrote:", path)

# Run icon generation
if __name__ == '__main__':
    # Run (triangle)
    img = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.polygon([(18,12),(18,52),(52,32)], fill=(0,122,204,255))
    save(img, 'run.png')

    # Stop (square)
    img = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([(18,18),(46,46)], fill=(220,53,69,255))
    save(img, 'stop.png')

    # Debug (bug)
    img = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse([(16,20),(48,44)], fill=(255,193,7,255))
    d.ellipse([(24,12),(40,28)], fill=(255,193,7,255))
    d.line([(12,28),(22,36)], fill=(30,30,30,255), width=3)
    d.line([(52,28),(42,36)], fill=(30,30,30,255), width=3)
    save(img, 'debug.png')

    # Load (arrow into box)
    img = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([(10,42),(54,52)], fill=(88,101,242,255))
    d.polygon([(32,12),(18,32),(26,32),(26,44),(38,44),(38,32),(46,32)], fill=(255,255,255,255))
    save(img, 'load.png')

    # Save (floppy-like)
    img = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.rectangle([(12,12),(52,52)], fill=(40,167,69,255))
    d.rectangle([(20,20),(44,36)], fill=(255,255,255,255))
    save(img, 'save.png')

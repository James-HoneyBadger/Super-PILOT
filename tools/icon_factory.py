"""
Icon factory for TempleCode toolbar buttons.
Generates small PNG icons at runtime using Pillow (if available) and returns
Tk PhotoImage objects. If Pillow is not installed, returns an empty dict so
`pilot.py` can gracefully fall back to text-only buttons.
"""

from typing import Dict
from typing import Dict
import os


def create_toolbar_icons(root, size: int = 18) -> Dict[str, object]:
    """Return a dict of PhotoImage objects keyed by name.

    Priority order:
    1. Load static PNGs from assets/icons (if present)
    2. Generate icons in-memory with Pillow (if available)
    3. Return empty dict to fall back to text labels
    """
    icons = {}

    # Try loading static files first (assets/icons)
    try:
        from tkinter import PhotoImage
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons')
        names = {'run': 'run.png', 'stop': 'stop.png', 'debug': 'debug.png', 'load': 'load.png', 'save': 'save.png'}
        for key, fname in names.items():
            path = os.path.join(base_dir, fname)
            if os.path.exists(path):
                try:
                    icons[key] = PhotoImage(file=path, master=root)
                except Exception:
                    # Fall back to generating if PhotoImage fails to load
                    icons = {}
                    break
        if icons:
            return icons
    except Exception:
        icons = {}

    # Fall back to in-memory generation using Pillow
    try:
        from PIL import Image, ImageDraw, ImageTk

        def pil_to_photo(img):
            return ImageTk.PhotoImage(img, master=root)

        # Run
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.polygon([(int(size * 0.28), int(size * 0.18)), (int(size * 0.28), int(size * 0.82)), (int(size * 0.82), int(size * 0.5))], fill=(0, 122, 204, 255))
        icons['run'] = pil_to_photo(img)

        # Stop
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rectangle([(int(size * 0.26), int(size * 0.26)), (int(size * 0.74), int(size * 0.74))], fill=(220, 53, 69, 255))
        icons['stop'] = pil_to_photo(img)

        # Debug
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.ellipse([(int(size * 0.22), int(size * 0.22)), (int(size * 0.78), int(size * 0.62))], fill=(255, 193, 7, 255))
        d.ellipse([(int(size * 0.38), int(size * 0.12)), (int(size * 0.62), int(size * 0.36))], fill=(255, 193, 7, 255))
        d.line([(int(size * 0.28), int(size * 0.42)), (int(size * 0.12), int(size * 0.58))], fill=(30, 30, 30, 255), width=1)
        d.line([(int(size * 0.72), int(size * 0.42)), (int(size * 0.88), int(size * 0.58))], fill=(30, 30, 30, 255), width=1)
        icons['debug'] = pil_to_photo(img)

        # Load
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rectangle([(int(size * 0.16), int(size * 0.64)), (int(size * 0.84), int(size * 0.84))], fill=(88, 101, 242, 255))
        d.polygon([(int(size * 0.5), int(size * 0.18)), (int(size * 0.32), int(size * 0.46)), (int(size * 0.44), int(size * 0.46)), (int(size * 0.44), int(size * 0.66)), (int(size * 0.56), int(size * 0.66)), (int(size * 0.56), int(size * 0.46)), (int(size * 0.68), int(size * 0.46))], fill=(255, 255, 255, 255))
        icons['load'] = pil_to_photo(img)

        # Save
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rectangle([(int(size * 0.18), int(size * 0.18)), (int(size * 0.82), int(size * 0.78))], fill=(40, 167, 69, 255))
        d.rectangle([(int(size * 0.30), int(size * 0.28)), (int(size * 0.70), int(size * 0.46))], fill=(255, 255, 255, 255))
        icons['save'] = pil_to_photo(img)

        return icons
    except Exception:
        return {}

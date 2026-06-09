import os

try:
    from PIL import Image, ImageDraw
except ImportError:
    raise RuntimeError('Pillow is required to generate PNG image assets. Install it with pip install pillow.')

base = os.path.dirname(__file__)
img_dir = os.path.join(base, 'assets', 'images')
os.makedirs(img_dir, exist_ok=True)

size = 32

patterns = {
    'water.png': lambda x, y: (0, 80, 160),
    'federation.png': lambda x, y: (255, 235, 120) if (x == size // 2 or y == size // 2) and 8 < x < 24 and 8 < y < 24 else (60, 180, 255),
    'klingon.png': lambda x, y: (255, 80, 20) if 10 < x < 22 and 10 < y < 22 and abs(x - y) < 5 else (255, 100, 40),
    'hit.png': lambda x, y: (255, 255, 0) if x == y or x == size - y - 1 else (220, 40, 40),
    'miss.png': lambda x, y: (120, 160, 220) if (x - 16) ** 2 + (y - 16) ** 2 < 100 else (80, 110, 170),
}

for name, func in patterns.items():
    path = os.path.join(img_dir, name)
    image = Image.new('RGB', (size, size))
    pixels = image.load()
    for y in range(size):
        for x in range(size):
            pixels[x, y] = func(x, y)
    image.save(path)

print('Assets created in', img_dir)

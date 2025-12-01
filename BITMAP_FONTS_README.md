# Bitmap Fonts Guide

This guide explains how to use and create custom bitmap fonts for the RP2350 display.

## What Are Bitmap Fonts?

Bitmap fonts are pre-rendered character images stored as binary data. Each pixel is either on (1) or off (0). They provide:
- **Crisp, clean appearance** - No scaling artifacts
- **Custom designs** - Create fonts that match your aesthetic
- **Fast rendering** - Pre-computed pixels, just copy to display
- **Memory efficient** - Only store characters you need

## Using the Included Bitmap Font

The `bitmap_fonts.py` module includes a 16x24 pixel font for digits (0-9) and colon (:).

### Example Usage:

```python
import bitmap_fonts

# Draw a single character at position (x, y)
bitmap_fonts.draw_char(lcd, '5', 50, 100, lcd.white)

# Draw text (auto-spacing)
bitmap_fonts.draw_text(lcd, "12:45", 50, 100, lcd.white, spacing=2)

# Center text on screen
text = "09:30"
text_width = bitmap_fonts.get_text_width(text, spacing=4)
x = (240 - text_width) // 2  # Center on 240px wide screen
bitmap_fonts.draw_text(lcd, text, x, 100, lcd.white, spacing=4)
```

## Creating Your Own Bitmap Fonts

### Method 1: Manual Binary Creation (What we did)

Each character is defined as a list of rows, where each row is a 16-bit binary number:

```python
'A': [
    0b0000001111000000,  # Row 0
    0b0000011111100000,  # Row 1
    0b0000111001110000,  # Row 2
    # ... 21 more rows for 24 total
]
```

**Steps:**
1. Draw your character on graph paper (16 wide x 24 tall)
2. Convert each row to binary (1 = pixel on, 0 = pixel off)
3. Add to the LARGE_DIGITS dictionary

### Method 2: Use an Image Editor (Easier!)

You can create bitmap fonts from images:

**Steps:**

1. **Create the character image:**
   - Use any image editor (GIMP, Photoshop, Paint.NET)
   - Create a 16x24 pixel image
   - Use 2 colors: black (background) and white (character)
   - Save as PNG

2. **Convert to binary format:**

```python
from PIL import Image

def image_to_bitmap(image_path):
    """Convert a 16x24 image to bitmap format"""
    img = Image.open(image_path).convert('1')  # Convert to 1-bit
    width, height = img.size

    if width != 16 or height != 24:
        raise ValueError("Image must be 16x24 pixels")

    bitmap = []
    for y in range(height):
        row_value = 0
        for x in range(width):
            pixel = img.getpixel((x, y))
            if pixel == 0:  # Black = pixel on
                row_value |= (1 << (15 - x))
        bitmap.append(row_value)

    return bitmap

# Usage:
char_a_bitmap = image_to_bitmap('letter_a_16x24.png')
print('A': [')
for row in char_a_bitmap:
    print(f'    0b{row:016b},')
print('],')
```

3. **Add to bitmap_fonts.py**

### Method 3: Online Bitmap Font Generators

Use online tools to create bitmap fonts:
- [The Dot Factory](http://www.eran.io/the-dot-factory-an-lcd-font-and-image-generator/)
- [Pixel Font Converter](https://rop.nl/truetype2gfx/)

Configure for:
- Width: 16 pixels
- Height: 24 pixels
- Format: Binary array
- Bit order: MSB first

## Font Sizes

Current font is 16x24 pixels (moderate size). You can create different sizes:

- **Small**: 8x12 pixels (fits more text)
- **Medium**: 16x24 pixels (current, good balance)
- **Large**: 24x32 pixels (very prominent)
- **Huge**: 32x48 pixels (fills screen, for temperature displays)

## Adding More Characters

To add letters, symbols, or other characters:

1. Design the character (16x24 pixels)
2. Convert to binary format
3. Add to the `LARGE_DIGITS` dictionary (or create a new dictionary like `LARGE_LETTERS`)

Example adding 'A':
```python
LARGE_LETTERS = {
    'A': [
        0b0000001111000000,
        0b0000011111100000,
        0b0000111001110000,
        0b0001110000111000,
        0b0011100000011100,
        # ... rest of rows
    ],
}
```

## Performance Considerations

- **Memory**: Each character uses 24 rows × 2 bytes = 48 bytes
- **Speed**: Bitmap rendering is fast (no calculations needed)
- **Storage**: Only store characters you actually use

For a full alphabet (A-Z, a-z, 0-9, symbols ~100 chars):
- Memory usage: ~4,800 bytes
- Perfectly acceptable for RP2350 (264KB RAM)

## Tips for Good Fonts

1. **Keep it simple** - Complex details may not show well at small sizes
2. **Test on device** - What looks good on computer may differ on LCD
3. **Consistent style** - Match the thickness and spacing across all characters
4. **Leave padding** - Don't use all 16 pixels width, leave 1-2px margins
5. **Anti-aliasing alternative** - For smoother fonts, use gray pixels (requires color depth changes)

## Example: Weather Icon Fonts

You can create icon fonts for weather conditions:

```python
WEATHER_ICONS = {
    'sunny': [
        # 32x32 sun icon
    ],
    'cloudy': [
        # 32x32 cloud icon
    ],
    'rainy': [
        # 32x32 rain icon
    ],
}
```

## Further Reading

- [MicroPython framebuf documentation](https://docs.micropython.org/en/latest/library/framebuf.html)
- [Bitmap Font Basics](https://en.wikipedia.org/wiki/Computer_font#Bitmap_fonts)
- Font editors: FontForge, Bits'N'Picas (free tools for creating bitmap fonts)

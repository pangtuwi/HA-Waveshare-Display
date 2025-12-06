#!/usr/bin/env python3
"""
Image to RGB565 Converter for Waveshare RP2350 Display

Converts JPG/PNG images to RGB565 byte arrays with BRG color correction
for the Waveshare RP2350-Touch-LCD-1.28 display (240x240 pixels).

Usage:
    python convert_image.py image.jpg variable_name > output.py

The output can be copied into image_data.py on the RP2350.

Requirements:
    pip install Pillow
"""

from PIL import Image
import sys
import os


def apply_gamma_correction(value, gamma=2.2):
    """
    Apply gamma correction to a color value.

    Converts from sRGB (gamma ~2.2) to linear RGB.
    This brightens mid-tones which tend to appear too dark on the display.

    Args:
        value: Color value 0-255
        gamma: Gamma value (default 2.2 for sRGB)

    Returns:
        Gamma-corrected value 0-255
    """
    # Normalize to 0-1
    normalized = value / 255.0
    # Apply gamma correction
    corrected = pow(normalized, 1.0 / gamma)
    # Convert back to 0-255
    return int(corrected * 255.0)


def convert_image_to_rgb565_brg(image_path, variable_name, gamma=2.2):
    """
    Convert image to RGB565 byte array with BRG color correction.

    Args:
        image_path: Path to JPG/PNG file
        variable_name: Variable name for the Python output
        gamma: Gamma correction value (default 2.2 for sRGB). Set to 1.0 to disable.

    Returns:
        Tuple of (byte_array, image_info_dict)
    """
    # Load image
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error loading image: {e}", file=sys.stderr)
        sys.exit(1)

    # Get original size
    orig_width, orig_height = img.size

    # Resize to 240x240 if needed
    if orig_width != 240 or orig_height != 240:
        print(f"# Resizing from {orig_width}x{orig_height} to 240x240", file=sys.stderr)
        img = img.resize((240, 240), Image.Resampling.LANCZOS)

    # Convert to RGB (handles RGBA, grayscale, etc.)
    img = img.convert('RGB')

    # Convert to RGB565 with BRG correction
    byte_array = bytearray()

    for y in range(240):
        for x in range(240):
            r, g, b = img.getpixel((x, y))

            # Apply gamma correction to brighten mid-tones
            if gamma != 1.0:
                r = apply_gamma_correction(r, gamma)
                g = apply_gamma_correction(g, gamma)
                b = apply_gamma_correction(b, gamma)

            # Convert RGB888 to RGB565 with BRG format for this display
            # The display uses non-standard color layout:
            # Bits 15-11: Blue (5 bits)
            # Bits 10-5: Red (6 bits)
            # Bits 4-0: Green (5 bits)
            rgb565 = ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

            # Store as little-endian bytes
            byte_array.append(rgb565 & 0xFF)
            byte_array.append((rgb565 >> 8) & 0xFF)

    info = {
        'original_size': (orig_width, orig_height),
        'output_size': (240, 240),
        'byte_count': len(byte_array),
        'variable_name': variable_name,
        'gamma': gamma
    }

    return byte_array, info


def generate_python_code(byte_array, variable_name, image_path, info):
    """
    Generate Python code with the byte array using bytes literal format (memory efficient).

    Args:
        byte_array: bytearray with image data
        variable_name: Name for the Python variable
        image_path: Original image path
        info: Dictionary with image info
    """
    print(f"# Image: {os.path.basename(image_path)}")
    print(f"# Original size: {info['original_size'][0]}x{info['original_size'][1]}")
    print(f"# Output size: 240x240 pixels")
    print(f"# Format: RGB565 (BRG color corrected)")
    gamma_note = f" with gamma correction {info['gamma']}" if info['gamma'] != 1.0 else ""
    print(f"# Size: {len(byte_array):,} bytes{gamma_note}")
    print()

    # Split into small chunks stored as separate variables
    # Then concatenate at runtime to avoid parser issues
    # Use 2KB chunks to keep line length reasonable
    chunk_size = 2048
    num_chunks = (len(byte_array) + chunk_size - 1) // chunk_size

    # Generate chunk variables
    for chunk_num in range(num_chunks):
        start = chunk_num * chunk_size
        end = min(start + chunk_size, len(byte_array))
        chunk = byte_array[start:end]
        hex_str = ''.join(f'\\x{b:02x}' for b in chunk)
        print(f"_{variable_name}_p{chunk_num} = b'{hex_str}'")

    print()

    # Store as tuple of chunks - don't concatenate at import time!
    # The display function will handle chunks to save memory
    chunk_vars = ', '.join(f'_{variable_name}_p{i}' for i in range(num_chunks))
    print(f"{variable_name} = ({chunk_vars})")
    print()


def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_image.py <image_file> <variable_name>", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print("  python convert_image.py background.jpg bg_image > temp.py", file=sys.stderr)
        print("\nThen copy the output from temp.py into image_data.py", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]
    variable_name = sys.argv[2]

    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    # Convert image
    print(f"# Converting {image_path}...", file=sys.stderr)
    byte_array, info = convert_image_to_rgb565_brg(image_path, variable_name)
    print(f"# Generated {len(byte_array):,} bytes", file=sys.stderr)

    # Generate Python code
    generate_python_code(byte_array, variable_name, image_path, info)

    print(f"# Conversion complete!", file=sys.stderr)
    print(f"# Copy the output above into image_data.py", file=sys.stderr)


if __name__ == "__main__":
    main()

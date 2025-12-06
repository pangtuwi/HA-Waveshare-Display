# Color Calibration Test for Waveshare RP2350 Display
# Tests RGB565 color accuracy with BRG format
#
# EXPECTED RESULTS:
# ✅ Test 1 (Primary Colors): Perfect
# ⚠️ Test 2 (Pink Shades): Some pinks may appear incorrect
# ✅ Test 3 (Red Gradient): Should show red (with gamma correction)
# ✅ Test 4 (Green Gradient): Should show green (with gamma correction)
# ✅ Test 5 (Blue Gradient): Should show blue (with gamma correction)
# ✗ Test 6 (Grayscale): WILL SHOW GREEN/PURPLE ARTIFACTS - hardware limitation
# ⚠️ Test 7+ (Bit Depth, etc.): Some banding and color variations expected
#
# HARDWARE LIMITATION: Grayscale (equal R=G=B) is fundamentally broken due to
# mismatched per-channel gamma curves in the display hardware. This cannot be
# fixed in software. See COLOR_NOTES.md for details.

from LCD_1inch28 import LCD_1inch28
import time

def apply_gamma_correction(value, gamma=2.2):
    """Apply gamma correction (same as image converter)."""
    normalized = value / 255.0
    corrected = pow(normalized, 1.0 / gamma)
    return int(corrected * 255.0)

def rgb_to_brg565(r, g, b):
    """
    Convert RGB888 to RGB565 with BRG format and gamma correction.

    Uses gamma correction to match how images display correctly.

    Args:
        r, g, b: RGB values (0-255)

    Returns:
        RGB565 value in BRG format with gamma correction
    """
    # Apply gamma correction (this makes images display correctly)
    r = apply_gamma_correction(r, 2.2)
    g = apply_gamma_correction(g, 2.2)
    b = apply_gamma_correction(b, 2.2)

    # BRG format: Blue(15-11), Red(10-5), Green(4-0)
    return ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)


def draw_color_block(lcd, x, y, width, height, r, g, b):
    """Draw a solid color block."""
    color = rgb_to_brg565(r, g, b)
    lcd.fill_rect(x, y, width, height, color)


def test_primary_colors(lcd):
    """Test 1: Pure primary colors."""
    print("\nTest 1: Primary Colors")
    lcd.fill(lcd.black)

    # Pure Red
    draw_color_block(lcd, 0, 0, 80, 60, 255, 0, 0)
    lcd.text("RED", 20, 25, lcd.white)

    # Pure Green
    draw_color_block(lcd, 80, 0, 80, 60, 0, 255, 0)
    lcd.text("GREEN", 90, 25, lcd.white)

    # Pure Blue
    draw_color_block(lcd, 160, 0, 80, 60, 0, 0, 255)
    lcd.text("BLUE", 175, 25, lcd.white)

    # Cyan
    draw_color_block(lcd, 0, 60, 80, 60, 0, 255, 255)
    lcd.text("CYAN", 20, 85, lcd.white)

    # Magenta
    draw_color_block(lcd, 80, 60, 80, 60, 255, 0, 255)
    lcd.text("MAGENTA", 85, 85, lcd.white)

    # Yellow
    draw_color_block(lcd, 160, 60, 80, 60, 255, 255, 0)
    lcd.text("YELLOW", 170, 85, lcd.white)

    # White
    draw_color_block(lcd, 0, 120, 120, 60, 255, 255, 255)
    lcd.text("WHITE", 35, 145, lcd.black)

    # Black
    draw_color_block(lcd, 120, 120, 120, 60, 0, 0, 0)
    lcd.text("BLACK", 155, 145, lcd.white)

    lcd.text("Primary Colors Test", 55, 190, lcd.white)
    lcd.show()
    time.sleep(5)


def test_pink_shades(lcd):
    """Test 2: Different shades of pink to diagnose darkness issue."""
    print("\nTest 2: Pink Shades")
    lcd.fill(lcd.black)

    pink_shades = [
        (255, 192, 203, "Pink Standard"),      # Standard pink
        (255, 182, 193, "Light Pink"),         # Light pink
        (255, 105, 180, "Hot Pink"),           # Hot pink
        (219, 112, 147, "Pale Violet"),        # Pale violet red
        (255, 160, 200, "Custom Pink 1"),      # Custom
        (230, 140, 180, "Custom Pink 2"),      # Darker custom
    ]

    y = 0
    for r, g, b, label in pink_shades:
        draw_color_block(lcd, 0, y, 120, 40, r, g, b)
        lcd.text(label, 125, y + 15, lcd.white)
        # Show RGB values
        lcd.text(f"{r},{g},{b}", 125, y + 25, lcd.white)
        y += 40

    lcd.show()
    time.sleep(7)


def test_red_gradient(lcd):
    """Test 3: Red channel gradient."""
    print("\nTest 3: Red Gradient")
    lcd.fill(lcd.black)
    lcd.text("Red Channel Gradient", 50, 10, lcd.white)

    # 8 steps from 0 to 255
    for i in range(8):
        red_val = i * 32  # 0, 32, 64, 96, 128, 160, 192, 224
        draw_color_block(lcd, i * 30, 30, 30, 60, red_val, 0, 0)
        lcd.text(str(red_val), i * 30 + 5, 95, lcd.white)

    lcd.show()
    time.sleep(5)


def test_green_gradient(lcd):
    """Test 4: Green channel gradient."""
    print("\nTest 4: Green Gradient")
    lcd.fill(lcd.black)
    lcd.text("Green Channel Gradient", 40, 10, lcd.white)

    for i in range(8):
        green_val = i * 32
        draw_color_block(lcd, i * 30, 30, 30, 60, 0, green_val, 0)
        lcd.text(str(green_val), i * 30 + 5, 95, lcd.white)

    lcd.show()
    time.sleep(5)


def test_blue_gradient(lcd):
    """Test 5: Blue channel gradient."""
    print("\nTest 5: Blue Gradient")
    lcd.fill(lcd.black)
    lcd.text("Blue Channel Gradient", 45, 10, lcd.white)

    for i in range(8):
        blue_val = i * 32
        draw_color_block(lcd, i * 30, 30, 30, 60, 0, 0, blue_val)
        lcd.text(str(blue_val), i * 30 + 5, 95, lcd.white)

    lcd.show()
    time.sleep(5)


def test_grayscale(lcd):
    """Test 6: Grayscale gradient."""
    print("\nTest 6: Grayscale")
    lcd.fill(lcd.black)
    lcd.text("Grayscale Gradient", 60, 10, lcd.white)

    for i in range(8):
        gray_val = i * 32
        draw_color_block(lcd, i * 30, 30, 30, 60, gray_val, gray_val, gray_val)
        lcd.text(str(gray_val), i * 30 + 5, 95, lcd.white)

    lcd.show()
    time.sleep(5)


def test_rgb565_limits(lcd):
    """Test 7: RGB565 bit depth limits."""
    print("\nTest 7: RGB565 Bit Depth")
    lcd.fill(lcd.black)
    lcd.text("RGB565 Precision Test", 50, 5, lcd.white)

    # Red: 5 bits (32 levels)
    lcd.text("Red: 5 bits (32 levels)", 10, 25, lcd.white)
    for i in range(16):
        # Map 0-31 range
        red_val = int(i * (255 / 15))
        draw_color_block(lcd, i * 15, 40, 15, 30, red_val, 0, 0)

    # Green: 6 bits (64 levels)
    lcd.text("Green: 6 bits (64 levels)", 10, 80, lcd.white)
    for i in range(16):
        green_val = int(i * (255 / 15))
        draw_color_block(lcd, i * 15, 95, 15, 30, 0, green_val, 0)

    # Blue: 5 bits (32 levels)
    lcd.text("Blue: 5 bits (32 levels)", 10, 135, lcd.white)
    for i in range(16):
        blue_val = int(i * (255 / 15))
        draw_color_block(lcd, i * 15, 150, 15, 30, 0, 0, blue_val)

    lcd.text("Note: Visible banding", 50, 190, lcd.white)
    lcd.text("is normal for RGB565", 50, 205, lcd.white)

    lcd.show()
    time.sleep(7)


def test_color_accuracy(lcd):
    """Test 8: Known reference colors."""
    print("\nTest 8: Reference Colors")
    lcd.fill(lcd.black)
    lcd.text("Reference Colors", 65, 5, lcd.white)

    # Standard web colors
    colors = [
        (255, 0, 0, "Red"),
        (0, 255, 0, "Lime"),
        (0, 0, 255, "Blue"),
        (255, 255, 0, "Yellow"),
        (0, 255, 255, "Cyan"),
        (255, 0, 255, "Magenta"),
        (192, 192, 192, "Silver"),
        (128, 128, 128, "Gray"),
        (128, 0, 0, "Maroon"),
        (0, 128, 0, "Green"),
        (0, 0, 128, "Navy"),
        (255, 165, 0, "Orange"),
    ]

    x, y = 0, 25
    for r, g, b, name in colors:
        draw_color_block(lcd, x, y, 60, 30, r, g, b)
        lcd.text(name, x + 5, y + 10, lcd.white if (r + g + b) < 384 else lcd.black)
        x += 60
        if x >= 240:
            x = 0
            y += 30

    lcd.show()
    time.sleep(7)


def test_brightness_levels(lcd):
    """Test 9: Brightness perception test."""
    print("\nTest 9: Brightness Levels")
    lcd.fill(lcd.black)
    lcd.text("Brightness Test", 70, 5, lcd.white)

    # Show same color at different brightness levels
    brightness_levels = [
        (255, 192, 203, "100%"),  # Your pink at 100%
        (204, 154, 162, "80%"),
        (153, 115, 122, "60%"),
        (102, 77, 81, "40%"),
        (51, 38, 41, "20%"),
    ]

    y = 25
    for r, g, b, label in brightness_levels:
        draw_color_block(lcd, 0, y, 160, 40, r, g, b)
        lcd.text(f"Pink {label}", 165, y + 10, lcd.white)
        lcd.text(f"RGB:{r},{g},{b}", 165, y + 20, lcd.white)
        y += 40

    lcd.show()
    time.sleep(15)


def main():
    """Run all color calibration tests."""
    print("=== Color Calibration Test Updated VERSION===")
    print("Testing RGB565 with BRG format")

    # Initialize display
    lcd = LCD_1inch28()
    lcd.set_bl_pwm(65535)  # Maximum brightness

    try:
        test_primary_colors(lcd)
        test_pink_shades(lcd)
        test_red_gradient(lcd)
        test_green_gradient(lcd)
        test_blue_gradient(lcd)
        test_grayscale(lcd)
        test_rgb565_limits(lcd)
        test_color_accuracy(lcd)
        test_brightness_levels(lcd)

        # Summary
        lcd.fill(lcd.black)
        lcd.text("Calibration Complete", 50, 100, lcd.white)
        lcd.text("Press Ctrl+C to exit", 45, 120, lcd.white)
        lcd.show()

        print("\n=== All Tests Complete ===")
        print("Observations to note:")
        print("- Color accuracy vs expected")
        print("- Banding in gradients")
        print("- Brightness levels")
        print("- Pink darkness issue")

        # Keep display on
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nCalibration test ended")


if __name__ == "__main__":
    main()

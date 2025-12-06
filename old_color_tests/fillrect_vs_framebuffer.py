# Compare fill_rect vs direct framebuffer write for intermediate values

from LCD_1inch28 import LCD_1inch28
import time

def rgb_to_brg565(r, g, b):
    """BRG565 format - same as working images."""
    return ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

print("=== fill_rect vs Framebuffer Test ===")

# Test red=64 (intermediate value)
test_values = [
    (64, 0, 0, "Red=64"),
    (0, 64, 0, "Green=64"),
    (0, 0, 64, "Blue=64"),
    (128, 128, 128, "Gray=128"),
]

for r, g, b, label in test_values:
    color = rgb_to_brg565(r, g, b)
    print(f"\n{label}: RGB({r}, {g}, {b}) -> 0x{color:04X}")

    lcd.fill(lcd.black)
    lcd.text(label, 80, 10, lcd.white)

    # LEFT: Using fill_rect
    lcd.fill_rect(0, 30, 120, 90, color)
    lcd.text("fill_rect", 25, 70, lcd.white)

    # RIGHT: Direct framebuffer write (like images)
    for y in range(30, 120):
        for x in range(120, 240):
            pixel_index = (y * 240 + x) * 2
            # Little-endian storage (like images)
            lcd.buffer[pixel_index] = color & 0xFF
            lcd.buffer[pixel_index + 1] = (color >> 8) & 0xFF

    lcd.text("framebuffer", 130, 70, lcd.white)
    lcd.show()

    print("  Left (fill_rect) vs Right (framebuffer)")
    print("  Are they the same color?")

    time.sleep(5)

print("\n=== Test complete ===")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTest ended")

# Test intermediate intensity values
# Compare fill_rect vs direct framebuffer write

from LCD_1inch28 import LCD_1inch28
import time

def rgb_to_brg565(r, g, b):
    """BRG format conversion."""
    return ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

print("=== Intermediate Value Test ===")

# Test intermediate red value (32 out of 255)
test_r = 32

print(f"\nTesting red value {test_r}:")
print(f"  rgb_to_brg565({test_r}, 0, 0) = 0x{rgb_to_brg565(test_r, 0, 0):04X}")

lcd.fill(lcd.black)
lcd.text("Red=32 Test", 80, 10, lcd.white)

# Method 1: Using fill_rect
color = rgb_to_brg565(test_r, 0, 0)
lcd.fill_rect(0, 30, 120, 90, color)
lcd.text("fill_rect", 30, 70, lcd.white)

# Method 2: Direct framebuffer write
color_fb = rgb_to_brg565(test_r, 0, 0)
for y in range(30, 120):
    for x in range(120, 240):
        pixel_index = (y * 240 + x) * 2
        lcd.buffer[pixel_index] = color_fb & 0xFF
        lcd.buffer[pixel_index + 1] = (color_fb >> 8) & 0xFF

lcd.text("framebuffer", 135, 70, lcd.white)

lcd.show()

print("\nCompare left (fill_rect) vs right (framebuffer):")
print("  Both should be VERY DARK RED")
print("  Are they the same color?")

time.sleep(10)

# Test Light Pink (255, 182, 193)
print(f"\nTesting Light Pink (255, 182, 193):")
color_pink = rgb_to_brg565(255, 182, 193)
print(f"  rgb_to_brg565(255, 182, 193) = 0x{color_pink:04X}")

lcd.fill(lcd.black)
lcd.text("Pink Test", 85, 10, lcd.white)

# Method 1: fill_rect
lcd.fill_rect(0, 30, 120, 90, color_pink)
lcd.text("fill_rect", 30, 70, lcd.white)

# Method 2: Direct framebuffer
for y in range(30, 120):
    for x in range(120, 240):
        pixel_index = (y * 240 + x) * 2
        lcd.buffer[pixel_index] = color_pink & 0xFF
        lcd.buffer[pixel_index + 1] = (color_pink >> 8) & 0xFF

lcd.text("framebuffer", 135, 70, lcd.white)

lcd.show()

print("\nCompare left (fill_rect) vs right (framebuffer):")
print("  Both should be LIGHT PINK")
print("  What colors do you see?")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTest ended")

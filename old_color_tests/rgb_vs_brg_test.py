# Test RGB565 vs BRG565 for fill_rect

from LCD_1inch28 import LCD_1inch28
import time

def rgb_to_rgb565(r, g, b):
    """Standard RGB565 format."""
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

def rgb_to_brg565(r, g, b):
    """BRG565 format."""
    return ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

print("=== RGB vs BRG Format Test ===")

# Test Light Pink with both formats
print("\nLight Pink (255, 182, 193):")

rgb_format = rgb_to_rgb565(255, 182, 193)
brg_format = rgb_to_brg565(255, 182, 193)

print(f"  RGB565 format: 0x{rgb_format:04X}")
print(f"  BRG565 format: 0x{brg_format:04X}")

lcd.fill(lcd.black)
lcd.text("Light Pink", 80, 10, lcd.white)

# Left: RGB565
lcd.fill_rect(0, 30, 120, 90, rgb_format)
lcd.text("RGB565", 30, 70, lcd.white)

# Right: BRG565
lcd.fill_rect(120, 30, 120, 90, brg_format)
lcd.text("BRG565", 135, 70, lcd.white)

lcd.show()

print("\nLeft (RGB565) vs Right (BRG565):")
print("  Which one looks like light pink?")

time.sleep(10)

# Test with red=32
print("\nDark red (32, 0, 0):")

rgb_format = rgb_to_rgb565(32, 0, 0)
brg_format = rgb_to_brg565(32, 0, 0)

print(f"  RGB565 format: 0x{rgb_format:04X}")
print(f"  BRG565 format: 0x{brg_format:04X}")

lcd.fill(lcd.black)
lcd.text("Dark Red", 85, 10, lcd.white)

lcd.fill_rect(0, 30, 120, 90, rgb_format)
lcd.text("RGB565", 30, 70, lcd.white)

lcd.fill_rect(120, 30, 120, 90, brg_format)
lcd.text("BRG565", 135, 70, lcd.white)

lcd.show()

print("\nWhich one shows as dark red?")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTest ended")

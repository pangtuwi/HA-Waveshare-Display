# Test grayscale WITHOUT gamma correction

from LCD_1inch28 import LCD_1inch28
import time

def rgb_to_brg565_no_gamma(r, g, b):
    """BRG565 without gamma correction."""
    return ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

print("=== Grayscale NO Gamma Test ===")

gray_values = [0, 32, 64, 96, 128, 160, 192, 224, 255]

for gray_val in gray_values:
    print(f"\nGray {gray_val} (no gamma):")

    color = rgb_to_brg565_no_gamma(gray_val, gray_val, gray_val)
    print(f"  Color: 0x{color:04X}")

    # Decode
    b_bits = (color >> 11) & 0x1F
    r_bits = (color >> 5) & 0x3F
    g_bits = color & 0x1F

    print(f"  Decoded: B={b_bits}/31, R={r_bits}/63, G={g_bits}/31")

    lcd.fill(lcd.black)
    lcd.text(f"Gray {gray_val}", 80, 50, lcd.white)
    lcd.fill_rect(60, 80, 120, 80, color)
    lcd.show()

    print(f"  What color do you see?")

    time.sleep(3)

print("\n=== Test complete ===")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTest ended")

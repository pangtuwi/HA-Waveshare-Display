# Test single grayscale values one at a time

from LCD_1inch28 import LCD_1inch28
import time

def apply_gamma_correction(value, gamma=2.2):
    """Apply gamma correction."""
    normalized = value / 255.0
    corrected = pow(normalized, 1.0 / gamma)
    return int(corrected * 255.0)

def rgb_to_brg565(r, g, b):
    """BRG565 with gamma correction."""
    r = apply_gamma_correction(r, 2.2)
    g = apply_gamma_correction(g, 2.2)
    b = apply_gamma_correction(b, 2.2)
    return ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

print("=== Single Grayscale Test ===")

# Test each gray value individually with delay
gray_values = [0, 32, 64, 96, 128, 160, 192, 224, 255]

for gray_val in gray_values:
    print(f"\nGray {gray_val}:")

    r_corr = apply_gamma_correction(gray_val, 2.2)
    g_corr = apply_gamma_correction(gray_val, 2.2)
    b_corr = apply_gamma_correction(gray_val, 2.2)

    print(f"  After gamma: ({r_corr}, {g_corr}, {b_corr})")

    color = rgb_to_brg565(gray_val, gray_val, gray_val)
    print(f"  Color: 0x{color:04X}")

    # Draw ONLY this gray value
    lcd.fill(lcd.black)
    lcd.text(f"Gray {gray_val}", 80, 50, lcd.white)
    lcd.fill_rect(60, 80, 120, 80, color)
    lcd.show()

    print(f"  What color do you see? (should be gray)")

    time.sleep(3)

print("\n=== Test complete ===")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTest ended")

# Test if gamma correction fixes test pattern colors

from LCD_1inch28 import LCD_1inch28
import time

def apply_gamma_correction(value, gamma=2.2):
    """Apply gamma correction."""
    normalized = value / 255.0
    corrected = pow(normalized, 1.0 / gamma)
    return int(corrected * 255.0)

def rgb_to_brg565_no_gamma(r, g, b):
    """BRG565 without gamma."""
    return ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

def rgb_to_brg565_with_gamma(r, g, b, gamma=2.2):
    """BRG565 with gamma correction."""
    if gamma != 1.0:
        r = apply_gamma_correction(r, gamma)
        g = apply_gamma_correction(g, gamma)
        b = apply_gamma_correction(b, gamma)
    return ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

print("=== Gamma Correction Test ===")

# Test Light Pink (255, 182, 193)
print("\nLight Pink (255, 182, 193):")

# Without gamma
color_no_gamma = rgb_to_brg565_no_gamma(255, 182, 193)
print(f"  Without gamma: 0x{color_no_gamma:04X}")

# With gamma
color_with_gamma = rgb_to_brg565_with_gamma(255, 182, 193, 2.2)
print(f"  With gamma:    0x{color_with_gamma:04X}")

lcd.fill(lcd.black)
lcd.text("Light Pink Test", 60, 10, lcd.white)

# Left: No gamma
lcd.fill_rect(0, 30, 120, 90, color_no_gamma)
lcd.text("NO gamma", 25, 70, lcd.white)

# Right: With gamma
lcd.fill_rect(120, 30, 120, 90, color_with_gamma)
lcd.text("WITH gamma", 130, 70, lcd.white)

lcd.show()

print("\nLeft (no gamma) vs Right (with gamma):")
print("  Which one looks like light pink?")

time.sleep(10)

# Test Standard Pink (255, 192, 203)
print("\nStandard Pink (255, 192, 203):")

color_no_gamma = rgb_to_brg565_no_gamma(255, 192, 203)
print(f"  Without gamma: 0x{color_no_gamma:04X}")

color_with_gamma = rgb_to_brg565_with_gamma(255, 192, 203, 2.2)
print(f"  With gamma:    0x{color_with_gamma:04X}")

lcd.fill(lcd.black)
lcd.text("Standard Pink", 70, 10, lcd.white)

lcd.fill_rect(0, 30, 120, 90, color_no_gamma)
lcd.text("NO gamma", 25, 70, lcd.white)

lcd.fill_rect(120, 30, 120, 90, color_with_gamma)
lcd.text("WITH gamma", 130, 70, lcd.white)

lcd.show()

print("\nWhich side looks correct?")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTest ended")

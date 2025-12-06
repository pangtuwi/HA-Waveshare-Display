# Debug grayscale gamma correction

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

print("=== Grayscale Gamma Debug ===")

# Test each grayscale value
for i in range(8):
    gray_val = i * 32

    # Apply gamma to each channel
    r_corrected = apply_gamma_correction(gray_val, 2.2)
    g_corrected = apply_gamma_correction(gray_val, 2.2)
    b_corrected = apply_gamma_correction(gray_val, 2.2)

    print(f"\nGray {gray_val}:")
    print(f"  After gamma: R={r_corrected}, G={g_corrected}, B={b_corrected}")
    print(f"  RGB equal? {r_corrected == g_corrected == b_corrected}")

    color = rgb_to_brg565(gray_val, gray_val, gray_val)
    print(f"  RGB565: 0x{color:04X}")

    # Decode the RGB565 value
    blue_bits = (color >> 11) & 0x1F
    red_bits = (color >> 5) & 0x3F
    green_bits = color & 0x1F

    print(f"  Decoded: B={blue_bits}/31, R={red_bits}/63, G={green_bits}/31")

# Display grayscale
lcd.fill(lcd.black)
lcd.text("Grayscale Test", 70, 10, lcd.white)

for i in range(8):
    gray_val = i * 32
    color = rgb_to_brg565(gray_val, gray_val, gray_val)
    lcd.fill_rect(i * 30, 30, 30, 60, color)
    lcd.text(str(gray_val), i * 30 + 5, 95, lcd.white)

lcd.show()

print("\n=== Test complete ===")
print("Does the display show a gray gradient?")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTest ended")

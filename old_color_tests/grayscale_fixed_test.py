# Test grayscale with proper RGB565 scaling

from LCD_1inch28 import LCD_1inch28
import time

def apply_gamma_correction(value, gamma=2.2):
    """Apply gamma correction."""
    normalized = value / 255.0
    corrected = pow(normalized, 1.0 / gamma)
    return int(corrected * 255.0)

def rgb_to_brg565_grayscale(gray):
    """
    Convert grayscale to BRG565 with proper bit depth scaling.

    For true grayscale, we need to ensure R, G, B have the same
    relative intensity despite different bit depths.
    """
    gray = apply_gamma_correction(gray, 2.2)

    # Scale each channel to its bit depth to maintain equal intensity
    # Red: 6 bits (0-63), Green: 5 bits (0-31), Blue: 5 bits (0-31)
    r_6bit = int((gray / 255.0) * 63)  # Scale to 0-63
    g_5bit = int((gray / 255.0) * 31)  # Scale to 0-31
    b_5bit = int((gray / 255.0) * 31)  # Scale to 0-31

    # Pack into RGB565 BRG format
    rgb565 = (b_5bit << 11) | (r_6bit << 5) | g_5bit
    return rgb565

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

print("=== Grayscale Fixed Test ===")

gray_values = [0, 32, 64, 96, 128, 160, 192, 224, 255]

for gray_val in gray_values:
    print(f"\nGray {gray_val}:")

    color = rgb_to_brg565_grayscale(gray_val)
    print(f"  Color: 0x{color:04X}")

    # Decode
    b_5bit = (color >> 11) & 0x1F
    r_6bit = (color >> 5) & 0x3F
    g_5bit = color & 0x1F

    print(f"  Decoded: B={b_5bit}/31 ({b_5bit/31.0*100:.1f}%), R={r_6bit}/63 ({r_6bit/63.0*100:.1f}%), G={g_5bit}/31 ({g_5bit/31.0*100:.1f}%)")

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

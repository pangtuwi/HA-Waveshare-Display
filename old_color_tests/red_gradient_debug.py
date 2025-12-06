# Red Gradient Debug Test
# Diagnose color conversion issues

from LCD_1inch28 import LCD_1inch28
import time

def apply_gamma_correction(value, gamma=2.2):
    """Apply gamma correction."""
    normalized = value / 255.0
    corrected = pow(normalized, 1.0 / gamma)
    return int(corrected * 255.0)

def rgb_to_brg565_with_gamma(r, g, b, gamma=2.2):
    """Convert RGB888 to RGB565 BRG format with gamma."""
    if gamma != 1.0:
        r_corrected = apply_gamma_correction(r, gamma)
        g_corrected = apply_gamma_correction(g, gamma)
        b_corrected = apply_gamma_correction(b, gamma)
    else:
        r_corrected = r
        g_corrected = g
        b_corrected = b

    rgb565 = ((b_corrected & 0xF8) << 8) | ((r_corrected & 0xFC) << 3) | (g_corrected >> 3)
    return rgb565, r_corrected, g_corrected, b_corrected

def rgb_to_brg565_no_gamma(r, g, b):
    """Convert RGB888 to RGB565 BRG format without gamma."""
    rgb565 = ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)
    return rgb565

# Initialize display
lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

print("=== Red Gradient Debug ===")
print("\nTesting red values with and without gamma correction")

# Test red gradient WITHOUT gamma
print("\n--- Test 1: Red gradient WITHOUT gamma ---")
lcd.fill(lcd.black)
lcd.text("Red: NO gamma", 60, 10, lcd.white)

for i in range(8):
    red_val = i * 32
    color = rgb_to_brg565_no_gamma(red_val, 0, 0)
    lcd.fill_rect(i * 30, 30, 30, 60, color)
    lcd.text(str(red_val), i * 30 + 5, 95, lcd.white)
    print(f"  Red {red_val:3d} -> RGB565: 0x{color:04X}")

lcd.show()
time.sleep(5)

# Test red gradient WITH gamma
print("\n--- Test 2: Red gradient WITH gamma 2.2 ---")
lcd.fill(lcd.black)
lcd.text("Red: gamma 2.2", 60, 10, lcd.white)

for i in range(8):
    red_val = i * 32
    color, r_cor, g_cor, b_cor = rgb_to_brg565_with_gamma(red_val, 0, 0, 2.2)
    lcd.fill_rect(i * 30, 30, 30, 60, color)
    lcd.text(str(red_val), i * 30 + 5, 95, lcd.white)
    print(f"  Red {red_val:3d} -> corrected {r_cor:3d} -> RGB565: 0x{color:04X}")

lcd.show()
time.sleep(5)

# Test if LCD.red constant works correctly
print("\n--- Test 3: LCD predefined colors ---")
lcd.fill(lcd.black)
lcd.text("LCD Constants", 70, 10, lcd.white)

# Display LCD's predefined red
lcd.fill_rect(0, 30, 80, 60, lcd.red)
lcd.text("lcd.red", 10, 60, lcd.white)
print(f"  lcd.red = 0x{lcd.red:04X}")

# Display our converted red (255, 0, 0) no gamma
color_no_g = rgb_to_brg565_no_gamma(255, 0, 0)
lcd.fill_rect(80, 30, 80, 60, color_no_g)
lcd.text("255 no-g", 85, 60, lcd.white)
print(f"  Our red (no gamma) = 0x{color_no_g:04X}")

# Display our converted red (255, 0, 0) with gamma
color_with_g, r_c, g_c, b_c = rgb_to_brg565_with_gamma(255, 0, 0, 2.2)
lcd.fill_rect(160, 30, 80, 60, color_with_g)
lcd.text("255 w-g", 170, 60, lcd.white)
print(f"  Our red (with gamma) = 0x{color_with_g:04X}")

lcd.show()
time.sleep(5)

# Test specific problematic values
print("\n--- Test 4: Specific values from user report ---")
lcd.fill(lcd.black)
lcd.text("Problem Values", 70, 10, lcd.white)

test_values = [0, 32, 64, 96, 128, 160, 192, 224]
for idx, red_val in enumerate(test_values):
    color, r_cor, g_cor, b_cor = rgb_to_brg565_with_gamma(red_val, 0, 0, 2.2)

    # Draw color block
    x = (idx % 4) * 60
    y = 30 + (idx // 4) * 90
    lcd.fill_rect(x, y, 60, 50, color)
    lcd.text(str(red_val), x + 15, y + 55, lcd.white)
    lcd.text(f">{r_cor}", x + 10, y + 65, lcd.white)

    # Decode RGB565 to verify what's stored
    blue_bits = (color >> 8) & 0xF8
    red_bits = (color >> 3) & 0xFC
    green_bits = (color << 3) & 0xF8

    print(f"  Red {red_val:3d} -> corrected ({r_cor}, {g_cor}, {b_cor})")
    print(f"    RGB565: 0x{color:04X} -> decoded as RGB({red_bits}, {green_bits}, {blue_bits})")

lcd.show()

print("\n=== Debug test complete ===")
print("Observe the display colors and compare to console output")
print("Press Ctrl+C to exit")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDebug test ended")

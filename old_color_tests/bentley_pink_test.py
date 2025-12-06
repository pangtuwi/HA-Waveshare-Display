# Test the exact pink from Bentley logo

from LCD_1inch28 import LCD_1inch28
import time

def rgb_to_brg565(r, g, b):
    """BRG565 format."""
    return ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

print("=== Bentley Pink Test ===")

# Test different pink values
pinks = [
    (255, 204, 204, "Bentley Pink"),
    (255, 192, 203, "Standard Pink"),
    (255, 182, 193, "Light Pink"),
]

for r, g, b, label in pinks:
    color = rgb_to_brg565(r, g, b)
    print(f"\n{label} ({r}, {g}, {b}):")
    print(f"  Color value: 0x{color:04X}")

    lcd.fill(lcd.black)
    lcd.text(label, 80, 50, lcd.white)
    lcd.fill_rect(60, 80, 120, 80, color)
    lcd.show()

    time.sleep(5)

print("\n=== Test complete ===")
print("Did Bentley Pink display correctly without gamma?")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTest ended")

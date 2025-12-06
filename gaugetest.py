from LCD_1inch28 import LCD_1inch28
from circular_gauge import CircularGauge, rgb_to_brg565
import time

# Initialize the LCD display
lcd = LCD_1inch28()

# Set brightness to maximum
lcd.set_bl_pwm(65535)

# Quick color test to verify rgb_to_brg565
print("\nColor conversion verification:")
print(f"  lcd.red = 0x{lcd.red:04X}")
print(f"  lcd.green = 0x{lcd.green:04X}")
print(f"  lcd.blue = 0x{lcd.blue:04X}")
print(f"  rgb_to_brg565(255,0,0) = 0x{rgb_to_brg565(255,0,0):04X} (should match lcd.red)")
print(f"  rgb_to_brg565(0,255,0) = 0x{rgb_to_brg565(0,255,0):04X} (should match lcd.green)")
print(f"  rgb_to_brg565(0,0,255) = 0x{rgb_to_brg565(0,0,255):04X} (should match lcd.blue)")
print()

# Test 8: Color variations (using BRG format)
print("\nTest 8: Different colors")
colors = [
    (lcd.white, "White"),
    (lcd.red, "Red"),
    (lcd.green, "Green"),
    (lcd.blue, "Blue"),
    (rgb_to_brg565(255, 255, 0), "Yellow"),
    (rgb_to_brg565(0, 255, 255), "Cyan"),
    (rgb_to_brg565(255, 224, 0), "Orange (90% grn)"),
    (rgb_to_brg565(224, 0, 255), "Purple (88% red)"),
    (rgb_to_brg565(255, 0, 255), "Magenta"),
]
for color, label in colors:
    lcd.fill(lcd.black)
    gauge = CircularGauge(
        lcd=lcd,
        center_x=120,
        center_y=120,
        radius=110,
        thickness=12,
        segments=12,
        start_angle=135,
        end_angle=405,
        gap_degrees=2,
        color=color
    )
    gauge.update(80)
    lcd.text(label, 70, 220, lcd.white)
    lcd.show()
    print(f"  {label} at 80%")
    time.sleep(2)
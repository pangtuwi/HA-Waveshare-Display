# Simple color test - just use LCD predefined colors
from LCD_1inch28 import LCD_1inch28
import time

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

print("=== Simple LCD Predefined Color Test ===")
print(f"lcd.red   = 0x{lcd.red:04X}")
print(f"lcd.green = 0x{lcd.green:04X}")
print(f"lcd.blue  = 0x{lcd.blue:04X}")

# Test 1: Use predefined colors
lcd.fill(lcd.black)
lcd.text("Predefined Colors", 50, 10, lcd.white)

lcd.fill_rect(0, 30, 80, 60, lcd.red)
lcd.text("lcd.red", 10, 60, lcd.white)

lcd.fill_rect(80, 30, 80, 60, lcd.green)
lcd.text("lcd.green", 85, 60, lcd.white)

lcd.fill_rect(160, 30, 80, 60, lcd.blue)
lcd.text("lcd.blue", 165, 60, lcd.white)

lcd.show()

print("\nWhat colors do you see?")
print("  Top-left (lcd.red): Should be RED")
print("  Top-middle (lcd.green): Should be GREEN")
print("  Top-right (lcd.blue): Should be BLUE")

time.sleep(10)

# Test 2: Use our rgb_to_brg565 function
def rgb_to_brg565(r, g, b):
    return ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

lcd.fill(lcd.black)
lcd.text("rgb_to_brg565", 70, 10, lcd.white)

red_color = rgb_to_brg565(255, 0, 0)
green_color = rgb_to_brg565(0, 255, 0)
blue_color = rgb_to_brg565(0, 0, 255)

print(f"\nCalculated colors:")
print(f"  rgb_to_brg565(255,0,0) = 0x{red_color:04X} (vs lcd.red = 0x{lcd.red:04X})")
print(f"  rgb_to_brg565(0,255,0) = 0x{green_color:04X} (vs lcd.green = 0x{lcd.green:04X})")
print(f"  rgb_to_brg565(0,0,255) = 0x{blue_color:04X} (vs lcd.blue = 0x{lcd.blue:04X})")

lcd.fill_rect(0, 30, 80, 60, red_color)
lcd.text("Red calc", 10, 60, lcd.white)

lcd.fill_rect(80, 30, 80, 60, green_color)
lcd.text("Grn calc", 85, 60, lcd.white)

lcd.fill_rect(160, 30, 80, 60, blue_color)
lcd.text("Blu calc", 165, 60, lcd.white)

lcd.show()

print("\nWhat colors do you see NOW?")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTest ended")

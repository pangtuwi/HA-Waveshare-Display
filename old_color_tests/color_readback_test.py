# Read back framebuffer values to see what's actually stored

from LCD_1inch28 import LCD_1inch28
import time

def rgb_to_brg565(r, g, b):
    """BRG565 conversion."""
    return ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)

lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

print("=== Color Readback Test ===")

# Test Standard Pink (works correctly)
print("\nStandard Pink (255, 192, 203) - displays correctly:")
r, g, b = 255, 192, 203
color_standard = rgb_to_brg565(r, g, b)
print(f"  Input RGB: ({r}, {g}, {b})")
print(f"  Calculated: 0x{color_standard:04X}")
print(f"  Binary breakdown:")
print(f"    b & 0xF8 = {b & 0xF8} = 0x{(b & 0xF8):02X}")
print(f"    r & 0xFC = {r & 0xFC} = 0x{(r & 0xFC):02X}")
print(f"    g >> 3   = {g >> 3} = 0x{(g >> 3):02X}")

lcd.fill(lcd.black)
lcd.fill_rect(0, 0, 120, 120, color_standard)

# Read back the first pixel
pixel_val = lcd.buffer[0] | (lcd.buffer[1] << 8)
print(f"  Stored in buffer: [0]=0x{lcd.buffer[0]:02X}, [1]=0x{lcd.buffer[1]:02X}")
print(f"  Read back as: 0x{pixel_val:04X}")
print(f"  Match: {pixel_val == color_standard}")

lcd.show()
time.sleep(5)

# Test Light Pink (shows as yellow)
print("\nLight Pink (255, 182, 193) - shows as yellow:")
r, g, b = 255, 182, 193
color_light = rgb_to_brg565(r, g, b)
print(f"  Input RGB: ({r}, {g}, {b})")
print(f"  Calculated: 0x{color_light:04X}")
print(f"  Binary breakdown:")
print(f"    b & 0xF8 = {b & 0xF8} = 0x{(b & 0xF8):02X}")
print(f"    r & 0xFC = {r & 0xFC} = 0x{(r & 0xFC):02X}")
print(f"    g >> 3   = {g >> 3} = 0x{(g >> 3):02X}")

lcd.fill(lcd.black)
lcd.fill_rect(0, 0, 120, 120, color_light)

# Read back
pixel_val = lcd.buffer[0] | (lcd.buffer[1] << 8)
print(f"  Stored in buffer: [0]=0x{lcd.buffer[0]:02X}, [1]=0x{lcd.buffer[1]:02X}")
print(f"  Read back as: 0x{pixel_val:04X}")
print(f"  Match: {pixel_val == color_light}")

lcd.show()
time.sleep(5)

# Decode what colors these values represent in BRG format
print("\nDecoding BRG565 values:")
print(f"Standard Pink 0x{color_standard:04X}:")
print(f"  Bits 15-11 (Blue):  {(color_standard >> 11) & 0x1F} / 31 = {((color_standard >> 11) & 0x1F) / 31.0 * 100:.0f}%")
print(f"  Bits 10-5  (Red):   {(color_standard >> 5) & 0x3F} / 63 = {((color_standard >> 5) & 0x3F) / 63.0 * 100:.0f}%")
print(f"  Bits 4-0   (Green): {color_standard & 0x1F} / 31 = {(color_standard & 0x1F) / 31.0 * 100:.0f}%")

print(f"\nLight Pink 0x{color_light:04X}:")
print(f"  Bits 15-11 (Blue):  {(color_light >> 11) & 0x1F} / 31 = {((color_light >> 11) & 0x1F) / 31.0 * 100:.0f}%")
print(f"  Bits 10-5  (Red):   {(color_light >> 5) & 0x3F} / 63 = {((color_light >> 5) & 0x3F) / 63.0 * 100:.0f}%")
print(f"  Bits 4-0   (Green): {color_light & 0x1F} / 31 = {(color_light & 0x1F) / 31.0 * 100:.0f}%")

print("\n=== Test complete ===")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTest ended")

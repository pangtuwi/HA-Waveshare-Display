# Framebuffer Format Diagnostic Test
# Tests if framebuffer RGB565 format matches our expectations

from LCD_1inch28 import LCD_1inch28
import time

def rgb_to_brg565(r, g, b):
    """BRG format conversion."""
    rgb565 = ((b & 0xF8) << 8) | ((r & 0xFC) << 3) | (g >> 3)
    return rgb565

# Initialize display
lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)

print("=== Framebuffer Format Test ===")
print("\nLCD predefined colors:")
print(f"  lcd.red   = 0x{lcd.red:04X}")
print(f"  lcd.green = 0x{lcd.green:04X}")
print(f"  lcd.blue  = 0x{lcd.blue:04X}")
print(f"  lcd.white = 0x{lcd.white:04X}")

# Test 1: Use lcd.fill_rect directly with integer color values
print("\n--- Test 1: Direct integer colors ---")
lcd.fill(lcd.black)
lcd.text("Direct Colors", 70, 10, lcd.white)

# Try small red values directly
colors_to_test = [
    (0x0100, "0x0100"),  # Should be dark red in BRG format
    (0x0300, "0x0300"),  # Should be medium-dark red
    (0x0500, "0x0500"),  # Should be medium red
    (0x07E0, "0x07E0"),  # lcd.red (should be bright red)
]

for idx, (color_val, label) in enumerate(colors_to_test):
    x = idx * 60
    lcd.fill_rect(x, 30, 60, 60, color_val)
    lcd.text(label, x + 5, 95, lcd.white)
    print(f"  Testing {label}")

lcd.show()
time.sleep(10)

# Test 2: Write directly to framebuffer
print("\n--- Test 2: Direct framebuffer manipulation ---")
lcd.fill(lcd.black)
lcd.text("Direct FB Write", 60, 10, lcd.white)

# Manually write RGB565 values to framebuffer
# Display is 240x240, framebuffer is row-major RGB565 (2 bytes per pixel)

# Draw a 60x60 block starting at (0, 30) with color 0x0100
# This should be dark red if BRG format is correct
block_color = 0x0100
for y in range(30, 90):
    for x in range(0, 60):
        pixel_index = (y * 240 + x) * 2  # 2 bytes per pixel
        # Write as little-endian: low byte first, then high byte
        lcd.buffer[pixel_index] = block_color & 0xFF
        lcd.buffer[pixel_index + 1] = (block_color >> 8) & 0xFF

lcd.text("0x0100", 10, 95, lcd.white)

# Draw another block with 0x0300
block_color = 0x0300
for y in range(30, 90):
    for x in range(60, 120):
        pixel_index = (y * 240 + x) * 2
        lcd.buffer[pixel_index] = block_color & 0xFF
        lcd.buffer[pixel_index + 1] = (block_color >> 8) & 0xFF

lcd.text("0x0300", 70, 95, lcd.white)

# Draw lcd.red for comparison
lcd.fill_rect(120, 30, 60, 60, lcd.red)
lcd.text("lcd.red", 130, 95, lcd.white)

lcd.show()
print("  Directly wrote 0x0100, 0x0300, and lcd.red to framebuffer")
time.sleep(10)

# Test 3: Check framebuffer format by reading back lcd.red
print("\n--- Test 3: Read back framebuffer values ---")
lcd.fill(lcd.black)
lcd.fill_rect(0, 0, 60, 60, lcd.red)
lcd.fill_rect(60, 0, 60, 60, lcd.green)
lcd.fill_rect(120, 0, 60, 60, lcd.blue)
lcd.show()

# Read back the pixel values
red_pixel = lcd.buffer[0] | (lcd.buffer[1] << 8)
green_pixel = lcd.buffer[(60 * 2)] | (lcd.buffer[(60 * 2) + 1] << 8)
blue_pixel = lcd.buffer[(120 * 2)] | (lcd.buffer[(120 * 2) + 1] << 8)

print(f"  Red pixel readback:   0x{red_pixel:04X} (expected 0x{lcd.red:04X})")
print(f"  Green pixel readback: 0x{green_pixel:04X} (expected 0x{lcd.green:04X})")
print(f"  Blue pixel readback:  0x{blue_pixel:04X} (expected 0x{lcd.blue:04X})")

# Check byte order
print(f"\n  Red pixel bytes: [0]=0x{lcd.buffer[0]:02X}, [1]=0x{lcd.buffer[1]:02X}")
print(f"  Expected for 0x{lcd.red:04X}: low=0x{lcd.red & 0xFF:02X}, high=0x{(lcd.red >> 8) & 0xFF:02X}")

time.sleep(10)

print("\n=== Test complete ===")
print("Compare display colors to console values")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nFramebuffer test ended")

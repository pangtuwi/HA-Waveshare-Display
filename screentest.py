from LCD_1inch28 import LCD_1inch28
import time

# Initialize the LCD display
lcd = LCD_1inch28()

# Set brightness to maximum
lcd.set_bl_pwm(65535)

# Clear screen with white background
lcd.fill(lcd.white)

# Display "Hello World" in the center
# Screen is 240x240, text is 8 pixels high
# Center text at approximately (80, 116) for good centering
lcd.text("Hello World", 80, 116, lcd.black)

# Show the display
lcd.show()

print("Screen test complete - displaying 'Hello World'")

# Keep the display on
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Screen test ended")

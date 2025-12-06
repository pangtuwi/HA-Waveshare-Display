# Image Display Test Script
# Tests image display functionality on Waveshare RP2350

from LCD_1inch28 import LCD_1inch28
from circular_gauge import CircularGauge, rgb_to_brg565
from image_data import get_image, get_image_names, get_image_count
from image_display import (display_image_background, display_image_with_text,
                           display_image_with_gauge, display_image_with_overlays)
import time

print("=== Image Display Test ===")

# Initialize display
lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)  # Maximum brightness

# Check if any images are available
image_count = get_image_count()
print(f"Found {image_count} image(s)")



img_name = get_image_names()[0]
img_data = get_image(img_name)

# Create two small gauges
gauge1 = CircularGauge(
    lcd=lcd, 
    center_x=120, 
    center_y=120,
    radius=115,
    thickness=10,
    segments=20, start_angle=215, end_angle=320,
    gap_degrees=2, 
    clockwise=True,
    color=lcd.white,
    background_color=rgb_to_brg565(230, 135, 230) 
)

    
display_image_with_overlays(
    lcd, img_data,
    gauge_items=[
        (gauge1, 70)
    ]
)
time.sleep(4)



# Keep display on
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDisplay ended")

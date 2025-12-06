# Image Display Test Script
# Tests image display functionality on Waveshare RP2350

from LCD_1inch28 import LCD_1inch28
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

if image_count == 0:
    print("\nNo images found in image_data.py")
    print("To add images:")
    print("1. On PC, run: python convert_image.py your_image.jpg image_name > temp.py")
    print("2. Copy output into image_data.py")
    print("3. Upload: mpremote cp image_data.py :image_data.py")

    # Display message on screen
    lcd.fill(lcd.black)
    lcd.write_text("No Images", 50, 100, 2, lcd.white)
    lcd.text("See console", 70, 140, lcd.white)
    lcd.show()

else:
    print("Available images:", get_image_names())

    # Test 1: Display each image
    print("\nTest 1: Displaying each image")
    for img_name in get_image_names():
        print(f"  Displaying: {img_name}")
        img_data = get_image(img_name)
        if img_data:
            display_image_background(lcd, img_data)
            time.sleep(10)
        else:
            print(f"  Error: Could not load {img_name}")

    # Test 2: Image with text overlay
    if get_image_count() > 0:
        print("\nTest 2: Image with text overlay")
        img_name = get_image_names()[0]
        img_data = get_image(img_name)

        display_image_with_text(lcd, img_data, [
            ("Test Display", 60, 50, lcd.white, 2),
            ("Text Overlay", 55, 100, lcd.white, 2),
            ("Standard text", 65, 150, lcd.white, None),
        ])
        time.sleep(3)

    # Test 3: Image with custom text positions
    if get_image_count() > 0:
        print("\nTest 3: Custom text layout")
        img_name = get_image_names()[0]
        img_data = get_image(img_name)

        display_image_with_text(lcd, img_data, [
            ("Top", 100, 10, lcd.white, 2),
            ("Middle", 85, 110, lcd.white, 3),
            ("Bottom", 85, 210, lcd.white, 2),
        ])
        time.sleep(3)

    # Test 4: Cycle through images
    if get_image_count() > 1:
        print("\nTest 4: Cycling through images")
        for i in range(3):  # Cycle 3 times
            for img_name in get_image_names():
                print(f"  Cycle {i+1}: {img_name}")
                img_data = get_image(img_name)
                display_image_background(lcd, img_data)
                time.sleep(1)

    # Test 5: Test with CircularGauge (if available)
    try:
        from circular_gauge import CircularGauge

        if get_image_count() > 0:
            print("\nTest 5: Image with circular gauge overlay")
            img_name = get_image_names()[0]
            img_data = get_image(img_name)

            # Create a gauge
            gauge = CircularGauge(
                lcd=lcd,
                center_x=120,
                center_y=120,
                radius=80,
                thickness=10,
                segments=12,
                start_angle=135,
                end_angle=405,
                gap_degrees=2,
                color=lcd.white,
                background_color=0x2104  # Dark grey
            )

            # Animate gauge from 0 to 100
            for val in range(0, 101, 10):
                display_image_with_gauge(lcd, img_data, gauge, val)
                time.sleep(0.3)

            time.sleep(2)
    except ImportError:
        print("\nTest 5: Skipped (circular_gauge.py not found)")

    # Test 6: Test with bitmap fonts (if available)
    try:
        import bitmap_fonts_48
        from image_display import display_image_with_bitmap_text

        if get_image_count() > 0:
            print("\nTest 6: Image with bitmap font overlay")
            img_name = get_image_names()[0]
            img_data = get_image(img_name)

            display_image_with_bitmap_text(
                lcd, img_data, bitmap_fonts_48,
                "12:34", 60, 90, lcd.white, spacing=4
            )
            time.sleep(3)
    except ImportError:
        print("\nTest 6: Skipped (bitmap_fonts_48.py not found)")

    # Test 7: Multiple overlays
    try:
        from circular_gauge import CircularGauge

        if get_image_count() > 0:
            print("\nTest 7: Image with multiple overlays")
            img_name = get_image_names()[0]
            img_data = get_image(img_name)

            # Create two small gauges
            gauge1 = CircularGauge(
                lcd=lcd, center_x=60, center_y=120, radius=45,
                thickness=8, segments=8, start_angle=135, end_angle=405,
                gap_degrees=2, color=lcd.white
            )

            gauge2 = CircularGauge(
                lcd=lcd, center_x=180, center_y=120, radius=45,
                thickness=8, segments=8, start_angle=135, end_angle=405,
                gap_degrees=2, color=lcd.white
            )

            display_image_with_overlays(
                lcd, img_data,
                text_items=[
                    ("Sensors", 85, 20, lcd.white, 2),
                    ("Temp", 35, 180, lcd.white, None),
                    ("Humidity", 140, 180, lcd.white, None),
                ],
                gauge_items=[
                    (gauge1, 72),
                    (gauge2, 55),
                ]
            )
            time.sleep(4)
    except ImportError:
        print("\nTest 7: Skipped (circular_gauge.py not found)")

    print("\n=== All Tests Complete ===")

    # Final display
    if get_image_count() > 0:
        img_name = get_image_names()[0]
        img_data = get_image(img_name)
        display_image_with_text(lcd, img_data, [
            ("Tests", 90, 100, lcd.white, 3),
            ("Complete!", 70, 140, lcd.white, 2),
        ])

print("\nImage display tests finished!")
print("Press Ctrl+C to exit")

# Keep display on
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTest ended")

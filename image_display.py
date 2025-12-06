# Image Display Utilities for Waveshare RP2350 Display
# Provides functions for displaying images as backgrounds with text/graphics overlay

def load_image_to_framebuffer(lcd, image_data):
    """
    Load image byte array directly into LCD framebuffer.

    Args:
        lcd: LCD_1inch28 instance
        image_data: bytes object OR tuple of bytes chunks (total 115,200 bytes for 240x240 RGB565)

    Returns:
        True if successful, False otherwise

    Example:
        from image_data import get_image
        img = get_image('background1')
        load_image_to_framebuffer(lcd, img)
        lcd.show()
    """
    # Handle chunked image data (tuple of bytes objects)
    if isinstance(image_data, tuple):
        # Calculate total size
        total_size = sum(len(chunk) for chunk in image_data)
        if total_size != 115200:
            print(f"Error: Image data must be 115,200 bytes, got {total_size}")
            return False

        # Copy chunks sequentially to framebuffer
        offset = 0
        for chunk in image_data:
            chunk_len = len(chunk)
            for i in range(chunk_len):
                lcd.buffer[offset + i] = chunk[i]
            offset += chunk_len

        return True

    # Handle single bytes object (original format)
    if len(image_data) != 115200:
        print(f"Error: Image data must be 115,200 bytes, got {len(image_data)}")
        return False

    # Copy image data directly to framebuffer
    # Using slice assignment for better performance if available
    try:
        lcd.buffer[:] = image_data
    except:
        # Fallback to byte-by-byte copy
        for i in range(len(image_data)):
            lcd.buffer[i] = image_data[i]

    return True


def display_image_background(lcd, image_data, show=True):
    """
    Display image as background and optionally push to screen.

    Args:
        lcd: LCD_1inch28 instance
        image_data: bytes object with image data
        show: If True, call lcd.show() to display immediately (default True)

    Returns:
        True if successful

    Example:
        from image_data import get_image
        background = get_image('background1')
        display_image_background(lcd, background)
    """
    if not load_image_to_framebuffer(lcd, image_data):
        return False

    if show:
        lcd.show()

    return True


def display_image_with_text(lcd, image_data, text_items, show=True):
    """
    Display image background with text overlay.

    Args:
        lcd: LCD_1inch28 instance
        image_data: bytes object with image data
        text_items: List of tuples (text, x, y, color, size)
                   size can be 1-5 for write_text, or None for standard 8x8 text
        show: If True, call lcd.show() after drawing (default True)

    Returns:
        True if successful

    Example:
        from image_data import get_image
        display_image_with_text(lcd, get_image('background1'), [
            ("Temperature", 10, 10, lcd.white, 2),
            ("22.5°C", 60, 100, lcd.white, 4),
            ("Humidity", 10, 150, lcd.white, None),  # None = standard text
        ])
    """
    # Load background image
    if not load_image_to_framebuffer(lcd, image_data):
        return False

    # Draw text overlays
    for item in text_items:
        if len(item) == 5:
            text, x, y, color, size = item
            if size is None:
                lcd.text(text, x, y, color)
            else:
                lcd.write_text(text, x, y, size, color)
        elif len(item) == 4:
            # Support 4-tuple format (text, x, y, color) - defaults to standard text
            text, x, y, color = item
            lcd.text(text, x, y, color)

    # Display
    if show:
        lcd.show()

    return True


def display_image_with_gauge(lcd, image_data, gauge, gauge_value, show=True):
    """
    Display image background with circular gauge overlay.

    Args:
        lcd: LCD_1inch28 instance
        image_data: bytes object with image data
        gauge: CircularGauge instance
        gauge_value: Value to display on gauge (0-100)
        show: If True, call lcd.show() after drawing (default True)

    Returns:
        True if successful

    Example:
        from circular_gauge import CircularGauge
        from image_data import get_image

        gauge = CircularGauge(lcd, 120, 120, 110, thickness=12, segments=16,
                             start_angle=135, end_angle=405, color=lcd.white)
        display_image_with_gauge(lcd, get_image('background1'), gauge, 75)
    """
    # Load background
    if not load_image_to_framebuffer(lcd, image_data):
        return False

    # Draw gauge on top (gauge draws directly to framebuffer)
    gauge.set_value(gauge_value)
    gauge.draw()

    # Display
    if show:
        lcd.show()

    return True


def display_image_with_bitmap_text(lcd, image_data, bitmap_font_module, text, x, y, color, spacing=2, show=True):
    """
    Display image background with bitmap font text overlay.

    Args:
        lcd: LCD_1inch28 instance
        image_data: bytes object with image data
        bitmap_font_module: Imported bitmap font module (bitmap_fonts, bitmap_fonts_32, or bitmap_fonts_48)
        text: Text string to display
        x: X coordinate
        y: Y coordinate
        color: Text color (RGB565)
        spacing: Pixel spacing between characters (default 2)
        show: If True, call lcd.show() after drawing (default True)

    Returns:
        True if successful

    Example:
        import bitmap_fonts_48
        from image_data import get_image

        display_image_with_bitmap_text(lcd, get_image('background1'),
                                       bitmap_fonts_48, "12:34", 60, 100, lcd.white)
    """
    # Load background
    if not load_image_to_framebuffer(lcd, image_data):
        return False

    # Draw bitmap text
    # Try different function name variations for different font modules
    if hasattr(bitmap_font_module, 'draw_text_48'):
        bitmap_font_module.draw_text_48(lcd, text, x, y, color, spacing)
    elif hasattr(bitmap_font_module, 'draw_text_32'):
        bitmap_font_module.draw_text_32(lcd, text, x, y, color, spacing)
    elif hasattr(bitmap_font_module, 'draw_text'):
        bitmap_font_module.draw_text(lcd, text, x, y, color, spacing)
    else:
        print("Error: Bitmap font module does not have a draw_text function")
        return False

    # Display
    if show:
        lcd.show()

    return True


def display_image_with_overlays(lcd, image_data, text_items=None, gauge_items=None, show=True):
    """
    Display image with multiple types of overlays (text and gauges).

    Args:
        lcd: LCD_1inch28 instance
        image_data: bytes object with image data
        text_items: Optional list of text tuples (text, x, y, color, size)
        gauge_items: Optional list of gauge tuples (gauge_instance, value)
        show: If True, call lcd.show() after drawing (default True)

    Returns:
        True if successful

    Example:
        from circular_gauge import CircularGauge
        from image_data import get_image

        temp_gauge = CircularGauge(lcd, 60, 120, 50, ...)
        humidity_gauge = CircularGauge(lcd, 180, 120, 50, ...)

        display_image_with_overlays(
            lcd,
            get_image('background1'),
            text_items=[("Sensors", 90, 20, lcd.white, 2)],
            gauge_items=[(temp_gauge, 72), (humidity_gauge, 55)]
        )
    """
    # Load background
    if not load_image_to_framebuffer(lcd, image_data):
        return False

    # Draw text overlays
    if text_items:
        for item in text_items:
            if len(item) == 5:
                text, x, y, color, size = item
                if size is None:
                    lcd.text(text, x, y, color)
                else:
                    lcd.write_text(text, x, y, size, color)
            elif len(item) == 4:
                text, x, y, color = item
                lcd.text(text, x, y, color)

    # Draw gauge overlays
    if gauge_items:
        for gauge, value in gauge_items:
            gauge.set_value(value)
            gauge.draw()

    # Display
    if show:
        lcd.show()

    return True

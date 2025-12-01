from machine import UART, Pin, RTC
from LCD_1inch28 import LCD_1inch28, Touch_CST816T
import time
import json
import bitmap_fonts

# Initialize UART
uart = UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17))

# Initialize RTC
rtc = RTC()

# Initialize display
lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)  # Set brightness to maximum

# Initialize touch controller
touch = Touch_CST816T(mode=1, LCD=lcd)  # Mode 1 = point mode

# Display welcome message
lcd.fill(lcd.white)
lcd.text("Home Assistant", 60, 100, lcd.black)
lcd.text("Display", 85, 120, lcd.black)
lcd.text("Ready!", 90, 140, lcd.black)
lcd.show()
print("Welcome message displayed")

# Wait for 2 seconds to show welcome message
time.sleep(2)

# Display settings
current_brightness = 100
current_mode = "Clock"
display_color = lcd.black

# Weather data
weather_condition = "N/A"
weather_temp = "N/A"
weather_humidity = "N/A"

# Sensor data (from IMU)
sensor_temp = "N/A"
sensor_accel_x = 0.0
sensor_accel_y = 0.0
sensor_accel_z = 0.0

def process_command(cmd_line):
    """Process incoming commands from Home Assistant via ESP32"""
    global current_brightness, current_mode, display_color, weather_condition, weather_temp, weather_humidity

    try:
        print(f"Received command: {cmd_line}")
        if cmd_line.startswith(b'MSG:'):
            # Display a text message
            message = cmd_line[4:].decode().strip()
            lcd.fill(lcd.white)
            lcd.text(message, 60, 120, display_color)
            lcd.show()
            print(f"Displayed: {message}")
            
        elif cmd_line.startswith(b'BRIGHT:'):
            # Adjust brightness
            brightness = int(cmd_line[7:].decode().strip())
            current_brightness = brightness
            lcd.set_bl_pwm(int(brightness * 65535 / 100))
            print(f"Brightness set to: {brightness}%")
            
        elif cmd_line.startswith(b'MODE:'):
            # Change display mode
            mode = cmd_line[5:].decode().strip()
            current_mode = mode
            print(f"Mode changed to: {mode}")
            update_display_for_mode(mode)
            
        elif cmd_line.startswith(b'CMD:CLEAR'):
            # Clear display
            lcd.fill(lcd.white)
            lcd.show()
            print("Display cleared")
            
        elif cmd_line.startswith(b'CMD:TIME'):
            # Show time (you'd get this from RTC or network)
            lcd.fill(lcd.white)
            lcd.text("12:34 PM", 80, 120, lcd.black)
            lcd.show()
            print("Time displayed")
            
        elif cmd_line.startswith(b'DISP:'):
            # Custom display command
            data = cmd_line[5:].decode().strip()
            lcd.fill(lcd.white)
            lcd.text(data, 60, 120, display_color)
            lcd.show()
            print(f"Custom display: {data}")
            
        elif cmd_line.startswith(b'COLOR:'):
            # Set text color (RGB)
            colors = cmd_line[6:].decode().strip().split(',')
            r, g, b = int(colors[0]), int(colors[1]), int(colors[2])
            # Convert RGB888 to RGB565 format (note: uses BRG format due to framebuf)
            display_color = ((b & 0xF8) << 8) | ((g & 0xFC) << 3) | (r >> 3)
            print(f"Color set to RGB({r},{g},{b})")

        elif cmd_line.startswith(b'SETTIME:'):
            # Set RTC time from ESP32
            # Format: SETTIME:YYYY,MM,DD,HH,MM,SS,WEEKDAY,YEARDAY
            time_str = cmd_line[8:].decode().strip()
            time_parts = time_str.split(',')
            if len(time_parts) == 8:
                year = int(time_parts[0])
                month = int(time_parts[1])
                day = int(time_parts[2])
                hour = int(time_parts[3])
                minute = int(time_parts[4])
                second = int(time_parts[5])
                weekday = int(time_parts[6])
                yearday = int(time_parts[7])
                rtc.datetime((year, month, day, weekday, hour, minute, second, 0))
                print(f"Time set to: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")
                # Refresh display if in clock mode
                if current_mode == "Clock":
                    update_display_for_mode(current_mode)

        elif cmd_line.startswith(b'WEATHER:'):
            # Update weather data
            # Format: WEATHER:condition,temperature,humidity
            weather_str = cmd_line[8:].decode().strip()
            weather_parts = weather_str.split(',')
            if len(weather_parts) == 3:
                weather_condition = weather_parts[0]
                weather_temp = weather_parts[1]
                weather_humidity = weather_parts[2]
                print(f"Weather updated: {weather_condition}, {weather_temp}, {weather_humidity}")
                # Refresh display if in weather mode
                if current_mode == "Weather":
                    update_display_for_mode(current_mode)

    except Exception as e:
        print(f"Error processing command: {e}")

def draw_mode_button(mode):
    """Draw a mode change button at the bottom of the screen"""
    # Button area: bottom 30 pixels (y: 210-240)
    button_color = lcd.blue if mode == "Clock" else lcd.red
    lcd.fill_rect(0, 210, 240, 30, button_color)
    lcd.text("MODE", 100, 220, lcd.white)

def cycle_mode():
    """Cycle to the next display mode"""
    global current_mode
    modes = ["Clock", "Sensors", "Weather", "Custom"]
    current_index = modes.index(current_mode)
    next_index = (current_index + 1) % len(modes)
    current_mode = modes[next_index]
    print(f"Mode changed to: {current_mode}")
    update_display_for_mode(current_mode)

def update_display_for_mode(mode):
    """Update display based on selected mode"""

    if mode == "Clock":
        # Black background for clock mode
        lcd.fill(lcd.black)

        # Get current time
        current_time = time.localtime()
        hour = current_time[3]
        minute = current_time[4]

        # Get date info
        year = current_time[0]
        month = current_time[1]
        day = current_time[2]
        weekday = current_time[6]

        # Day names
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_name = days[weekday]

        # Format time as 12-hour with AM/PM
        am_pm = "AM" if hour < 12 else "PM"
        display_hour = hour if hour < 12 else hour - 12
        if display_hour == 0:
            display_hour = 12

        # Just the time without AM/PM for larger display
        time_str = "{:02d}:{:02d}".format(display_hour, minute)

        # Top: Day and date
        date_str = "{} {}/{}/{}".format(day_name, day, month, year)
        lcd.text(date_str, 55, 50, lcd.white)

        # Center: Very large time using bitmap font (16x24 per char)
        # Calculate centering for time string
        time_width = bitmap_fonts.get_text_width(time_str, spacing=4)
        time_x = (240 - time_width) // 2
        bitmap_fonts.draw_text(lcd, time_str, time_x, 100, lcd.white, spacing=4)

        # AM/PM indicator below time
        lcd.write_text(am_pm, 100, 155, 2, lcd.white)

    elif mode == "Sensors":
        # Gradient background (top to bottom)
        lcd.fill(0xE73F)  # Light cyan background

        # Title
        lcd.text("SENSOR DATA", 70, 40, lcd.black)

        # Temperature section
        lcd.text("Temperature", 70, 70, lcd.black)
        if sensor_temp != "N/A":
            lcd.write_text(sensor_temp, 70, 85, 3, 0xF800)  # Red
        else:
            lcd.write_text("--.-C", 65, 85, 3, 0x7BEF)  # Gray

        # Accelerometer section
        lcd.text("Accelerometer", 60, 135, lcd.black)
        accel_text = "X:{:.1f} Y:{:.1f}".format(sensor_accel_x, sensor_accel_y)
        lcd.text(accel_text, 45, 155, lcd.black)
        z_text = "Z:{:.1f}g".format(sensor_accel_z)
        lcd.text(z_text, 85, 170, lcd.black)

    elif mode == "Weather":
        # Choose background color based on condition
        if "clear" in weather_condition.lower() or "sunny" in weather_condition.lower():
            bg_color = 0xFFE0  # Light yellow
        elif "cloud" in weather_condition.lower():
            bg_color = 0xCE79  # Light gray
        elif "rain" in weather_condition.lower() or "drizzle" in weather_condition.lower():
            bg_color = 0x5D1F  # Light blue
        else:
            bg_color = lcd.white

        lcd.fill(bg_color)

        # Weather condition at top (centered)
        condition_x = 120 - (len(weather_condition) * 4)  # Approximate centering
        lcd.write_text(weather_condition, condition_x, 40, 2, lcd.black)

        # Large temperature in center
        temp_display = weather_temp.replace("°C", "")
        temp_x = 60 if len(temp_display) <= 4 else 50
        lcd.write_text(temp_display, temp_x, 90, 4, lcd.black)
        lcd.text("C", 150, 105, lcd.black)

        # Humidity at bottom
        lcd.text("Humidity:", 75, 155, lcd.black)
        lcd.write_text(weather_humidity, 85, 170, 2, lcd.black)

    elif mode == "Custom":
        lcd.fill(lcd.white)
        lcd.text("Custom Mode", 60, 120, lcd.black)

    # Draw mode button at the bottom
    draw_mode_button(mode)

    lcd.show()

def send_sensor_data():
    """Send sensor data back to Home Assistant"""
    # Read from IMU or other sensors
    data = {
        "temperature": 22.5,
        "status": "OK",
        "mode": current_mode
    }
    uart.write(f"SENSOR:{json.dumps(data)}\n".encode())

# Display initial clock mode after welcome message
update_display_for_mode(current_mode)
print(f"Switched to {current_mode} mode")

# Main loop
last_sensor_update = time.ticks_ms()
last_clock_update = time.ticks_ms()
last_touch_time = 0

while True:
    # Check for incoming commands from Home Assistant
    if uart.any():
        cmd_line = uart.readline()
        if cmd_line:
            print(f"Raw UART data received: {cmd_line}")
            process_command(cmd_line)

    # Check for touch events
    if touch.Flag == 1:
        current_time = time.ticks_ms()
        # Only process touch if at least 500ms has passed since last touch
        if time.ticks_diff(current_time, last_touch_time) > 500:
            touch.Flag = 0  # Reset flag
            x = touch.X_point
            y = touch.Y_point

            # Check if touch is in button area (y: 210-240)
            if y >= 210 and y <= 240:
                print(f"Mode button touched at ({x}, {y})")
                cycle_mode()
                last_touch_time = current_time
        else:
            # Reset flag even if we ignore the touch
            touch.Flag = 0

    # Update clock display every minute if in clock mode
    if current_mode == "Clock" and time.ticks_diff(time.ticks_ms(), last_clock_update) > 60000:
        update_display_for_mode(current_mode)
        last_clock_update = time.ticks_ms()

    # Send sensor data periodically (every 10 seconds)
    if time.ticks_diff(time.ticks_ms(), last_sensor_update) > 10000:
        send_sensor_data()
        last_sensor_update = time.ticks_ms()

    time.sleep(0.1)
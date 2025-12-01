from machine import UART, Pin
from LCD_1inch28 import LCD_1inch28
import time
import json

# Initialize UART
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# Initialize display
lcd = LCD_1inch28()
lcd.set_bl_pwm(65535)  # Set brightness to maximum

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

def process_command(cmd_line):
    """Process incoming commands from Home Assistant via ESP32"""
    global current_brightness, current_mode, display_color
    
    try:
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
            
    except Exception as e:
        print(f"Error processing command: {e}")

def update_display_for_mode(mode):
    """Update display based on selected mode"""

    if mode == "Clock":
        # Black background for clock mode
        lcd.fill(lcd.black)

        # Get current time
        current_time = time.localtime()
        hour = current_time[3]
        minute = current_time[4]

        # Format time as 12-hour with AM/PM
        am_pm = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        if display_hour == 0:
            display_hour = 12
        time_str = "{:02d}:{:02d} {}".format(display_hour, minute, am_pm)

        # Display "Current Time" label
        lcd.text("Current Time", 65, 80, lcd.white)

        # Display large time (using write_text with size 3)
        lcd.write_text(time_str, 35, 110, 3, lcd.white)

    elif mode == "Sensors":
        lcd.fill(lcd.white)
        lcd.text("Sensors", 80, 80, lcd.black)
        lcd.text("Temp: 22C", 70, 110, lcd.black)
        lcd.text("Humidity: 45%", 60, 140, lcd.black)
        
    elif mode == "Weather":
        lcd.fill(lcd.white)
        lcd.text("Weather", 80, 100, lcd.black)
        lcd.text("Sunny 24C", 70, 140, lcd.black)

    elif mode == "Custom":
        lcd.fill(lcd.white)
        lcd.text("Custom Mode", 60, 120, lcd.black)
    
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

while True:
    # Check for incoming commands from Home Assistant
    if uart.any():
        cmd_line = uart.readline()
        if cmd_line:
            process_command(cmd_line)
    
    # Send sensor data periodically (every 10 seconds)
    if time.ticks_diff(time.ticks_ms(), last_sensor_update) > 10000:
        send_sensor_data()
        last_sensor_update = time.ticks_ms()
    
    time.sleep(0.1)
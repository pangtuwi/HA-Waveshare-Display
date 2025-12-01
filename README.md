# HA-Waveshare-Display

A MicroPython project for the Waveshare RP2350-Touch-LCD-1.28 display that integrates with Home Assistant via UART communication through an ESP32 bridge.

![Waveshare RP2350-Touch-LCD-1.28](https://www.waveshare.com/img/devkit/RP2350-Touch-LCD-1.28/RP2350-Touch-LCD-1.28-1.jpg)

## Hardware

**Waveshare RP2350-Touch-LCD-1.28**
- 240×240 pixel round LCD display (GC9A01 driver)
- CST816T capacitive touch controller
- QMI8658 6-axis IMU (accelerometer + gyroscope)
- RP2350B microcontroller

## Features

- **UART Communication**: Receives commands from ESP32 bridge at 115200 baud
- **Display Modes**: Clock, Sensors, Weather, Custom
- **Touch Support**: Gesture and point detection
- **Configurable**: Brightness, color, display mode via UART commands
- **Sensor Data**: Reads and reports IMU data back to Home Assistant

## Project Structure

```
.
├── main.py                      # Main application with HA integration
├── RP2350-TOUCH-LCD-1.28.py    # Hardware driver library
├── WAVESHARE_RP2350B.uf2       # MicroPython firmware
├── CLAUDE.md                    # Development documentation
└── README.md                    # This file
```

## Quick Start

### 1. Install MicroPython Firmware

1. Hold the BOOTSEL button on the RP2350
2. Connect USB cable to your computer
3. Copy `WAVESHARE_RP2350B.uf2` to the mounted drive
4. Device will reboot with MicroPython installed

### 2. Upload Project Files

Using `mpremote`:

```bash
mpremote cp main.py :
mpremote cp RP2350-TOUCH-LCD-1.28.py :LCD_1inch28.py
```

Or using `ampy`:

```bash
ampy --port /dev/ttyACM0 put main.py
ampy --port /dev/ttyACM0 put RP2350-TOUCH-LCD-1.28.py LCD_1inch28.py
```

### 3. Connect Hardware

Connect the RP2350 to your ESP32 via UART:
- RP2350 TX (Pin 0) → ESP32 RX
- RP2350 RX (Pin 1) → ESP32 TX
- GND → GND

## UART Command Protocol

Commands are line-delimited ASCII strings sent from ESP32 to RP2350:

### Display Commands

- `MSG:<text>` - Display text message
- `DISP:<data>` - Custom display text
- `CMD:CLEAR` - Clear display
- `CMD:TIME` - Show time

### Configuration Commands

- `BRIGHT:<0-100>` - Set brightness percentage
- `MODE:<mode_name>` - Set display mode (Clock/Sensors/Weather/Custom)
- `COLOR:<r>,<g>,<b>` - Set text color (RGB values)

### Sensor Responses (RP2350 to ESP32)

- `SENSOR:{json_data}` - Sends sensor data every 10 seconds

Example:
```json
{"acc_x": 0.12, "acc_y": -0.05, "acc_z": 9.81, "gyr_x": 0.0, "gyr_y": 0.0, "gyr_z": 0.0}
```

## Display Modes

- **Clock**: Shows time (requires RTC or network sync)
- **Sensors**: Displays temperature and humidity from IMU or external sensors
- **Weather**: Shows weather info (data source not yet implemented)
- **Custom**: User-defined display content

## Architecture

```
┌──────────────────┐
│ Home Assistant   │
│   (MQTT/API)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  ESP32 Bridge    │
│  (WiFi → UART)   │
└────────┬─────────┘
         │ UART 115200
         ▼
┌──────────────────┐
│   RP2350 Display │
│  (This Project)  │
└──────────────────┘
```

## Development

### Monitor Serial Output

```bash
mpremote  # Opens REPL, shows print() output
```

### Run Code Manually

```bash
mpremote run main.py
```

### Testing Commands

Send test commands via UART:

```python
# In REPL
uart.write(b'MSG:Hello World\n')
uart.write(b'BRIGHT:50\n')
uart.write(b'MODE:Sensors\n')
```

## Driver Library

The `RP2350-TOUCH-LCD-1.28.py` library provides:

### LCD_1inch28 Class
- Inherits from `framebuf.FrameBuffer` (RGB565 format)
- Methods: `show()`, `Windows_show()`, `write_text()`, `set_bl_pwm()`
- Predefined colors (note: uses BRG format internally)

### Touch_CST816T Class
- Three modes: gestures (0), point (1), mixed (2)
- Gesture types: UP, DOWN, LEFT, RIGHT, Long Press, Double Click
- Interrupt-driven touch detection

### QMI8658 Class (6-DOF IMU)
- Accelerometer range: ±8g at 1000Hz
- Gyroscope range: ±512dps at 1000Hz
- Returns 6-axis data: [acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z]

## Current Limitations

1. **Time Display**: No RTC or network time sync implemented yet
2. **Sensor Data**: IMU data available but not fully integrated into display modes
3. **ESP32 Bridge**: UART protocol defined but ESP32 code not included in this repo
4. **Home Assistant Integration**: UART protocol defined but HA configuration not included
5. **Error Handling**: Limited error feedback to Home Assistant

## Future Enhancements

- [ ] RTC or NTP time synchronization
- [ ] ESP32 bridge firmware code
- [ ] Home Assistant configuration examples
- [ ] Additional display modes and widgets
- [ ] Touch-based UI controls
- [ ] Sleep mode with wake on touch
- [ ] Over-the-air updates via ESP32

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source. Please check individual file headers for specific license information.

## Resources

- [Waveshare RP2350-Touch-LCD-1.28 Wiki](https://www.waveshare.com/wiki/RP2350-Touch-LCD-1.28)
- [MicroPython Documentation](https://docs.micropython.org/)
- [Home Assistant](https://www.home-assistant.io/)

## Acknowledgments

- Hardware drivers based on Waveshare example code
- MicroPython community for excellent documentation and support
# Buzz Lightyear Costume Controller 🚀

A Raspberry Pi-based controller for a Buzz Lightyear costume with interactive features including wing movement, LED effects, laser activation, and sound effects!

## Features

- **Wing Control**: Toggle wings between horizontal and vertical positions using a servo motor
- **Strobing LEDs**: Automatically activate strobing LED effects when wings are horizontal
- **Laser LED**: Toggle laser LED on/off with button press
- **Sound Effects**: Play sound effects for all button interactions
- **Buzz Lightyear Phrases**: Trigger random Buzz Lightyear phrases with a dedicated button

## Hardware Requirements

### Components
- Raspberry Pi (any model with GPIO pins - tested on Pi 3/4)
- Servo motor (SG90 or similar) for wing control
- LEDs:
  - Multiple LEDs for wing strobe effect
  - Single LED for laser
- 3 push buttons
- Resistors:
  - 220-330Ω resistors for LEDs
  - Optional pull-down resistors if not using internal pull-ups
- Power supply appropriate for your servo and Pi
- Speaker or audio amplifier for sound output
- Jumper wires and breadboard/prototyping board

### Wiring Diagram

#### GPIO Pin Assignments (BCM numbering)
```
Servo Signal    -> GPIO 18 (PWM0)
Strobe LEDs     -> GPIO 23
Laser LED       -> GPIO 24
Wing Button     -> GPIO 17 (with internal pull-up)
Laser Button    -> GPIO 27 (with internal pull-up)
Phrase Button   -> GPIO 22 (with internal pull-up)
```

#### Connections
1. **Servo Motor**:
   - Signal wire -> GPIO 18
   - Power (VCC) -> 5V (external power recommended for larger servos)
   - Ground -> GND

2. **LEDs**:
   - Strobe LEDs: Anode -> 220Ω resistor -> GPIO 23, Cathode -> GND
   - Laser LED: Anode -> 220Ω resistor -> GPIO 24, Cathode -> GND

3. **Buttons**:
   - One side -> GPIO pin (17, 27, or 22)
   - Other side -> GND
   - (Internal pull-up resistors are enabled in software)

4. **Audio**:
   - Connect speaker/amplifier to Pi's audio jack or HDMI audio output

## Software Installation

### 1. Clone the Repository
```bash
git clone https://github.com/porteratzo/buzz_lightyear.git
cd buzz_lightyear
```

### 2. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Add Audio Files
Place your audio files in the `audio/` directory. See `audio/README.md` for required files and format specifications.

### 4. Configure (Optional)
Copy `config_example.py` to `config.py` and modify pin assignments if needed:
```bash
cp config_example.py config.py
```

## Usage

### Running the Controller
```bash
python3 buzz_controller.py
```

### Testing
To run without actual hardware (for development):
```bash
# Install fake GPIO for testing
pip3 install fake-rpi

# Set environment variable to use fake GPIO
export FAKE_GPIO=1
python3 buzz_controller.py
```

### Controls
- **Wing Button**: Toggle wings between horizontal (with strobing LEDs) and vertical positions
- **Laser Button**: Toggle laser LED on/off
- **Phrase Button**: Play a random Buzz Lightyear phrase

### Auto-start on Boot (Optional)
To run the controller automatically when the Pi boots:

1. Create a systemd service:
```bash
sudo nano /etc/systemd/system/buzz-controller.service
```

2. Add the following content:
```ini
[Unit]
Description=Buzz Lightyear Costume Controller
After=multi-user.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/buzz_lightyear
ExecStart=/usr/bin/python3 /home/pi/buzz_lightyear/buzz_controller.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable buzz-controller.service
sudo systemctl start buzz-controller.service
```

## Configuration Options

Edit `config_example.py` (or your custom `config.py`) to adjust:

- **GPIO Pin Assignments**: Change pins to match your wiring
- **Servo Positions**: Adjust PWM duty cycles for horizontal/vertical positions
- **Strobe Frequency**: Change how fast the LEDs flash (default: 10 Hz)
- **Audio Path**: Location of sound effect files
- **Debounce Time**: Button debounce delay in milliseconds (default: 200ms)

## Troubleshooting

### Servo Not Moving
- Check servo power supply (may need external 5V power)
- Verify GPIO 18 connection
- Adjust `servo_horizontal` and `servo_vertical` values in config

### LEDs Not Working
- Check LED polarity (long leg is anode/positive)
- Verify resistor values (220-330Ω recommended)
- Test LED directly with 3.3V to confirm it works

### No Sound
- Check audio output device: `aplay -l`
- Verify audio files are in correct format (WAV)
- Test audio: `aplay audio/test.wav`
- Check speaker/amplifier connection

### Buttons Not Responding
- Verify button connections to correct GPIO pins
- Check for shorts or loose connections
- Monitor button events: add debug prints in callback functions

## Project Structure

```
buzz_lightyear/
├── buzz_controller.py      # Main controller code
├── config_example.py        # Example configuration file
├── requirements.txt         # Python dependencies
├── audio/                   # Audio files directory
│   └── README.md           # Audio file specifications
└── README.md               # This file
```

## Safety Notes

- Use appropriate resistors for LEDs to prevent burning them out
- Be careful with servo power requirements - larger servos may need external power
- Always connect ground between Pi and external power supplies
- Test individual components before assembling the full costume

## Credits

Created for controlling a Buzz Lightyear costume with Raspberry Pi.

## License

MIT License - Feel free to modify and use for your own projects!

---

**To infinity and beyond!** 🚀✨
# Project Structure and Files

## Overview
Complete Raspberry Pi-based controller for a Buzz Lightyear costume with interactive features.

## File Structure

```
buzz_lightyear/
├── README.md                 # Main documentation
├── QUICKSTART.md             # Quick start guide for beginners
├── WIRING.md                 # Detailed wiring diagrams and connections
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
│
├── buzz_controller.py        # Main controller implementation ⭐
├── config_example.py         # Configuration template
├── test_controller.py        # Test suite (no hardware needed)
├── diagnose.py              # Diagnostic and troubleshooting tool
├── example_custom.py         # Example of extending the controller
├── install.sh               # Installation script
│
└── audio/                    # Audio files directory
    └── README.md            # Audio file specifications
```

## Core Files

### buzz_controller.py ⭐
**Purpose**: Main controller implementation
**Features**:
- `BuzzController` class with complete costume control logic
- Servo motor control for wing positions
- LED control (strobing and steady)
- Button event handling with debouncing
- Audio playback system
- Threaded strobe effect for non-blocking operation
- Clean lifecycle management (init, run, cleanup)

**Key Classes**:
- `WingPosition(Enum)`: Wing state enumeration
- `BuzzController`: Main controller class

**GPIO Pins** (default):
- GPIO 18: Servo signal (PWM)
- GPIO 23: Strobe LEDs
- GPIO 24: Laser LED
- GPIO 17: Wing button
- GPIO 27: Laser button
- GPIO 22: Phrase button

### config_example.py
**Purpose**: Configuration template
**Contains**: All customizable settings for pins, timing, and audio paths
**Usage**: Copy to `config.py` and modify as needed

### test_controller.py
**Purpose**: Automated testing without hardware
**Features**:
- Mocks GPIO and pygame for testing
- Tests all core functionality
- Validates state transitions
- Can run on any Python environment

### diagnose.py
**Purpose**: Hardware and software diagnostics
**Checks**:
- Python version compatibility
- Raspberry Pi detection
- GPIO access and permissions
- pygame installation
- Audio files presence
- Audio output devices
- GPIO pin functionality (with sudo)

### example_custom.py
**Purpose**: Demonstrates how to extend the controller
**Shows**:
- Class inheritance from BuzzController
- Overriding button callbacks
- Adding custom state tracking
- Implementing custom LED patterns

## Documentation Files

### README.md
**Main documentation** covering:
- Feature overview
- Hardware requirements
- Wiring instructions
- Installation steps
- Usage guide
- Configuration options
- Troubleshooting
- Auto-start setup

### QUICKSTART.md
**Beginner-friendly guide** with:
- Step-by-step setup instructions
- System preparation
- Testing procedures
- Troubleshooting common issues
- Success checklist

### WIRING.md
**Detailed wiring guide** including:
- Pin mapping diagrams
- Component connections
- Breadboard layouts
- Power considerations
- Safety checklist
- Individual component testing

### audio/README.md
**Audio file specifications**:
- Required audio files list
- Format requirements (WAV)
- Where to find audio
- Conversion tips

## Utility Files

### install.sh
**Installation script** that:
- Checks system requirements
- Installs dependencies
- Sets up directory structure
- Creates config file
- Sets file permissions

### requirements.txt
**Python dependencies**:
- RPi.GPIO==0.7.1 (GPIO control)
- pygame==2.5.2 (Audio playback)

### .gitignore
Standard Python gitignore plus:
- `__pycache__/`
- Virtual environments
- Compiled Python files
- Build artifacts

## Feature Implementation Map

### Wing Control
**Files**: buzz_controller.py (lines 119-128)
**Components**: Servo motor, wing button
**GPIO**: Pin 18 (servo), Pin 17 (button)

### LED Strobing
**Files**: buzz_controller.py (lines 130-147)
**Components**: LED strip/multiple LEDs
**GPIO**: Pin 23
**Thread**: Separate thread for non-blocking strobe

### Laser Control
**Files**: buzz_controller.py (lines 169-180)
**Components**: Single LED
**GPIO**: Pin 24, Pin 27 (button)

### Audio Playback
**Files**: buzz_controller.py (lines 149-159)
**Components**: Speaker/amplifier
**Library**: pygame.mixer
**Files**: audio/*.wav

### Button Handling
**Files**: buzz_controller.py (lines 75-91)
**Method**: GPIO event detection with software debouncing
**Pull-up**: Internal pull-up resistors enabled

## Testing Strategy

1. **Unit Tests**: test_controller.py
   - Tests individual features
   - No hardware required
   - Fast feedback loop

2. **Diagnostics**: diagnose.py
   - Hardware checks
   - Dependency verification
   - GPIO access validation

3. **Manual Testing**: Run on actual hardware
   - Physical button presses
   - Visual LED verification
   - Audio output confirmation

## Usage Patterns

### Basic Usage
```bash
sudo python3 buzz_controller.py
```

### Testing
```bash
python3 test_controller.py
```

### Diagnostics
```bash
sudo python3 diagnose.py
```

### Custom Implementation
```bash
# Modify example_custom.py
sudo python3 example_custom.py
```

## Dependencies and Compatibility

**Python Version**: 3.7+
**Platform**: Raspberry Pi (any model with GPIO)
**OS**: Raspberry Pi OS (Raspbian)
**Libraries**: RPi.GPIO, pygame

## Development Workflow

1. **Setup**: Run install.sh
2. **Configure**: Adjust config_example.py
3. **Test**: Run test_controller.py
4. **Wire**: Follow WIRING.md
5. **Diagnose**: Run diagnose.py with sudo
6. **Deploy**: Run buzz_controller.py with sudo
7. **Customize**: Extend using example_custom.py pattern

## Security Considerations

✓ No security vulnerabilities (CodeQL verified)
✓ No hardcoded credentials
✓ Requires sudo for GPIO (proper privilege model)
✓ File operations restricted to audio directory
✓ No network operations
✓ Safe GPIO cleanup on exit

## Future Enhancement Ideas

- Add WiFi control via web interface
- Implement additional servo channels
- Add programmable LED patterns
- Support for MP3 audio files
- Configuration via web UI
- Battery level monitoring
- Multiple costume profiles

## Support and Maintenance

**Documentation**: README.md, QUICKSTART.md, WIRING.md
**Testing**: Automated tests in test_controller.py
**Diagnostics**: Built-in diagnostic script
**Examples**: Custom implementation pattern shown

---

**Created**: 2025-10-28
**License**: MIT
**Status**: Production Ready ✓

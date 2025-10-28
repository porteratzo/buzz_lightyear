# Quick Start Guide

Get your Buzz Lightyear costume up and running in minutes!

## 🚀 Super Quick Start

If you're experienced with Raspberry Pi:

```bash
git clone https://github.com/porteratzo/buzz_lightyear.git
cd buzz_lightyear
./install.sh
# Add your audio files to the audio/ directory
sudo python3 buzz_controller.py
```

## 📋 Step-by-Step Guide for Beginners

### Step 1: Set Up Your Raspberry Pi

1. **Get a Raspberry Pi** (Model 3 or 4 recommended)
2. **Install Raspberry Pi OS** (formerly Raspbian)
   - Download from: https://www.raspberrypi.com/software/
   - Flash to SD card using Raspberry Pi Imager
3. **Boot up** and complete initial setup
4. **Connect to internet** (WiFi or Ethernet)

### Step 2: Update Your System

Open a terminal and run:
```bash
sudo apt-get update
sudo apt-get upgrade
```

### Step 3: Download the Project

```bash
cd ~
git clone https://github.com/porteratzo/buzz_lightyear.git
cd buzz_lightyear
```

### Step 4: Run Installation Script

```bash
./install.sh
```

This installs all required software packages.

### Step 5: Add Audio Files

1. **Get or create audio files** (see `audio/README.md` for details)
2. **Copy them to the audio folder**:
   ```bash
   cp /path/to/your/sounds/*.wav audio/
   ```

Required files:
- `wings_open.wav`
- `wings_close.wav`
- `laser_on.wav`
- `laser_off.wav`
- `to_infinity.wav`
- `buzz_lightyear.wav`
- `not_flying.wav`
- `space_ranger.wav`

### Step 6: Wire Up Hardware

Follow the diagrams in `WIRING.md`. Basic connections:

**Minimum setup to test:**
- 1 button on GPIO 17 (wing button)
- 1 LED on GPIO 23 (strobe LED)

**Full setup:**
- 3 buttons (GPIO 17, 27, 22)
- 2 LEDs (GPIO 23, 24)
- 1 servo motor (GPIO 18)
- Speaker connected to audio jack

### Step 7: Test Your Setup

Run the test script first (no GPIO needed):
```bash
python3 test_controller.py
```

If all tests pass, you're ready!

### Step 8: Run the Controller

**Important**: You need sudo to access GPIO pins:
```bash
sudo python3 buzz_controller.py
```

### Step 9: Try It Out!

- Press the **wing button** (GPIO 17) to toggle wings and strobe
- Press the **laser button** (GPIO 27) to toggle laser
- Press the **phrase button** (GPIO 22) to hear Buzz speak!

### Step 10: Make It Auto-Start (Optional)

To run automatically when the Pi boots:

1. Edit the systemd service file path in README.md section
2. Follow the "Auto-start on Boot" instructions
3. Your costume will be ready to go whenever you power on!

## 🔧 Troubleshooting

### "Permission denied" error
- Always use `sudo` when running the controller
- Example: `sudo python3 buzz_controller.py`

### No sound
```bash
# Test audio output
speaker-test -t wav -c 2
# Or try playing a file
aplay audio/to_infinity.wav
```

### Servo doesn't move
- Check your power supply (servo may need more power)
- Try external 5V power source for the servo
- Verify GPIO 18 connection

### Button doesn't work
- Check wiring (button between GPIO and GND)
- Verify GPIO pin numbers match your config
- Test button with multimeter

### "Module not found" errors
```bash
# Reinstall dependencies
pip3 install -r requirements.txt

# For GPIO
sudo apt-get install python3-rpi.gpio
```

## 💡 Tips

1. **Start Simple**: Test one component at a time
2. **Check Connections**: Loose wires are the #1 issue
3. **Use a Breadboard**: Makes testing and changes easier
4. **Label Wires**: Helps prevent mistakes
5. **External Power**: Servos work better with external 5V supply
6. **Test Audio First**: Make sure speakers work before integrating

## 📱 Getting Help

If you're stuck:

1. Check `README.md` for detailed documentation
2. Review `WIRING.md` for connection diagrams
3. Read `audio/README.md` for audio file setup
4. Run `python3 test_controller.py` to test without hardware

## 🎯 Success Checklist

- [ ] Raspberry Pi set up and updated
- [ ] Project downloaded and installed
- [ ] Audio files in place
- [ ] Hardware wired according to diagram
- [ ] Test script passes
- [ ] Controller runs with sudo
- [ ] Buttons respond to presses
- [ ] LEDs light up
- [ ] Servo moves
- [ ] Sound plays

## 🌟 You Did It!

Congratulations! Your Buzz Lightyear costume is now operational!

**To infinity and beyond!** 🚀✨

---

*Need more details? See README.md for complete documentation*

#!/usr/bin/env python3
"""
Diagnostic script for Buzz Lightyear Controller

This script helps diagnose hardware and software issues.
Run with: sudo python3 diagnose.py
"""

import sys
import os
import subprocess

def print_header(text):
    """Print a section header"""
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50)

def check_python_version():
    """Check Python version"""
    print_header("Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 7:
        print("✓ Python version is compatible")
        return True
    else:
        print("✗ Python 3.7 or higher required")
        return False

def check_running_on_pi():
    """Check if running on Raspberry Pi"""
    print_header("Hardware Check")
    try:
        with open('/proc/cpuinfo', 'r') as f:
            if 'Raspberry Pi' in f.read():
                print("✓ Running on Raspberry Pi")
                return True
            else:
                print("⚠️  Not running on Raspberry Pi (GPIO won't work)")
                return False
    except:
        print("⚠️  Cannot determine hardware")
        return False

def check_gpio_access():
    """Check if GPIO can be accessed"""
    print_header("GPIO Access")
    try:
        import RPi.GPIO as GPIO
        print("✓ RPi.GPIO module imported successfully")
        
        # Check if running with sudo
        if os.geteuid() != 0:
            print("⚠️  Not running as root (use sudo)")
            return False
        else:
            print("✓ Running with sudo/root privileges")
            return True
    except ImportError:
        print("✗ RPi.GPIO module not found")
        print("  Install with: sudo apt-get install python3-rpi.gpio")
        return False
    except Exception as e:
        print(f"✗ Error accessing GPIO: {e}")
        return False

def check_pygame():
    """Check pygame installation"""
    print_header("Audio System (pygame)")
    try:
        import pygame
        print("✓ pygame module imported successfully")
        
        pygame.mixer.init()
        print("✓ pygame mixer initialized")
        pygame.mixer.quit()
        return True
    except ImportError:
        print("✗ pygame module not found")
        print("  Install with: pip3 install pygame")
        return False
    except Exception as e:
        print(f"⚠️  pygame found but error initializing: {e}")
        return False

def check_audio_files():
    """Check if audio files exist"""
    print_header("Audio Files")
    
    required_files = [
        'wings_open.wav',
        'wings_close.wav',
        'laser_on.wav',
        'laser_off.wav',
        'to_infinity.wav',
        'buzz_lightyear.wav',
        'not_flying.wav',
        'space_ranger.wav'
    ]
    
    audio_path = 'audio'
    missing = []
    
    if not os.path.exists(audio_path):
        print(f"✗ Audio directory '{audio_path}' not found")
        return False
    
    for filename in required_files:
        filepath = os.path.join(audio_path, filename)
        if os.path.exists(filepath):
            print(f"✓ {filename}")
        else:
            print(f"✗ {filename} - MISSING")
            missing.append(filename)
    
    if missing:
        print(f"\n⚠️  {len(missing)} audio file(s) missing")
        print("  See audio/README.md for details")
        return False
    else:
        print("\n✓ All required audio files present")
        return True

def check_audio_output():
    """Check audio output devices"""
    print_header("Audio Output Devices")
    try:
        result = subprocess.run(['aplay', '-l'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(result.stdout)
            print("✓ Audio devices found")
            return True
        else:
            print("⚠️  No audio devices found")
            return False
    except FileNotFoundError:
        print("⚠️  'aplay' command not found")
        return False
    except Exception as e:
        print(f"⚠️  Error checking audio: {e}")
        return False

def test_gpio_pins():
    """Test GPIO pin access"""
    print_header("GPIO Pin Test")
    
    if os.geteuid() != 0:
        print("⚠️  Skipping (requires sudo)")
        return False
    
    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Test LED pin
        test_pin = 23
        print(f"Testing GPIO {test_pin} (LED)...")
        GPIO.setup(test_pin, GPIO.OUT)
        GPIO.output(test_pin, GPIO.HIGH)
        print(f"✓ GPIO {test_pin} set HIGH")
        
        import time
        time.sleep(0.5)
        
        GPIO.output(test_pin, GPIO.LOW)
        print(f"✓ GPIO {test_pin} set LOW")
        
        GPIO.cleanup()
        print("✓ GPIO test passed")
        return True
        
    except Exception as e:
        print(f"✗ GPIO test failed: {e}")
        return False

def check_dependencies():
    """Check all Python dependencies"""
    print_header("Python Dependencies")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip() for line in f if line.strip()]
        
        for req in requirements:
            package = req.split('==')[0].split('>=')[0]
            try:
                __import__(package.replace('-', '_'))
                print(f"✓ {package}")
            except ImportError:
                print(f"✗ {package} - NOT INSTALLED")
        return True
    except FileNotFoundError:
        print("⚠️  requirements.txt not found")
        return False

def main():
    """Run all diagnostics"""
    print("\n" + "🔍" * 25)
    print("  Buzz Lightyear Controller Diagnostics")
    print("🔍" * 25)
    
    results = []
    
    results.append(("Python Version", check_python_version()))
    results.append(("Hardware Check", check_running_on_pi()))
    results.append(("GPIO Access", check_gpio_access()))
    results.append(("pygame", check_pygame()))
    results.append(("Audio Files", check_audio_files()))
    results.append(("Audio Output", check_audio_output()))
    results.append(("Dependencies", check_dependencies()))
    
    if os.geteuid() == 0:
        results.append(("GPIO Pin Test", test_gpio_pins()))
    
    # Summary
    print_header("Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:20s} {status}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Ready to launch!")
        print("   Run: sudo python3 buzz_controller.py")
    else:
        print("\n⚠️  Some checks failed. Review the output above.")
        print("   See README.md and TROUBLESHOOTING for help")
    
    print("\nTo infinity and beyond! 🚀")

if __name__ == '__main__':
    main()

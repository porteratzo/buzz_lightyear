#!/usr/bin/env python3
"""
Test script for Buzz Lightyear Controller (without hardware)

This script simulates button presses to test the controller logic
without requiring actual GPIO hardware.
"""

import time
import sys
from unittest.mock import Mock, MagicMock, patch
import threading

# Mock RPi.GPIO before importing buzz_controller
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()

# Mock pygame
sys.modules['pygame'] = MagicMock()
sys.modules['pygame.mixer'] = MagicMock()

# Now import the controller
from buzz_controller import BuzzController, WingPosition

class TestBuzzController:
    """Test harness for BuzzController"""
    
    def __init__(self):
        print("Initializing test controller...")
        
        # Create controller with test config
        self.controller = BuzzController({
            'servo_pin': 18,
            'strobe_led_pin': 23,
            'laser_led_pin': 24,
            'wing_button_pin': 17,
            'laser_button_pin': 27,
            'phrase_button_pin': 22,
            'servo_horizontal': 5.0,
            'servo_vertical': 10.0,
            'strobe_frequency': 10,
            'audio_path': 'audio',
            'debounce_time': 200
        })
        
        print("Test controller initialized successfully!")
    
    def test_wing_toggle(self):
        """Test wing position toggle"""
        print("\n--- Testing Wing Toggle ---")
        
        # Initial state should be vertical
        assert self.controller.wing_position == WingPosition.VERTICAL, "Initial wing position should be vertical"
        print("✓ Initial position: VERTICAL")
        
        # Simulate wing button press (horizontal)
        print("Simulating wing button press (open wings)...")
        self.controller._wing_button_callback(None)
        assert self.controller.wing_position == WingPosition.HORIZONTAL, "Wing position should be horizontal"
        assert self.controller.strobe_running, "Strobe should be running"
        print("✓ Wings opened: HORIZONTAL, Strobe: ON")
        
        time.sleep(0.5)
        
        # Simulate wing button press again (vertical)
        print("Simulating wing button press (close wings)...")
        self.controller._wing_button_callback(None)
        assert self.controller.wing_position == WingPosition.VERTICAL, "Wing position should be vertical"
        assert not self.controller.strobe_running, "Strobe should be stopped"
        print("✓ Wings closed: VERTICAL, Strobe: OFF")
    
    def test_laser_toggle(self):
        """Test laser toggle"""
        print("\n--- Testing Laser Toggle ---")
        
        # Initial state should be off
        assert not self.controller.laser_on, "Laser should be off initially"
        print("✓ Initial laser state: OFF")
        
        # Turn laser on
        print("Simulating laser button press (turn on)...")
        self.controller._laser_button_callback(None)
        assert self.controller.laser_on, "Laser should be on"
        print("✓ Laser turned: ON")
        
        # Turn laser off
        print("Simulating laser button press (turn off)...")
        self.controller._laser_button_callback(None)
        assert not self.controller.laser_on, "Laser should be off"
        print("✓ Laser turned: OFF")
    
    def test_phrase_button(self):
        """Test phrase button"""
        print("\n--- Testing Phrase Button ---")
        
        print("Simulating phrase button press...")
        self.controller._phrase_button_callback(None)
        print("✓ Phrase played successfully")
    
    def test_strobe_timing(self):
        """Test strobe LED timing"""
        print("\n--- Testing Strobe Timing ---")
        
        print("Starting strobe...")
        self.controller._start_strobe()
        assert self.controller.strobe_running, "Strobe should be running"
        print("✓ Strobe started")
        
        # Let it run for a bit
        time.sleep(1.0)
        
        print("Stopping strobe...")
        self.controller._stop_strobe()
        assert not self.controller.strobe_running, "Strobe should be stopped"
        print("✓ Strobe stopped")
    
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 50)
        print("Starting Buzz Lightyear Controller Tests")
        print("=" * 50)
        
        try:
            self.test_wing_toggle()
            self.test_laser_toggle()
            self.test_phrase_button()
            self.test_strobe_timing()
            
            print("\n" + "=" * 50)
            print("ALL TESTS PASSED! ✓")
            print("=" * 50)
            return True
            
        except AssertionError as e:
            print(f"\n✗ TEST FAILED: {e}")
            return False
        except Exception as e:
            print(f"\n✗ UNEXPECTED ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # Cleanup
            self.controller.running = False
            self.controller._stop_strobe()
            print("\nCleanup complete")

def main():
    """Main test runner"""
    tester = TestBuzzController()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

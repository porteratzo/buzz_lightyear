#!/usr/bin/env python3
"""
Buzz Lightyear Costume Controller
Main controller for Raspberry Pi-based Buzz Lightyear costume with:
- Servo control for wings (horizontal/vertical)
- LED control (strobing and laser)
- Button inputs with sound effects
- Audio playback for phrases and effects
"""

import RPi.GPIO as GPIO
import time
import pygame
import os
from enum import Enum
from threading import Thread, Event

class WingPosition(Enum):
    """Wing position states"""
    HORIZONTAL = 0
    VERTICAL = 1

class BuzzController:
    """Main controller for Buzz Lightyear costume"""
    
    def __init__(self, config=None):
        """
        Initialize the Buzz Lightyear controller
        
        Args:
            config: Dictionary with pin configurations and settings
        """
        # Default configuration
        self.config = config or {
            'servo_pin': 18,          # GPIO pin for servo control
            'strobe_led_pin': 23,     # GPIO pin for strobing LEDs
            'laser_led_pin': 24,      # GPIO pin for laser LED
            'wing_button_pin': 17,    # GPIO pin for wing toggle button
            'laser_button_pin': 27,   # GPIO pin for laser button
            'phrase_button_pin': 22,  # GPIO pin for phrase button
            'servo_horizontal': 5.0,  # PWM duty cycle for horizontal (0 degrees)
            'servo_vertical': 10.0,   # PWM duty cycle for vertical (90 degrees)
            'strobe_frequency': 10,   # Strobe flashes per second
            'audio_path': 'audio',    # Path to audio files
            'debounce_time': 200      # Button debounce time in ms
        }
        
        # Initialize state
        self.wing_position = WingPosition.VERTICAL
        self.laser_on = False
        self.strobe_running = False
        self.running = True
        
        # Threading events for strobe control
        self.strobe_event = Event()
        self.strobe_thread = None
        
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup servo
        GPIO.setup(self.config['servo_pin'], GPIO.OUT)
        self.servo_pwm = GPIO.PWM(self.config['servo_pin'], 50)  # 50Hz for servo
        self.servo_pwm.start(0)
        
        # Setup LEDs
        GPIO.setup(self.config['strobe_led_pin'], GPIO.OUT)
        GPIO.setup(self.config['laser_led_pin'], GPIO.OUT)
        GPIO.output(self.config['strobe_led_pin'], GPIO.LOW)
        GPIO.output(self.config['laser_led_pin'], GPIO.LOW)
        
        # Setup buttons with pull-up resistors
        GPIO.setup(self.config['wing_button_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.config['laser_button_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.config['phrase_button_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Initialize pygame mixer for audio
        pygame.mixer.init()
        
        # Add button event detection
        GPIO.add_event_detect(
            self.config['wing_button_pin'],
            GPIO.FALLING,
            callback=self._wing_button_callback,
            bouncetime=self.config['debounce_time']
        )
        GPIO.add_event_detect(
            self.config['laser_button_pin'],
            GPIO.FALLING,
            callback=self._laser_button_callback,
            bouncetime=self.config['debounce_time']
        )
        GPIO.add_event_detect(
            self.config['phrase_button_pin'],
            GPIO.FALLING,
            callback=self._phrase_button_callback,
            bouncetime=self.config['debounce_time']
        )
        
        # Initialize wing position to vertical
        self._set_servo_position(WingPosition.VERTICAL)
        
        print("Buzz Lightyear Controller initialized")
    
    def _set_servo_position(self, position):
        """Set servo to specified wing position"""
        if position == WingPosition.HORIZONTAL:
            duty_cycle = self.config['servo_horizontal']
        else:
            duty_cycle = self.config['servo_vertical']
        
        self.servo_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)  # Give servo time to move
        self.servo_pwm.ChangeDutyCycle(0)  # Stop sending signal to prevent jitter
    
    def _start_strobe(self):
        """Start the LED strobe effect"""
        if not self.strobe_running:
            self.strobe_running = True
            self.strobe_event.clear()
            self.strobe_thread = Thread(target=self._strobe_loop)
            self.strobe_thread.start()
    
    def _stop_strobe(self):
        """Stop the LED strobe effect"""
        if self.strobe_running:
            self.strobe_running = False
            self.strobe_event.set()
            if self.strobe_thread:
                self.strobe_thread.join()
            GPIO.output(self.config['strobe_led_pin'], GPIO.LOW)
    
    def _strobe_loop(self):
        """Strobe LED loop running in separate thread"""
        period = 1.0 / self.config['strobe_frequency']
        half_period = period / 2
        
        while self.strobe_running and not self.strobe_event.is_set():
            GPIO.output(self.config['strobe_led_pin'], GPIO.HIGH)
            time.sleep(half_period)
            GPIO.output(self.config['strobe_led_pin'], GPIO.LOW)
            time.sleep(half_period)
    
    def _play_sound(self, sound_file):
        """Play a sound effect"""
        sound_path = os.path.join(self.config['audio_path'], sound_file)
        if os.path.exists(sound_path):
            try:
                sound = pygame.mixer.Sound(sound_path)
                sound.play()
            except Exception as e:
                print(f"Error playing sound {sound_file}: {e}")
        else:
            print(f"Sound file not found: {sound_path}")
    
    def _wing_button_callback(self, channel):
        """Handle wing toggle button press"""
        # Toggle wing position
        if self.wing_position == WingPosition.VERTICAL:
            self.wing_position = WingPosition.HORIZONTAL
            self._set_servo_position(WingPosition.HORIZONTAL)
            self._start_strobe()
            self._play_sound('wings_open.wav')
            print("Wings: HORIZONTAL - Strobe ON")
        else:
            self.wing_position = WingPosition.VERTICAL
            self._set_servo_position(WingPosition.VERTICAL)
            self._stop_strobe()
            self._play_sound('wings_close.wav')
            print("Wings: VERTICAL - Strobe OFF")
    
    def _laser_button_callback(self, channel):
        """Handle laser button press"""
        # Toggle laser
        self.laser_on = not self.laser_on
        GPIO.output(self.config['laser_led_pin'], GPIO.HIGH if self.laser_on else GPIO.LOW)
        
        if self.laser_on:
            self._play_sound('laser_on.wav')
            print("Laser: ON")
        else:
            self._play_sound('laser_off.wav')
            print("Laser: OFF")
    
    def _phrase_button_callback(self, channel):
        """Handle phrase button press"""
        # Play a random Buzz Lightyear phrase
        phrases = [
            'to_infinity.wav',
            'buzz_lightyear.wav',
            'not_flying.wav',
            'space_ranger.wav'
        ]
        
        # Select a random phrase
        import random
        phrase = random.choice(phrases)
        self._play_sound(phrase)
        print(f"Playing phrase: {phrase}")
    
    def run(self):
        """Main run loop - keep program alive"""
        print("Buzz Lightyear Controller running...")
        print("Press Ctrl+C to exit")
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up GPIO and resources"""
        print("Cleaning up...")
        self.running = False
        self._stop_strobe()
        self.servo_pwm.stop()
        GPIO.cleanup()
        pygame.mixer.quit()
        print("Cleanup complete")

def main():
    """Main entry point"""
    controller = BuzzController()
    controller.run()

if __name__ == '__main__':
    main()

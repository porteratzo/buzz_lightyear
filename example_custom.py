#!/usr/bin/env python3
"""
Advanced example: Customizing the Buzz Controller

This example shows how to extend the base controller with custom features.
"""

from buzz_controller import BuzzController, WingPosition
import time

class CustomBuzzController(BuzzController):
    """Extended controller with custom features"""
    
    def __init__(self, config=None):
        super().__init__(config)
        
        # Add custom state
        self.activation_count = 0
        self.easter_egg_triggered = False
    
    def _wing_button_callback(self, channel):
        """Override wing button with counter"""
        # Call parent implementation
        super()._wing_button_callback(channel)
        
        # Add custom behavior
        self.activation_count += 1
        print(f"Wing activation count: {self.activation_count}")
        
        # Easter egg: after 10 activations, play special sound
        if self.activation_count == 10 and not self.easter_egg_triggered:
            self.easter_egg_triggered = True
            self._play_sound('easter_egg.wav')
            print("🎉 Easter egg unlocked!")
    
    def _phrase_button_callback(self, channel):
        """Override phrase button for sequential phrases"""
        # Cycle through phrases in order instead of random
        phrases = [
            'to_infinity.wav',
            'buzz_lightyear.wav',
            'not_flying.wav',
            'space_ranger.wav'
        ]
        
        if not hasattr(self, 'phrase_index'):
            self.phrase_index = 0
        
        phrase = phrases[self.phrase_index]
        self._play_sound(phrase)
        print(f"Playing phrase {self.phrase_index + 1}/{len(phrases)}: {phrase}")
        
        # Move to next phrase
        self.phrase_index = (self.phrase_index + 1) % len(phrases)
    
    def custom_strobe_pattern(self):
        """Example: Different strobe pattern"""
        import RPi.GPIO as GPIO
        
        print("Activating custom strobe pattern...")
        
        # Stop default strobe
        self._stop_strobe()
        
        # Custom pattern: 3 quick flashes
        for _ in range(3):
            self._play_sound('beep.wav')
            for __ in range(3):
                GPIO.output(self.config['strobe_led_pin'], GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(self.config['strobe_led_pin'], GPIO.LOW)
                time.sleep(0.1)
            time.sleep(0.5)

# Example configuration with custom settings
CUSTOM_CONFIG = {
    'servo_pin': 18,
    'strobe_led_pin': 23,
    'laser_led_pin': 24,
    'wing_button_pin': 17,
    'laser_button_pin': 27,
    'phrase_button_pin': 22,
    'servo_horizontal': 4.0,    # Different position
    'servo_vertical': 11.0,     # Different position
    'strobe_frequency': 15,     # Faster strobe
    'audio_path': 'audio',
    'debounce_time': 300        # Longer debounce
}

def main():
    """Run the custom controller"""
    print("Starting Custom Buzz Controller...")
    
    # Create custom controller
    controller = CustomBuzzController(CUSTOM_CONFIG)
    
    # Run it
    controller.run()

if __name__ == '__main__':
    main()

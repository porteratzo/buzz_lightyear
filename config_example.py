"""
Configuration file for Buzz Lightyear Controller

Copy this file to config.py and modify as needed for your hardware setup.
"""

# GPIO Pin Configuration (BCM numbering)
CONFIG = {
    # Servo control
    'servo_pin': 18,              # GPIO18 (PWM0) for servo signal
    
    # LED pins
    'strobe_led_pin': 23,         # GPIO23 for wing strobe LEDs
    'laser_led_pin': 24,          # GPIO24 for laser LED
    
    # Button pins (active LOW with pull-up resistors)
    'wing_button_pin': 17,        # GPIO17 for wing toggle button
    'laser_button_pin': 27,       # GPIO27 for laser toggle button
    'phrase_button_pin': 22,      # GPIO22 for phrase button
    
    # Servo settings (PWM duty cycle percentages for 50Hz)
    'servo_horizontal': 5.0,      # Duty cycle for horizontal position (0°)
    'servo_vertical': 10.0,       # Duty cycle for vertical position (90°)
    
    # LED settings
    'strobe_frequency': 10,       # Strobe flashes per second
    
    # Audio settings
    'audio_path': 'audio',        # Directory containing audio files
    
    # Button settings
    'debounce_time': 200          # Button debounce time in milliseconds
}

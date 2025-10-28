# Wiring Diagram for Buzz Lightyear Costume Controller

## Component Layout

```
                                RASPBERRY PI
                        +-------------------------+
                        |                         |
                        |  (3V3)  1  2  (5V)     |
                        |         3  4  (5V)     |
                        |         5  6  (GND)    |
                        |         7  8           |
                        |  (GND)  9 10           |
    Wing Button    -----|> GPIO17 11 12  GPIO18 >|----- Servo Signal (Orange/Yellow)
                        |         13 14  (GND)   |
                        |         15 16           |
                        |  (3V3) 17 18           |
                        |         19 20  (GND)   |
                        |         21 22  GPIO22 >|----- Phrase Button
   Strobe LEDs     -----|< GPIO23 23 24  GPIO24 >|----- Laser LED
                        |  (GND) 25 26           |
   Laser Button    -----|> GPIO27 27 28           |
                        |         29 30  (GND)   |
                        |         31 32           |
                        |         33 34  (GND)   |
                        |         35 36           |
                        |         37 38           |
                        |  (GND) 39 40           |
                        +-------------------------+

Legend:
  >  = Output
  <  = Output (LED)
  >| = Input (Button)
```

## Detailed Connections

### 1. Servo Motor (SG90 or similar)
```
Servo Wire Color    Connection
----------------    ----------
Brown/Black         GND (Pin 6, 9, 14, 20, 25, 30, 34, or 39)
Red                 5V (Pin 2 or 4) *Use external 5V for larger servos
Orange/Yellow       GPIO 18 (Pin 12) - PWM Signal
```

### 2. Wing Button
```
Button Terminal     Connection
---------------     ----------
Terminal 1          GPIO 17 (Pin 11)
Terminal 2          GND (any GND pin)

Note: Internal pull-up resistor enabled in software
```

### 3. Laser Button
```
Button Terminal     Connection
---------------     ----------
Terminal 1          GPIO 27 (Pin 13)
Terminal 2          GND (any GND pin)

Note: Internal pull-up resistor enabled in software
```

### 4. Phrase Button
```
Button Terminal     Connection
---------------     ----------
Terminal 1          GPIO 22 (Pin 15)
Terminal 2          GND (any GND pin)

Note: Internal pull-up resistor enabled in software
```

### 5. Strobe LEDs (can be multiple LEDs in parallel)
```
Component           Connection
---------           ----------
LED Anode (+)  -->  220Ω Resistor  -->  GPIO 23 (Pin 16)
LED Cathode (-) --> GND (any GND pin)

Note: For multiple LEDs, use parallel connection with one resistor per LED
```

### 6. Laser LED
```
Component           Connection
---------           ----------
LED Anode (+)  -->  220Ω Resistor  -->  GPIO 24 (Pin 18)
LED Cathode (-) --> GND (any GND pin)
```

### 7. Audio Output
```
Connection          Description
----------          -----------
3.5mm Jack          Pi's audio jack to speaker/amplifier
or HDMI             HDMI audio output to TV/monitor speakers
or USB              USB audio adapter
```

## Breadboard Layout Example

```
        +5V  GND                                        +3.3V  GND
         |    |                                           |     |
         |    |    [Servo Motor]                         |     |
    +----|----|----|-----|----+                     +----|-----|----+
    |    |    |    |     |    |                     |    |     |    |
    |   Red  Brn  Org    |    |                     |   Btn1  Btn2 |
    |    |    |    |     |    |                     |    |     |    |
    |    |    |    |     |    |                     |   Wing  Laser|
    |    +----+    |     |    |                     |    |     |    |
    |         |    |     |    |                     |    |     |    |
    |        GND   |     |    |                     |   GPIO17 GPIO27
    |              |     |    |                     |          |    |
    |            GPIO18  |    |                     |          +----+
    |                    |    |                     |               |
    |        [LEDs]      |    |                     |              GND
    |                    |    |                     |
    |  Strobe  Laser     |    |                     |    [Button 3]
    |    |      |        |    |                     |       |
    |   LED    LED       |    |                     |     Phrase
    |    |      |        |    |                     |       |
    |   220Ω   220Ω      |    |                     |     GPIO22
    |    |      |        |    |                     |       |
    |  GPIO23 GPIO24     |    |                     |      GND
    |    |      |        |    |
    +----+------+--------+----+
         |      |
        GND    GND
```

## Power Considerations

1. **Raspberry Pi Power**: Use a good quality 5V 2.5A-3A power supply
2. **Servo Power**: Small servos (SG90) can run from Pi's 5V, but larger servos should use external 5V power supply
3. **LED Current**: Each LED draws ~20mA, ensure total doesn't exceed GPIO limits (16mA per pin safe limit)
   - For high-power LEDs, use transistor/MOSFET switching circuit
4. **Common Ground**: If using external power supply for servo, connect grounds together

## Safety Checklist

- [ ] All connections secure with no loose wires
- [ ] LED polarity correct (long leg to resistor/GPIO)
- [ ] Resistors in series with all LEDs
- [ ] Buttons connected between GPIO and GND
- [ ] Servo power adequate (external supply if needed)
- [ ] Common ground between Pi and external power
- [ ] No short circuits
- [ ] Test individual components before connecting all

## Testing Individual Components

1. **Test Servo**: 
   ```bash
   python3 -c "import RPi.GPIO as GPIO; import time; GPIO.setmode(GPIO.BCM); GPIO.setup(18, GPIO.OUT); p=GPIO.PWM(18,50); p.start(7.5); time.sleep(2); p.stop(); GPIO.cleanup()"
   ```

2. **Test LED**:
   ```bash
   python3 -c "import RPi.GPIO as GPIO; import time; GPIO.setmode(GPIO.BCM); GPIO.setup(23, GPIO.OUT); GPIO.output(23, GPIO.HIGH); time.sleep(2); GPIO.output(23, GPIO.LOW); GPIO.cleanup()"
   ```

3. **Test Button**:
   ```bash
   python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP); print('Button state:', GPIO.input(17)); GPIO.cleanup()"
   ```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Servo jitters | Add capacitor across power lines, use external power |
| LED too dim | Reduce resistor value (but not below 220Ω for 3.3V) |
| Button not detected | Check wiring, verify pull-up resistor enabled |
| No sound | Check audio device, test with `speaker-test -t wav` |
| Pi crashes | Check power supply quality and amperage |

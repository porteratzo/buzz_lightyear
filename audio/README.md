# Audio Files

This directory should contain the sound effect files for the Buzz Lightyear costume.

## Required Audio Files

The following audio files should be placed in this directory (in WAV format):

### Wing Sound Effects
- `wings_open.wav` - Sound played when wings open to horizontal position
- `wings_close.wav` - Sound played when wings close to vertical position

### Laser Sound Effects
- `laser_on.wav` - Sound played when laser is activated
- `laser_off.wav` - Sound played when laser is deactivated

### Buzz Lightyear Phrases
- `to_infinity.wav` - "To infinity and beyond!"
- `buzz_lightyear.wav` - "Buzz Lightyear to the rescue!"
- `not_flying.wav` - "That wasn't flying, that was falling with style!"
- `space_ranger.wav` - "Space Ranger, Buzz Lightyear!"

## Audio Format

All audio files should be in WAV format for best compatibility with pygame.mixer.

You can convert audio files to WAV format using tools like:
- ffmpeg: `ffmpeg -i input.mp3 output.wav`
- audacity: Export as WAV
- online converters

## Finding Audio Files

You can source audio files from:
1. Record your own voice acting
2. Extract from Toy Story movies (for personal use only)
3. Find free sound effects online from sites like:
   - freesound.org
   - zapsplat.com
   - soundbible.com

## Tips

- Keep file sizes reasonable (under 1MB each) for faster loading
- Use mono audio at 22050Hz or 44100Hz sample rate
- Normalize volume levels across all files
- Test each sound effect to ensure proper volume and duration

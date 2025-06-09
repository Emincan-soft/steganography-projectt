# Audio Masking & Filtering Steganography

This folder demonstrates how to hide and extract a 160-character message in a WAV audio file using masking and filtering techniques.

## Algorithm Overview
This method hides data in the high-frequency (masked) regions of the audio signal, where the human ear is less sensitive. By embedding message bits in these regions, the secret data becomes less perceptible.

## Usage
- Use `masking_audio_steganography.py` to encode or decode a message in a WAV file.
- Example input file: `input.wav`

### Encoding a Message
```bash
python masking_audio_steganography.py --encode --infile input.wav --outfile output.wav --message "Your secret message here!"
```

### Decoding a Message
```bash
python masking_audio_steganography.py --decode --infile output.wav
```

## Requirements
- Python 3.x
- numpy
- scipy

Install dependencies with:
```bash
pip install numpy scipy
```

## Notes
- Works best with 16-bit PCM WAV files.
- The message is limited to 160 characters for this project.
- The script is for educational purposes and is well-commented for learning. 
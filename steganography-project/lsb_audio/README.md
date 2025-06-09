# LSB Audio Steganography (Least Significant Bit)

This folder demonstrates how to hide and extract a 160-character message in a WAV audio file using the LSB (Least Significant Bit) algorithm.

## Algorithm Overview
The LSB algorithm hides data by replacing the least significant bit of each audio sample with the message bits. This change is usually inaudible to the human ear, making it a simple but effective steganography technique for uncompressed audio files.

## Usage
- Use `lsb_audio_steganography.py` to encode or decode a message in a WAV file.
- Example input file: `input.wav`

### Encoding a Message
```bash
python lsb_audio_steganography.py --encode --infile input.wav --outfile output.wav --message "Your secret message here!"
```

### Decoding a Message
```bash
python lsb_audio_steganography.py --decode --infile output.wav
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
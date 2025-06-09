# Heuristic Video Steganography

This folder demonstrates how to hide and extract a 160-character message in an MP4 video file using a simple heuristic steganography method.

## Algorithm Overview
A basic heuristic approach is used: the least significant bit (LSB) of the blue channel of the top-left pixel in each video frame is used to store one bit of the message. This method is simple and designed for educational purposes, showing how video frames can be used for steganography.

## Usage
- Use `heuristic_steganography.py` to encode or decode a message in an MP4 file.
- Example input file: `input.mp4`

### Encoding a Message
```bash
python heuristic_steganography.py --encode --infile input.mp4 --outfile output.mp4 --message "Your secret message here!"
```

### Decoding a Message
```bash
python heuristic_steganography.py --decode --infile output.mp4
```

## Requirements
- Python 3.x
- numpy
- opencv-python

Install dependencies with:
```bash
pip install numpy opencv-python
```

## Notes
- Works best with short MP4 videos.
- The message is limited to 160 characters for this project.
- The script is for educational purposes and is well-commented for learning. 
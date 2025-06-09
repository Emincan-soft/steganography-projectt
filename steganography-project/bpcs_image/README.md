# BPCS Image Steganography (Bit Plane Complexity Segmentation)

This folder demonstrates how to hide and extract a 160-character message in a PNG image using the BPCS (Bit Plane Complexity Segmentation) algorithm.

## Algorithm Overview
BPCS steganography hides data in the complex regions of an image's bit planes. Blocks with high complexity (many transitions between 0 and 1) are suitable for embedding data, as changes are less noticeable to the human eye.

## Usage
- Use `bpcs_steganography.py` to encode or decode a message in a PNG file.
- Example input file: `input.png`

### Encoding a Message
```bash
python bpcs_steganography.py --encode --infile input.png --outfile output.png --message "Your secret message here!"
```

### Decoding a Message
```bash
python bpcs_steganography.py --decode --infile output.png
```

## Requirements
- Python 3.x
- numpy
- Pillow

Install dependencies with:
```bash
pip install numpy Pillow
```

## Notes
- Works best with grayscale PNG images.
- The message is limited to 160 characters for this project.
- The script is for educational purposes and is well-commented for learning. 
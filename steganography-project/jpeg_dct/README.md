# JPEG DCT Steganography

This folder demonstrates how to hide and extract a 160-character message in a JPEG image using the DCT (Discrete Cosine Transform) algorithm.

## Algorithm Overview
JPEG images are compressed using DCT, which transforms image blocks into frequency components. By modifying the least significant bits of selected DCT coefficients (excluding the DC component), we can embed secret data without significantly affecting image quality.

## Usage
- Use `jpeg_dct_steganography.py` to encode or decode a message in a JPEG file.
- The script automatically converts images to grayscale for simplicity.

### Encoding a Message
```bash
python jpeg_dct_steganography.py --encode --infile input.jpg --outfile output.jpg --message "Your secret message here!"
```

### Decoding a Message
```bash
python jpeg_dct_steganography.py --decode --infile output.jpg
```

## Requirements
- Python 3.x
- numpy
- Pillow
- scipy

Install dependencies with:
```bash
pip install numpy Pillow scipy
```

## Notes
- Works best with grayscale JPEG images.
- The message is limited to 160 characters for this project.
- The script is for educational purposes and is well-commented for learning. 
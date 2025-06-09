# Steganography Project

This project demonstrates how to hide and extract a 160-character message in audio, image, and video files using different steganography and steganalysis techniques. Each algorithm is implemented in a separate folder with educational and well-commented Python code.

## Algorithms and Folders

- `lsb_audio/` : LSB (Least Significant Bit) steganography for audio (WAV)
- `jpeg_dct/` : JPEG (DCT) steganography for images (JPEG)
- `bpcs_image/` : BPCS (Bit Plane Complexity Segmentation) steganography for images (PNG)
- `masking_audio/` : Masking and filtering steganography for audio (WAV)
- `heuristic_video/` : Heuristic steganography for video (MP4)

Each folder contains:
- A detailed README explaining the algorithm and usage
- Example input files
- Python scripts for hiding and extracting messages

## How to Use
1. Install Python 3.x and required libraries (see each folder's README for dependencies).
2. Place your input file (audio/image/video) in the relevant folder.
3. Run the provided Python script to hide or extract a message.

## Educational Purpose
This repository is designed for educational purposes to help you understand and experiment with different steganography techniques. Each script is commented and easy to follow.

---

For more details, see the README in each algorithm's folder. 
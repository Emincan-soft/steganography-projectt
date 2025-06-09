import cv2
import numpy as np
import argparse
import sys

def message_to_bits(message):
    message += chr(0)
    bits = ''.join([format(ord(c), '08b') for c in message])
    return bits

def bits_to_message(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(''.join(byte), 2))
        if char == chr(0):
            break
        chars.append(char)
    return ''.join(chars)

def encode_heuristic(infile, outfile, message):
    cap = cv2.VideoCapture(infile)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(outfile, fourcc, fps, (width, height))
    bits = message_to_bits(message)
    bit_idx = 0
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Her karede sol üst pikselin mavi kanalının LSB'sine veri göm
        if bit_idx < len(bits):
            b, g, r = frame[0, 0]
            b = (b & ~1) | int(bits[bit_idx])
            frame[0, 0] = [b, g, r]
            bit_idx += 1
        out.write(frame)
        frame_idx += 1
    cap.release()
    out.release()
    print(f"Mesaj başarıyla {outfile} dosyasına gizlendi.")

def decode_heuristic(infile):
    cap = cv2.VideoCapture(infile)
    bits = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        b, g, r = frame[0, 0]
        bits.append(str(b & 1))
        if len(bits) % 8 == 0 and bits[-8:] == ['0']*8:
            message = bits_to_message(bits)
            print("Gizli Mesaj:", message)
            cap.release()
            return message
    message = bits_to_message(bits)
    print("Gizli Mesaj:", message)
    cap.release()
    return message

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sezgisel yöntemle videoya mesaj gizleme ve çıkarma.")
    parser.add_argument('--encode', action='store_true', help='Mesajı videoya gizle')
    parser.add_argument('--decode', action='store_true', help='Gizli mesajı çıkar')
    parser.add_argument('--infile', type=str, required=True, help='Giriş video dosyası (mp4 önerilir)')
    parser.add_argument('--outfile', type=str, help='Çıkış video dosyası (encode için)')
    parser.add_argument('--message', type=str, help='Gizlenecek mesaj (encode için)')
    args = parser.parse_args()

    if args.encode:
        if not args.outfile or not args.message:
            print("Encode için --outfile ve --message parametreleri gereklidir.")
            sys.exit(1)
        encode_heuristic(args.infile, args.outfile, args.message[:160])
    elif args.decode:
        decode_heuristic(args.infile)
    else:
        print("Lütfen --encode veya --decode seçiniz.") 
import numpy as np
from PIL import Image
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

def complexity(bitplane):
    # Komşu bitler arasındaki değişim oranı (basit karmaşıklık ölçütü)
    diff = np.sum(bitplane[:, :-1] != bitplane[:, 1:]) + np.sum(bitplane[:-1, :] != bitplane[1:, :])
    total = 2 * bitplane.shape[0] * (bitplane.shape[1] - 1)
    return diff / total

def encode_bpcs(infile, outfile, message, threshold=0.3):
    img = Image.open(infile).convert('L')
    arr = np.array(img)
    h, w = arr.shape
    bits = message_to_bits(message)
    bit_idx = 0
    arr_mod = arr.copy()
    for plane in range(7, -1, -1):
        bitplane = ((arr >> plane) & 1).astype(np.uint8)
        for i in range(0, h, 8):
            for j in range(0, w, 8):
                block = bitplane[i:i+8, j:j+8]
                if block.shape != (8, 8):
                    continue
                if complexity(block) > threshold:
                    # Karmaşık bloklara veri göm
                    for x in range(8):
                        for y in range(8):
                            if bit_idx >= len(bits):
                                break
                            block[x, y] = int(bits[bit_idx])
                            bit_idx += 1
                        if bit_idx >= len(bits):
                            break
                bitplane[i:i+8, j:j+8] = block
                if bit_idx >= len(bits):
                    break
            if bit_idx >= len(bits):
                break
        arr_mod &= ~(1 << plane)
        arr_mod |= (bitplane << plane)
        if bit_idx >= len(bits):
            break
    img_mod = Image.fromarray(arr_mod)
    img_mod.save(outfile)
    print(f"Mesaj başarıyla {outfile} dosyasına gizlendi.")

def decode_bpcs(infile, threshold=0.3):
    img = Image.open(infile).convert('L')
    arr = np.array(img)
    h, w = arr.shape
    bits = []
    for plane in range(7, -1, -1):
        bitplane = ((arr >> plane) & 1).astype(np.uint8)
        for i in range(0, h, 8):
            for j in range(0, w, 8):
                block = bitplane[i:i+8, j:j+8]
                if block.shape != (8, 8):
                    continue
                if complexity(block) > threshold:
                    for x in range(8):
                        for y in range(8):
                            bits.append(str(block[x, y]))
                            if len(bits) % 8 == 0 and bits[-8:] == ['0']*8:
                                message = bits_to_message(bits)
                                print("Gizli Mesaj:", message)
                                return message
    message = bits_to_message(bits)
    print("Gizli Mesaj:", message)
    return message

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BPCS ile resme mesaj gizleme ve çıkarma.")
    parser.add_argument('--encode', action='store_true', help='Mesajı resme gizle')
    parser.add_argument('--decode', action='store_true', help='Gizli mesajı çıkar')
    parser.add_argument('--infile', type=str, required=True, help='Giriş resim dosyası (PNG önerilir)')
    parser.add_argument('--outfile', type=str, help='Çıkış dosyası (encode için)')
    parser.add_argument('--message', type=str, help='Gizlenecek mesaj (encode için)')
    args = parser.parse_args()

    if args.encode:
        if not args.outfile or not args.message:
            print("Encode için --outfile ve --message parametreleri gereklidir.")
            sys.exit(1)
        encode_bpcs(args.infile, args.outfile, args.message[:160])
    elif args.decode:
        decode_bpcs(args.infile)
    else:
        print("Lütfen --encode veya --decode seçiniz.") 
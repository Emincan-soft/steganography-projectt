import numpy as np
from PIL import Image
import argparse
import sys
import scipy.fftpack

# Yardımcı fonksiyon: Mesajı bit dizisine çevir
def message_to_bits(message):
    message += chr(0)  # Mesaj sonu için null karakter
    bits = ''.join([format(ord(c), '08b') for c in message])
    return bits

# Yardımcı fonksiyon: Bit dizisini mesaja çevir
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

# 8x8 bloklara ayır
def blockify(arr, block_size=8):
    h, w = arr.shape
    return [arr[i:i+block_size, j:j+block_size]
            for i in range(0, h, block_size)
            for j in range(0, w, block_size)]

def unblockify(blocks, shape, block_size=8):
    h, w = shape
    arr = np.zeros((h, w), dtype=np.float32)
    idx = 0
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            arr[i:i+block_size, j:j+block_size] = blocks[idx]
            idx += 1
    return arr

# Mesajı DCT katsayılarının LSB'sine göm
def encode_dct(infile, outfile, message):
    img = Image.open(infile).convert('L')  # Gri tonlamalıya çevir
    arr = np.array(img, dtype=np.float32)
    h, w = arr.shape
    blocks = blockify(arr)
    bits = message_to_bits(message)
    bit_idx = 0
    for block in blocks:
        dct = scipy.fftpack.dct(scipy.fftpack.dct(block.T, norm='ortho').T, norm='ortho')
        # (0,0) DC bileşeni hariç, ilk uygun AC bileşenin LSB'sine bit göm
        for x in range(8):
            for y in range(8):
                if x == 0 and y == 0:
                    continue
                if bit_idx >= len(bits):
                    break
                coeff = int(dct[x, y])
                coeff = (coeff & ~1) | int(bits[bit_idx])
                dct[x, y] = coeff
                bit_idx += 1
            if bit_idx >= len(bits):
                break
        # Ters DCT
        block[:, :] = scipy.fftpack.idct(scipy.fftpack.idct(dct.T, norm='ortho').T, norm='ortho')
        block[:, :] = np.clip(block, 0, 255)
        if bit_idx >= len(bits):
            break
    arr_mod = unblockify(blocks, (h, w))
    img_mod = Image.fromarray(arr_mod.astype(np.uint8))
    img_mod.save(outfile, 'JPEG')
    print(f"Mesaj başarıyla {outfile} dosyasına gizlendi.")

# DCT katsayılarının LSB'sinden mesajı çıkar
def decode_dct(infile):
    img = Image.open(infile).convert('L')
    arr = np.array(img, dtype=np.float32)
    blocks = blockify(arr)
    bits = []
    for block in blocks:
        dct = scipy.fftpack.dct(scipy.fftpack.dct(block.T, norm='ortho').T, norm='ortho')
        for x in range(8):
            for y in range(8):
                if x == 0 and y == 0:
                    continue
                bits.append(str(int(dct[x, y]) & 1))
                if len(bits) % 8 == 0 and bits[-8:] == ['0']*8:
                    message = bits_to_message(bits)
                    print("Gizli Mesaj:", message)
                    return message
    message = bits_to_message(bits)
    print("Gizli Mesaj:", message)
    return message

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JPEG (DCT) ile resme mesaj gizleme ve çıkarma.")
    parser.add_argument('--encode', action='store_true', help='Mesajı resme gizle')
    parser.add_argument('--decode', action='store_true', help='Gizli mesajı çıkar')
    parser.add_argument('--infile', type=str, required=True, help='Giriş JPEG dosyası')
    parser.add_argument('--outfile', type=str, help='Çıkış JPEG dosyası (encode için)')
    parser.add_argument('--message', type=str, help='Gizlenecek mesaj (encode için)')
    args = parser.parse_args()

    if args.encode:
        if not args.outfile or not args.message:
            print("Encode için --outfile ve --message parametreleri gereklidir.")
            sys.exit(1)
        encode_dct(args.infile, args.outfile, args.message[:160])
    elif args.decode:
        decode_dct(args.infile)
    else:
        print("Lütfen --encode veya --decode seçiniz.") 
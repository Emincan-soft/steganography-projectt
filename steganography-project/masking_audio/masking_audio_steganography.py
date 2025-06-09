import wave
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

def encode_masking(infile, outfile, message):
    with wave.open(infile, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(wav.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16)

    bits = message_to_bits(message)
    if len(bits) > len(audio) // 2:
        print("Hata: Mesaj çok uzun!")
        sys.exit(1)

    audio_mod = np.copy(audio)
    # Yüksek frekanslı (maskelenmiş) bölgelere veri gömme
    for i, bit in enumerate(bits):
        idx = len(audio) // 2 + i  # Sinyalin ortasından sonuna doğru (yüksek frekanslı kısım)
        audio_mod[idx] = (audio_mod[idx] & ~1) | int(bit)

    with wave.open(outfile, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(audio_mod.tobytes())
    print(f"Mesaj başarıyla {outfile} dosyasına gizlendi.")

def decode_masking(infile):
    with wave.open(infile, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16)

    bits = [str(audio[len(audio)//2 + i] & 1) for i in range(len(audio)//2)]
    message = bits_to_message(bits)
    print("Gizli Mesaj:", message)
    return message

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Maskeleme ve filtreleme ile WAV dosyasına mesaj gizleme ve çıkarma.")
    parser.add_argument('--encode', action='store_true', help='Mesajı ses dosyasına gizle')
    parser.add_argument('--decode', action='store_true', help='Gizli mesajı çıkar')
    parser.add_argument('--infile', type=str, required=True, help='Giriş WAV dosyası')
    parser.add_argument('--outfile', type=str, help='Çıkış WAV dosyası (encode için)')
    parser.add_argument('--message', type=str, help='Gizlenecek mesaj (encode için)')
    args = parser.parse_args()

    if args.encode:
        if not args.outfile or not args.message:
            print("Encode için --outfile ve --message parametreleri gereklidir.")
            sys.exit(1)
        encode_masking(args.infile, args.outfile, args.message[:160])
    elif args.decode:
        decode_masking(args.infile)
    else:
        print("Lütfen --encode veya --decode seçiniz.") 
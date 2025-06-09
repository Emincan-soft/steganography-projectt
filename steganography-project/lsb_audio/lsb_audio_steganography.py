import wave
import numpy as np
import argparse
import sys

# LSB ile mesajı ses dosyasına gömme fonksiyonu
def encode_audio(infile, outfile, message):
    # WAV dosyasını oku
    with wave.open(infile, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(wav.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16)

    # Mesajı bitlere çevir
    message += chr(0)  # Mesaj sonu için null karakter
    bits = ''.join([format(ord(c), '08b') for c in message])

    if len(bits) > len(audio):
        print("Hata: Mesaj çok uzun!")
        sys.exit(1)

    # LSB'leri mesaj bitleriyle değiştir
    audio_mod = np.copy(audio)
    for i, bit in enumerate(bits):
        audio_mod[i] = (audio_mod[i] & ~1) | int(bit)

    # Yeni ses dosyasını kaydet
    with wave.open(outfile, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(audio_mod.tobytes())
    print(f"Mesaj başarıyla {outfile} dosyasına gizlendi.")

# LSB ile ses dosyasından mesajı çıkarma fonksiyonu
def decode_audio(infile):
    with wave.open(infile, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16)

    bits = [str(audio[i] & 1) for i in range(len(audio))]
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(''.join(byte), 2))
        if char == chr(0):
            break
        chars.append(char)
    message = ''.join(chars)
    print("Gizli Mesaj:", message)
    return message

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LSB ile WAV dosyasına mesaj gizleme ve çıkarma.")
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
        encode_audio(args.infile, args.outfile, args.message[:160])
    elif args.decode:
        decode_audio(args.infile)
    else:
        print("Lütfen --encode veya --decode seçiniz.") 
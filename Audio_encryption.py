import numpy as np
from scipy.io import wavfile


class AudioEncryptor:
    """
    Encrypt a stereo WAV file using XOR with a logistic-map-generated key.
    """
    def __init__(self, r=3.99, x0=0.5):
        self.r = r
        self.x0 = x0
        self.key = None
    @staticmethod
    def read_audio(path):
        rate, data = wavfile.read(path)
        print(f"Loaded '{path}' → rate={rate}, shape={data.shape}, dtype={data.dtype}")
        return rate, data
    @staticmethod
    def write_audio(path, rate, data):
        wavfile.write(path, rate, data)
        print(f"Saved '{path}' → dtype={data.dtype}, shape={data.shape}")

    def generate_key(self, n):
        """
        Generate a chaotic logistic-map key stream mapped into uint16 [0..65535].
        """
        x = self.x0
        key = np.empty(n, dtype=np.uint16)
        for i in range(n):
            x = self.r * x * (1 - x)
            key[i] = np.uint16(np.floor(x * 65535))
        return key

    def encrypt(self, in_path, out_path):
        """
        Encrypt the WAV at in_path and write the ciphertext to out_path.
        Returns the key stream and sample rate.
        """
        rate, audio = self.read_audio(in_path)

        L = audio[:, 0].astype(np.uint16)
        R = audio[:, 1].astype(np.uint16)

        n = L.size
        self.key = self.generate_key(n)

        C1 = np.bitwise_xor(L, self.key)
        C2 = np.bitwise_xor(R, self.key)

        encrypted = np.vstack((C1, C2)).T.astype(np.int16)
        self.write_audio(out_path, rate, encrypted)
        return self.key, rate


class AudioDecryptor:
    """
    Decrypt an encrypted audio.
    """
    def __init__(self, r=3.99, x0=0.5):
        self.r = r
        self.x0 = x0
    @staticmethod
    def read_audio(path):
        rate, data = wavfile.read(path)
        print(f"Loaded '{path}' → rate={rate}, shape={data.shape}, dtype={data.dtype}")
        return rate, data
    @staticmethod
    def write_audio(path, rate, data):
        wavfile.write(path, rate, data)
        print(f"Saved '{path}' → dtype={data.dtype}, shape={data.shape}")

    def generate_key(self, n):
        x = self.x0
        key = np.empty(n, dtype=np.uint16)
        for i in range(n):
            x = self.r * x * (1 - x)
            key[i] = np.uint16(np.floor(x * 65535))
        return key

    def decrypt(self, in_path, out_path, key=None, rate=None):
        """
        Decrypt the WAV at in_path using the provided key or regenerate one.
        Writes the decrypted audio to out_path and returns the array.
        """
        if rate is None:
            rate, encrypted = self.read_audio(in_path)
        else:
            _, encrypted = self.read_audio(in_path)

        L_enc = encrypted[:, 0].astype(np.uint16)
        R_enc = encrypted[:, 1].astype(np.uint16)
        n = L_enc.size

        if key is None:
            key = self.generate_key(n)

        L_plain = np.bitwise_xor(L_enc, key).astype(np.int16)
        R_plain = np.bitwise_xor(R_enc, key).astype(np.int16)

        decrypted = np.vstack((L_plain, R_plain)).T
        self.write_audio(out_path, rate, decrypted)
        return decrypted


if __name__ == '__main__':
    encryptor = AudioEncryptor(r=3.99, x0=0.5)
    key_stream, sr = encryptor.encrypt('person1.wav', 'person1_encrypted.wav')

    decryptor = AudioDecryptor(r=3.99, x0=0.5)
    decryptor.decrypt('person1_encrypted.wav', 'person1_decrypted.wav', key=key_stream, rate=sr)
    print("Done: encryption and decryption complete.")
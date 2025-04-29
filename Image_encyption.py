import numpy as np
import cv2

class ImageEncryptor:
    def __init__(self, frame_shape, r=3.99, x0=0.5):
        self.r = r
        self.x0 = x0
        self.frame_shape = frame_shape
        self.n = frame_shape[0] * frame_shape[1] * frame_shape[2]

        # Precompute key and permutation once
        self.key = self.generate_key(self.n)
        self.permutation = self.generate_permutation(self.n)

    def generate_key(self, n):
        x = np.empty(n, dtype=np.float32)
        x[0] = self.x0
        for i in range(1, n):
            x[i] = self.r * x[i-1] * (1 - x[i-1])
        key = np.floor(x * 255).astype(np.uint8)
        return key

    def generate_permutation(self, n):
        np.random.seed(42)
        return np.random.permutation(n)

    def encrypt(self, frame):
        flat_frame = frame.reshape(-1)
        shuffled_frame = flat_frame[self.permutation]
        encrypted_flat_frame = np.bitwise_xor(shuffled_frame, self.key)
        encrypted_frame = encrypted_flat_frame.reshape(self.frame_shape)
        return encrypted_frame


class ImageDecryptor:
    def __init__(self, frame_shape, r=3.99, x0=0.5):
        self.r = r
        self.x0 = x0
        self.frame_shape = frame_shape
        self.n = frame_shape[0] * frame_shape[1] * frame_shape[2]

        # Precompute key and permutation once
        self.key = self.generate_key(self.n)
        self.permutation = self.generate_permutation(self.n)
        self.inverse_permutation = np.argsort(self.permutation)

    def generate_key(self, n):
        x = np.empty(n, dtype=np.float32)
        x[0] = self.x0
        for i in range(1, n):
            x[i] = self.r * x[i-1] * (1 - x[i-1])
        key = np.floor(x * 255).astype(np.uint8)
        return key

    def generate_permutation(self, n):
        np.random.seed(42)
        return np.random.permutation(n)

    def decrypt(self, frame):
        flat_frame = frame.reshape(-1)
        decrypted_flat_frame = np.bitwise_xor(flat_frame, self.key)
        unshuffled_frame = decrypted_flat_frame[self.inverse_permutation]
        decrypted_frame = unshuffled_frame.reshape(self.frame_shape)
        return decrypted_frame


if __name__ == '__main__':
    frame = cv2.imread('/Users/harshsingh/Desktop/Course/Nld/frames/frame0.jpg')
    frame_shape = frame.shape

    # Important: use SAME r and x0
    r = 3.99
    x0 = 0.7

    encryptor = ImageEncryptor(frame_shape, r=r, x0=x0)
    encrypted_frame = encryptor.encrypt(frame)
    cv2.imwrite('encrypted_frame_0.jpg', encrypted_frame)

    decryptor = ImageDecryptor(frame_shape, r=r, x0=x0)
    decrypted_frame = decryptor.decrypt(encrypted_frame)
    cv2.imwrite('decrypted_frame_0.jpg', decrypted_frame)
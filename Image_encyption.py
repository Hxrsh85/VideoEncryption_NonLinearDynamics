import numpy as np
import cv2
import numpy as np

class ImageEncryptor:
    def __init__(self, r=3.99, x0=0.5):
        self.r = r
        self.x0 = x0
        self.key = None
        self.permutation = None

    def generate_key(self, n):
        x = self.x0
        key = np.empty(n, dtype=np.uint8)
        for i in range(n):
            x = self.r * x * (1 - x)
            key[i] = np.uint8(np.floor(x * 255))
        return key

    def generate_permutation(self, n):
        np.random.seed(42) 
        permutation = np.random.permutation(n)
        return permutation

    def encrypt(self, frame):
        height, width, channels = frame.shape
        n = height * width * channels 

        self.key = self.generate_key(n)
        self.permutation = self.generate_permutation(n)

        flat_frame = frame.flatten()
        flat_frame = flat_frame[self.permutation] 

        encrypted_flat_frame = np.bitwise_xor(flat_frame, self.key[:len(flat_frame)])
        encrypted_frame = encrypted_flat_frame.reshape((height, width, channels))

        return encrypted_frame, self.key, self.permutation


class ImageDecryptor:
    def __init__(self, r=3.99, x0=0.5):
        self.r = r
        self.x0 = x0

    def generate_key(self, n):
        x = self.x0
        key = np.empty(n, dtype=np.uint8)
        for i in range(n):
            x = self.r * x * (1 - x)
            key[i] = np.uint8(np.floor(x * 255))
        return key

    def generate_permutation(self, n):
        np.random.seed(42) 
        permutation = np.random.permutation(n)
        return permutation

    def decrypt(self, frame, key=None, permutation=None, shape=None):

        height, width, channels = shape
        n = height * width * channels

        if key is None:
            key = self.generate_key(n)

        if permutation is None:
            permutation = self.generate_permutation(n)

        inverse_permutation = np.argsort(permutation)

        flat_frame = frame.flatten()
        decrypted_flat_frame = np.bitwise_xor(flat_frame, key[:len(flat_frame)])
        decrypted_flat_frame = decrypted_flat_frame[inverse_permutation]  # unshuffle
        decrypted_frame = decrypted_flat_frame.reshape((height, width, channels))

        return decrypted_frame



if __name__ == '__main__':

    frame = cv2.imread(f'/Users/harshsingh/Desktop/Course/Nld/frames/frame0.jpg') 

    encryptor = ImageEncryptor(r=3.99, x0=0.7)
    encrypted_frame, key_stream, permutation = encryptor.encrypt(frame)

    cv2.imwrite('encrypted_frame_0.jpg', encrypted_frame) 

    decryptor = ImageDecryptor(r=3.99, x0=0.50000000001)
    decrypted_frame = decryptor.decrypt(encrypted_frame, None ,permutation, encrypted_frame.shape)

    cv2.imwrite('decrypted_frame_0.jpg', decrypted_frame) 
import os
import cv2

from Audio_extractor import AudioExtractor
from Frame_extractor import FrameExtractor
from Audio_Video_combiner import VideoCreator
from Audio_encryption import AudioDecryptor, AudioEncryptor
from Image_encyption import ImageDecryptor, ImageEncryptor

# Directory setup
ORIGINAL_DIR = 'original'
ENCRYPTED_DIR = 'encrypted'
DECRYPTED_DIR = 'decrypted'

# Input video file
INPUT_VIDEO_NAME = 'Nld_vid_2.mov'
INPUT_VIDEO_BASENAME = os.path.splitext(INPUT_VIDEO_NAME)[0]  
ORIGINAL_VIDEO_PATH = os.path.join(ORIGINAL_DIR, INPUT_VIDEO_NAME)

# Dynamic filenames based on input video
ORIGINAL_AUDIO_PATH = os.path.join(ORIGINAL_DIR, f'original_{INPUT_VIDEO_BASENAME}_audio.wav')
ENCRYPTED_AUDIO_PATH = os.path.join(ENCRYPTED_DIR, f'encrypted_{INPUT_VIDEO_BASENAME}_audio.wav')
DECRYPTED_AUDIO_PATH = os.path.join(DECRYPTED_DIR, f'decrypted_{INPUT_VIDEO_BASENAME}_audio.wav')

ENCRYPTED_VIDEO_PATH = os.path.join(ENCRYPTED_DIR, f'encrypted_{INPUT_VIDEO_BASENAME}_video.mov')
DECRYPTED_VIDEO_PATH = os.path.join(DECRYPTED_DIR, f'decrypted_{INPUT_VIDEO_BASENAME}_video.mov')

# Parameters
r = 3.99

# Audio parameters
x0_enc_audio = 0.5
x0_dec_audio = 0.50001

# Image parameters
x0_enc_img = 0.7
x0_dec_img = 0.70001


# Extract Audio
audio_extractor = AudioExtractor(ORIGINAL_VIDEO_PATH, ORIGINAL_AUDIO_PATH)
audio_extractor.extract_audio()

# Extract Frames
frame_extractor = FrameExtractor(ORIGINAL_VIDEO_PATH)
frames = frame_extractor.extract_frames()
frame_shape = frames[0].shape


# Encrypt Audio
audio_encryptor = AudioEncryptor(r, x0_enc_audio)
key_stream, sr = audio_encryptor.encrypt(ORIGINAL_AUDIO_PATH, ENCRYPTED_AUDIO_PATH)

# Encrypt Video Frames
image_encryptor = ImageEncryptor(frame_shape, r, x0_enc_img)
encrypted_frames = [image_encryptor.encrypt(frame) for frame in frames]

# Combine Encrypted Audio + Frames
video_creator = VideoCreator(encrypted_frames, ENCRYPTED_AUDIO_PATH, ENCRYPTED_VIDEO_PATH)
video_creator.create_video()


# Decrypt Audio
audio_decryptor = AudioDecryptor(r, x0_dec_audio)
audio_decryptor.decrypt(ENCRYPTED_AUDIO_PATH, DECRYPTED_AUDIO_PATH, rate=sr)

# Decrypt Video Frames
image_decryptor = ImageDecryptor(frame_shape, r, x0_dec_img)
decrypted_frames = [image_decryptor.decrypt(frame) for frame in encrypted_frames]

# Combine Decrypted Audio + Frames
video_creator = VideoCreator(decrypted_frames, DECRYPTED_AUDIO_PATH, DECRYPTED_VIDEO_PATH)
video_creator.create_video()

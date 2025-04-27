import os
import cv2
import subprocess

from Audio_extractor import AudioExtractor
from Frame_extractor import FrameExtractor
from Audio_Video_combiner import VideoCreator

from Audio_encryption import AudioDecryptor, AudioEncryptor

from Image_encyption import ImageDecryptor, ImageEncryptor


video_path = 'video1.mov'      # Your input video path
audio_output_path = 'output.wav'   # Path to save the extracted audio
audio_extractor = AudioExtractor(video_path, audio_output_path)
audio_extractor.extract_audio()

frame_extractor = FrameExtractor(video_path)
frames = frame_extractor.extract_frames()

#performing encryption on Audio:
encryptor = AudioEncryptor(r=3.99, x0=0.5)
key_stream, sr = encryptor.encrypt('output.wav', 'encrypted_audio.wav')

#performing encryption on Video:
encryptor = ImageEncryptor(r=3.99, x0=0.7)
encrypted_frames = []
for frame in frames:
    encrypted_frame, key_stream, permutation = encryptor.encrypt(frame)
    encrypted_frames.append(encrypted_frame)

#combining encrypted audio and video to get the encrypted video:
output_video_path = "Encrypted_video.mov"
video_creator = VideoCreator(encrypted_frames, 'encrypted_audio.wav', output_video_path)
video_creator.create_video()

#performing Decryption on audio:
decryptor = AudioDecryptor(r=3.99, x0=0.5)
decryptor.decrypt('encrypted_audio.wav', 'decrypted_audio.wav', rate=sr)

#performing Decryption on Video:
decryptor = ImageDecryptor(r=3.99, x0=0.7)
decrypted_frames = []
for enc_frame in encrypted_frames:
    decrypted_frame = decryptor.decrypt(enc_frame, None , permutation, enc_frame.shape)
    decrypted_frames.append(decrypted_frame)

#combining encrypted audio and video to get the encrypted video:
output_video_path = "Decrypted_video.mov"
video_creator = VideoCreator(decrypted_frames, 'decrypted_audio.wav', output_video_path)
video_creator.create_video()





import os
import cv2
import subprocess

class AudioExtractor:
    def __init__(self, video_path, output_audio_path):
        self.video_path = video_path
        self.output_audio_path = output_audio_path

    def extract_audio(self):
        """
        Extract audio from the video using FFmpeg and save it as a .wav file.
        """
        command = [
            'ffmpeg',
            '-i', self.video_path,   # Input video file
            '-vn',                    # Disable video processing
            '-acodec', 'pcm_s16le',   # Audio codec (PCM signed 16-bit little endian)
            '-ar', '44100',           # Audio sample rate
            '-ac', '2',               # Audio channels (stereo)
            self.output_audio_path    # Output audio file
        ]
        
        subprocess.run(command, check=True)
        print(f"Audio extracted and saved to {self.output_audio_path}")

if __name__ == '__main__':

    video_path = 'video1.mov'      # Your input video path
    audio_output_path = 'output.wav'   # Path to save the extracted audio
    audio_extractor = AudioExtractor(video_path, audio_output_path)
    audio_extractor.extract_audio()
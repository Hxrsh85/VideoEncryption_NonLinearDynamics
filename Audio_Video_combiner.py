import subprocess
import os
import cv2

class VideoCreator:
    def __init__(self, frames, audio_path, output_video_path, fps=30):
        self.frames = frames
        self.audio_path = audio_path
        self.output_video_path = output_video_path
        self.fps = fps

    def create_video(self):
        """
        Combine frames and audio to create a video file.
        """
        if not self.frames:
            print("Error: No frames to process.")
            return
        
        # Get the frame size from the first frame
        height, width, _ = self.frames[0].shape

        # Create a temporary video file (with no audio)
        temp_video_path = "temp_video.mov"

        # Create a VideoWriter object using 'mp4v' codec (can save as .mov)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_video_path, fourcc, self.fps, (width, height))

        # Write each frame to the temporary video file
        for frame in self.frames:
            out.write(frame)

        out.release()
        print(f"Temporary video saved to {temp_video_path}")

        # Now combine the temporary video file with the audio
        self.combine_audio_video(temp_video_path)

    def combine_audio_video(self, temp_video_path):
        """
        Combine the video and audio files into a final video with audio.
        """
        command = [
            'ffmpeg',
            '-i', temp_video_path,         # Input video file (temporary video)
            '-i', self.audio_path,         # Input audio file
            '-c:v', 'copy',                # Copy the video codec
            '-c:a', 'aac',                 # Use AAC codec for audio
            '-strict', 'experimental',     # Use experimental features for AAC
            '-shortest',                   # Match the shortest duration (video/audio)
            self.output_video_path         # Final output video with audio
        ]
        
        subprocess.run(command, check=True)
        print(f"Final video with audio saved to {self.output_video_path}")

        # Clean up the temporary video file
        os.remove(temp_video_path)
        print(f"Temporary video file {temp_video_path} deleted.")

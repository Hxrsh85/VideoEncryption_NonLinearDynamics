import cv2
import os

class FrameExtractor:
    def __init__(self, video_path):
        self.video_path = video_path

    def extract_frames(self):
        """
        Extract frames from the video and return them as a list of NumPy arrays.
        """
        cap = cv2.VideoCapture(self.video_path)
        frames = []

        if not cap.isOpened():
            print("Error: Could not open video file.")
            return frames

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Append the frame to the list (in BGR format)
            frames.append(frame)

        cap.release()
        print(f"Extracted {len(frames)} frames from {self.video_path}")
        return frames
import cv2
import os

def video_frame_generator(video_path, step=1, resize=None):
    """
    A generator that yields frames from a video one by one.

    :param video_path: Path to the video file
    :param step: Step size (1 = every frame, 30 = every 30th frame)
    :yield: Tuple (frame_id, frame_image)
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    try:
        frame_idx = 0
        while True:
            success, frame = cap.read()

            if not success:
                break  # Video is finished

            # Only yield if we match the step interval
            if frame_idx % step == 0:
                if resize is not None:
                    # INTER_AREA is best for shrinking images (downsampling)
                    # INTER_LINEAR is faster, but INTER_AREA reduces noise better for ML
                    frame = cv2.resize(frame, resize, interpolation=cv2.INTER_AREA)
                yield frame_idx, frame

            frame_idx += 1

    finally:
        cap.release()

if __name__ == "__main__":
        video_path = 'test.mp4'
        vid_frame_iter = video_frame_generator(video_path, resize=(160,160))

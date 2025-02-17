import os

import cv2


def extract_frames(video_path, output_dir, fps_target=None):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    if fps_target is None:
        fps_target = frame_rate
    frame_interval = int(round(frame_rate / fps_target))
    count = 0
    saved = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            filename = os.path.join(output_dir, f"frame_{saved:04d}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Extracted frame {saved}: {filename}")
            saved += 1
        count += 1
    cap.release()


# Example usage:
extract_frames("input_video.mp4", "data/real_frames/input", fps_target=15)

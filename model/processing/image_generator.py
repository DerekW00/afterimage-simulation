import os

import cv2
import numpy as np


# --- Step 1: Extract Frames from Video ---

def extract_frames(video_path, output_dir, fps_target=None):
    """
    Extract frames from a video file and save them as JPEG images.

    Parameters:
      video_path (str): Path to the input video file.
      output_dir (str): Directory to save extracted frames.
      fps_target (float, optional): Target FPS for extraction (if None, use the video's native FPS).
    """
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video {video_path}")
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if fps_target is None:
        fps_target = video_fps
    # Calculate frame interval
    frame_interval = int(round(video_fps / fps_target))
    frame_count = 0
    saved_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            filename = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Extracted frame {saved_count}: {filename}")
            saved_count += 1
        frame_count += 1
    cap.release()
    print(f"Extraction complete. {saved_count} frames saved in '{output_dir}'.")


# --- Step 2: Generate Afterimage Frames ---

def generate_afterimage_frame(frame):
    """
    Generate an afterimage effect for a single frame.

    Here we use a simple inversion as an example.
    In your model, replace this with your more advanced processing.

    Parameters:
      frame (np.ndarray): Original frame (BGR format).

    Returns:
      np.ndarray: Afterimage frame (BGR format).
    """
    # Example: invert colors for afterimage effect.
    return cv2.bitwise_not(frame)


def generate_afterimage_frames(input_dir, afterimage_dir):
    """
    Process all frames in input_dir to generate corresponding afterimage frames.
    """
    os.makedirs(afterimage_dir, exist_ok=True)
    frame_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith('.jpg')])
    for i, fname in enumerate(frame_files):
        input_path = os.path.join(input_dir, fname)
        frame = cv2.imread(input_path)
        if frame is None:
            print(f"Skipping {fname}: unable to read.")
            continue
        afterimage = generate_afterimage_frame(frame)
        output_path = os.path.join(afterimage_dir, fname)
        cv2.imwrite(output_path, afterimage)
        print(f"Generated afterimage frame {i + 1}/{len(frame_files)}: {output_path}")
    print(f"Afterimage frame generation complete. Frames saved in '{afterimage_dir}'.")


# --- Step 3: Generate Videos from Frames ---

def generate_videos(original_dir, afterimage_dir, output_dir, fps=30, alpha=0.5):
    """
    Generate four videos from the original and afterimage frames:
      1. Original Video
      2. Afterimage Video
      3. Blended Video (input blended with afterimage)
      4. Side-by-Side Comparison Video (original and blended horizontally)

    Parameters:
      original_dir (str): Folder with original frames.
      afterimage_dir (str): Folder with afterimage frames.
      output_dir (str): Folder to save the videos.
      fps (int): Frames per second for the videos.
      alpha (float): Blending weight for the original (0 < alpha <= 1).
    """
    os.makedirs(output_dir, exist_ok=True)

    original_frames = sorted([f for f in os.listdir(original_dir) if f.lower().endswith('.jpg')])
    afterimage_frames = sorted([f for f in os.listdir(afterimage_dir) if f.lower().endswith('.jpg')])

    if not original_frames or not afterimage_frames:
        print("No frames found in one or both directories.")
        return

    frame_count = min(len(original_frames), len(afterimage_frames))
    # Read first frame to determine dimensions (assume both sets have same dimensions)
    first_frame = cv2.imread(os.path.join(original_dir, original_frames[0]))
    height, width, _ = first_frame.shape

    # Define output video file paths.
    original_video_path = os.path.join(output_dir, "original_video.mp4")
    afterimage_video_path = os.path.join(output_dir, "afterimage_video.mp4")
    blended_video_path = os.path.join(output_dir, "blended_video.mp4")
    side_by_side_video_path = os.path.join(output_dir, "side_by_side_video.mp4")

    # Define codec (using H.264 via 'avc1' if available)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    original_video = cv2.VideoWriter(original_video_path, fourcc, fps, (width, height))
    afterimage_video = cv2.VideoWriter(afterimage_video_path, fourcc, fps, (width, height))
    blended_video = cv2.VideoWriter(blended_video_path, fourcc, fps, (width, height))
    side_by_side_video = cv2.VideoWriter(side_by_side_video_path, fourcc, fps, (width * 2, height))

    for i in range(frame_count):
        orig_path = os.path.join(original_dir, original_frames[i])
        af_path = os.path.join(afterimage_dir, afterimage_frames[i])
        orig_frame = cv2.imread(orig_path)
        af_frame = cv2.imread(af_path)
        if orig_frame is None or af_frame is None:
            print(f"Skipping frame {i + 1} due to read error.")
            continue

        # Generate blended frame.
        blended = cv2.addWeighted(orig_frame, alpha, af_frame, 1 - alpha, 0)
        # Generate side-by-side frame (stack horizontally).
        side_by_side = np.hstack((orig_frame, blended))

        # Write to videos.
        original_video.write(orig_frame)
        afterimage_video.write(af_frame)
        blended_video.write(blended)
        side_by_side_video.write(side_by_side)

        print(f"Processed frame {i + 1}/{frame_count}")

    original_video.release()
    afterimage_video.release()
    blended_video.release()
    side_by_side_video.release()

    print("Videos generated successfully:")
    print("  Original Video:", original_video_path)
    print("  Afterimage Video:", afterimage_video_path)
    print("  Blended Video:", blended_video_path)
    print("  Side-by-Side Video:", side_by_side_video_path)


# --- Main Pipeline ---

if __name__ == "__main__":
    # Define paths (adjust as needed)
    video_path = "data/afterimage/2_video/IMG_1124.mov"
    frames_dir = "data/afterimage/2_video/input"
    afterimage_dir = "data/afterimage/2_video/afterimage"
    videos_dir = "data/afterimage/2_video/output"

    # Step 1: Extract frames from the input video.
    print("Extracting frames...")
    extract_frames(video_path, frames_dir, fps_target=15)

    # Step 2: Generate afterimage frames.
    print("Generating afterimage frames...")
    generate_afterimage_frames(frames_dir, afterimage_dir)

    # Step 3: Generate 4 videos.
    print("Generating videos...")
    generate_videos(frames_dir, afterimage_dir, videos_dir, fps=15, alpha=0.5)

    print("Video processing pipeline completed!")

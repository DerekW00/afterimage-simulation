import os

import cv2

from model.processing.afterimage_batch import process_frame_sequence  # Reuse your batch processing module


# --- Step 1: Extract Frames from Video ---
def extract_frames(video_path, output_dir, fps_target=None):
    """
    Extract frames from a video file and save them as JPEG images.
    """
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video {video_path}")
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if fps_target is None:
        fps_target = video_fps
    frame_interval = int(round(video_fps / fps_target))
    count, saved = 0, 0
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
    print(f"Extraction complete. {saved} frames saved in '{output_dir}'.")


# --- Step 2: Generate Afterimage and Persistent Overlay Frames Using Your Batch Module ---
# This call will read frames from the extracted frames folder and write:
#   - Afterimage frames to afterimage_dir, and
#   - Persistent overlay frames into afterimage_dir/persistent_overlay
def generate_afterimage_and_overlay_frames(input_dir, afterimage_dir):
    process_frame_sequence(input_dir, afterimage_dir)


# --- Step 3: Generate Videos from Frames ---
def generate_videos(original_dir, afterimage_dir, persistent_overlay_dir, output_dir, fps=30, alpha=0.7,
                    target_resolution=None):
    """
    Generate four videos:
      1. Original Video: frames from original_dir.
      2. Afterimage Video: frames from afterimage_dir.
      3. Blended Video: each frame is blended (alpha) from original and afterimage.
      4. Persistent Overlay Video: frames from persistent_overlay_dir.

    Parameters:
      original_dir (str): Directory containing original frames.
      afterimage_dir (str): Directory containing afterimage frames.
      persistent_overlay_dir (str): Directory with persistent overlay frames.
      output_dir (str): Directory to save the videos.
      fps (int): Frames per second.
      alpha (float): Blending factor for creating a blended frame (only used here for the blended video).
      target_resolution (tuple, optional): (width, height) to which frames are resized.
    """
    os.makedirs(output_dir, exist_ok=True)

    original_frames = sorted([f for f in os.listdir(original_dir) if f.lower().endswith('.jpg')])
    afterimage_frames = sorted([f for f in os.listdir(afterimage_dir) if f.lower().endswith('.jpg')])
    overlay_frames = sorted([f for f in os.listdir(persistent_overlay_dir) if f.lower().endswith('.jpg')])

    if not original_frames or not afterimage_frames or not overlay_frames:
        print("No frames found in one or more directories.")
        return
    frame_count = min(len(original_frames), len(afterimage_frames), len(overlay_frames))

    first_frame = cv2.imread(os.path.join(original_dir, original_frames[0]))
    if first_frame is None:
        print("Failed to read the first frame.")
        return
    if target_resolution:
        width, height = target_resolution
    else:
        height, width, _ = first_frame.shape

    # Set video output paths.
    original_video_path = os.path.join(output_dir, "original_video.mp4")
    afterimage_video_path = os.path.join(output_dir, "afterimage_video.mp4")
    blended_video_path = os.path.join(output_dir, "blended_video.mp4")
    overlay_video_path = os.path.join(output_dir, "persistent_overlay_video.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    original_video = cv2.VideoWriter(original_video_path, fourcc, fps, (width, height))
    afterimage_video = cv2.VideoWriter(afterimage_video_path, fourcc, fps, (width, height))
    blended_video = cv2.VideoWriter(blended_video_path, fourcc, fps, (width, height))
    overlay_video = cv2.VideoWriter(overlay_video_path, fourcc, fps, (width, height))

    for i in range(frame_count):
        orig_path = os.path.join(original_dir, original_frames[i])
        af_path = os.path.join(afterimage_dir, afterimage_frames[i])
        ol_path = os.path.join(persistent_overlay_dir, overlay_frames[i])

        orig_frame = cv2.imread(orig_path)
        af_frame = cv2.imread(af_path)
        ol_frame = cv2.imread(ol_path)
        if orig_frame is None or af_frame is None or ol_frame is None:
            print(f"Skipping frame {i + 1} due to read error.")
            continue

        if target_resolution:
            orig_frame = cv2.resize(orig_frame, (width, height))
            af_frame = cv2.resize(af_frame, (width, height))
            ol_frame = cv2.resize(ol_frame, (width, height))

        # Blended frame: blend original and afterimage using alpha weight.
        blended = cv2.addWeighted(orig_frame, alpha, af_frame, 1 - alpha, 0)

        original_video.write(orig_frame)
        afterimage_video.write(af_frame)
        blended_video.write(blended)
        overlay_video.write(ol_frame)

        print(f"Processed frame {i + 1}/{frame_count}")

    original_video.release()
    afterimage_video.release()
    blended_video.release()
    overlay_video.release()

    print("Videos generated successfully:")
    print("  Original Video:", original_video_path)
    print("  Afterimage Video:", afterimage_video_path)
    print("  Blended Video:", blended_video_path)
    print("  Persistent Overlay Video:", overlay_video_path)


# --- Main Pipeline ---
if __name__ == "__main__":
    # Define paths (update if needed)
    video_path = "data/afterimage/2_video/IMG_1124.mov"
    frames_dir = "data/afterimage/2_video/extracted_frames"
    afterimage_dir = "data/afterimage/2_video/afterimage_frames"
    # The persistent overlay frames are expected to be saved in a subfolder of afterimage_dir:
    persistent_overlay_dir = os.path.join(afterimage_dir, "persistent_overlay")
    videos_dir = "data/afterimage/2_video/output"

    fps_target = 15
    blend_alpha = 0.7

    print("Extracting frames from video...")
    extract_frames(video_path, frames_dir, fps_target)
    print("Generating afterimage and persistent overlay frames using batch processing...")
    generate_afterimage_and_overlay_frames(frames_dir, afterimage_dir)
    print("Generating videos...")
    generate_videos(frames_dir, afterimage_dir, persistent_overlay_dir, videos_dir, fps=fps_target, alpha=blend_alpha)
    print("Video processing pipeline completed!")

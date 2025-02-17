import cv2
import os
import numpy as np


def generate_combined_video(top_folder: str, bottom_folder: str, output_video_path: str, fps: int = 30,
                            slow_factor: int = 3):
    """
    Generate a video that combines two sets of frames vertically and slows down playback.

    Parameters
    ----------
    top_folder : str
        Directory containing the top video frames.
    bottom_folder : str
        Directory containing the bottom video frames.
    output_video_path : str
        File path or directory to save the combined video.
    fps : int
        Base frames per second for the output video.
    slow_factor : int
        Factor to slow down the video by duplicating frames.
    """
    # If the output_video_path is a directory, append a default filename.
    if os.path.isdir(output_video_path):
        output_video_path = os.path.join(output_video_path, "combined_video.mp4")

    # Get sorted list of image files from both folders.
    top_frames = sorted([f for f in os.listdir(top_folder) if f.lower().endswith(('.jpg', '.png'))])
    bottom_frames = sorted([f for f in os.listdir(bottom_folder) if f.lower().endswith(('.jpg', '.png'))])

    if not top_frames or not bottom_frames:
        print("No frames found in one or both folders.")
        return

    # Use the minimum count of frames to ensure synchronization.
    frame_count = min(len(top_frames), len(bottom_frames))

    # Read the first frame from the top folder to determine dimensions.
    first_top_path = os.path.join(top_folder, top_frames[0])
    first_top = cv2.imread(first_top_path)
    if first_top is None:
        print(f"Failed to read the first frame from {first_top_path}.")
        return
    height, width, layers = first_top.shape
    combined_height = height * 2  # Two frames stacked vertically.

    # Set up the video writer.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, combined_height))

    for i in range(frame_count):
        top_path = os.path.join(top_folder, top_frames[i])
        bottom_path = os.path.join(bottom_folder, bottom_frames[i])
        top_frame = cv2.imread(top_path)
        bottom_frame = cv2.imread(bottom_path)

        if top_frame is None or bottom_frame is None:
            print(f"Skipping frame {i} due to a read error.")
            continue

        # Resize bottom frame if dimensions differ (assuming top_frame has desired dimensions).
        if top_frame.shape != bottom_frame.shape:
            bottom_frame = cv2.resize(bottom_frame, (width, height))

        # Stack the frames vertically.
        combined_frame = np.vstack((top_frame, bottom_frame))

        # Write the same frame multiple times to slow down playback.
        for _ in range(slow_factor):
            out.write(combined_frame)

    out.release()
    print(f"Combined video saved to {output_video_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a combined video from two frame folders (top and bottom) with slower playback.")
    parser.add_argument("top_folder", help="Folder containing the top video frames.")
    parser.add_argument("bottom_folder", help="Folder containing the bottom video frames.")
    parser.add_argument("output_video_path", help="File path or directory to save the combined output video.")
    parser.add_argument("--fps", type=int, default=30, help="Base frames per second for the video (default: 30).")
    parser.add_argument("--slow_factor", type=int, default=3, help="Factor to slow down the video (default: 3).")
    args = parser.parse_args()

    generate_combined_video(args.top_folder, args.bottom_folder, args.output_video_path, args.fps, args.slow_factor)
    print("Combined video generation completed!")
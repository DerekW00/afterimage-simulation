import cv2
import os
import numpy as np

def generate_combined_and_separate_videos(top_folder: str, bottom_folder: str, output_video_path: str, fps: int = 30, alpha: float = 0.5):
    """
    Generate a video to show the effect of afterimage by stacking:
    - Top: Original input image.
    - Middle: Afterimage only.
    - Bottom: Input image + afterimage blended together.

    Save the combined video and the three individual videos separately.

    Parameters
    ----------
    top_folder : str
        Directory containing the input frames.
    bottom_folder : str
        Directory containing the afterimage frames.
    output_video_path : str
        File path or directory to save the combined video.
    fps : int
        Frames per second for the video.
    alpha : float
        Blending weight for the input image (0 < alpha <= 1).
        The afterimage gets weight (1 - alpha).
    """
    # If the output path is a directory, add a default filename.
    if os.path.isdir(output_video_path):
        combined_path = os.path.join(output_video_path, "combined_video.mp4")
        original_path = os.path.join(output_video_path, "original_video.mp4")
        afterimage_path = os.path.join(output_video_path, "afterimage_video.mp4")
        combined_with_afterimage_path = os.path.join(output_video_path, "input_with_afterimage_video.mp4")
    else:
        base_path = os.path.dirname(output_video_path)
        combined_path = output_video_path
        original_path = os.path.join(base_path, "original_video.mp4")
        afterimage_path = os.path.join(base_path, "afterimage_video.mp4")
        combined_with_afterimage_path = os.path.join(base_path, "input_with_afterimage_video.mp4")

    # Get sorted list of image files from both folders.
    top_frames = sorted([f for f in os.listdir(top_folder) if f.lower().endswith(('.jpg', '.png'))])
    bottom_frames = sorted([f for f in os.listdir(bottom_folder) if f.lower().endswith(('.jpg', '.png'))])

    if not top_frames or not bottom_frames:
        print("No frames found in one or both folders.")
        return

    frame_count = min(len(top_frames), len(bottom_frames))

    # Read the first frame to determine dimensions.
    first_top = cv2.imread(os.path.join(top_folder, top_frames[0]))
    if first_top is None:
        print("Failed to read the first frame.")
        return
    height, width, layers = first_top.shape
    combined_height = height * 3  # Three stacked frames.

    # Set up video writers for combined and separate videos.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    combined_video = cv2.VideoWriter(combined_path, fourcc, fps, (width, combined_height))
    original_video = cv2.VideoWriter(original_path, fourcc, fps, (width, height))
    afterimage_video = cv2.VideoWriter(afterimage_path, fourcc, fps, (width, height))
    combined_with_afterimage_video = cv2.VideoWriter(combined_with_afterimage_path, fourcc, fps, (width, height))

    for i in range(frame_count):
        top_path = os.path.join(top_folder, top_frames[i])
        bottom_path = os.path.join(bottom_folder, bottom_frames[i])

        top_frame = cv2.imread(top_path)
        bottom_frame = cv2.imread(bottom_path)

        if top_frame is None or bottom_frame is None:
            print(f"Skipping frame {i} due to read error.")
            continue

        # Resize frames if needed.
        if top_frame.shape != bottom_frame.shape:
            bottom_frame = cv2.resize(bottom_frame, (width, height))

        # Generate the combined frame (input + afterimage).
        combined_with_afterimage = cv2.addWeighted(top_frame, alpha, bottom_frame, 1 - alpha, 0)

        # Stack the three frames vertically.
        combined_frame = np.vstack((top_frame, bottom_frame, combined_with_afterimage))

        # Write frames to videos.
        combined_video.write(combined_frame)
        original_video.write(top_frame)
        afterimage_video.write(bottom_frame)
        combined_with_afterimage_video.write(combined_with_afterimage)

    combined_video.release()
    original_video.release()
    afterimage_video.release()
    combined_with_afterimage_video.release()

    print(f"Videos saved to: {combined_path}, {original_path}, {afterimage_path}, {combined_with_afterimage_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a combined video and separate videos for original, afterimage, and combined frames.")
    parser.add_argument("top_folder", help="Folder containing the original video frames.")
    parser.add_argument("bottom_folder", help="Folder containing the afterimage frames.")
    parser.add_argument("output_video_path", help="File path or directory to save the videos.")
    parser.add_argument("--fps", type=int, default=10, help="Frames per second for the videos (default: 10).")
    parser.add_argument("--alpha", type=float, default=0.5, help="Blending factor for combining images (default: 0.5).")
    args = parser.parse_args()

    generate_combined_and_separate_videos(args.top_folder, args.bottom_folder, args.output_video_path, args.fps, args.alpha)
    print("Video generation completed!")

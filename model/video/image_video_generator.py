import os

import cv2
import numpy as np

from model.model_config import ModelConfig
from model.utils.file_utils import list_images


def generate_combined_and_separate_videos(top_folder: str = None,
                                          bottom_folder: str = None,
                                          output_folder: str = None,
                                          fps: int = None,
                                          alpha: float = 0.5,
                                          target_resolution: tuple = None):
    """
    Generate four videos from two sets of frames:
      1. Combined video: three vertically stacked frames (original on top, afterimage in middle, and blended on bottom)
      2. Original video: original frames only.
      3. Afterimage video: afterimage frames only.
      4. Blended video: input frames blended with afterimage frames.

    If any folder parameter is omitted, the defaults from ModelConfig are used.

    Parameters:
      top_folder (str): Directory with original frames.
      bottom_folder (str): Directory with afterimage frames.
      output_folder (str): Directory where videos will be saved.
      fps (int): Frames per second (default from ModelConfig.FPS).
      alpha (float): Blending factor (0 < alpha <= 1) for the blended video.
      target_resolution (tuple): (width, height) to resize frames for the videos.
    """
    if top_folder is None:
        top_folder = ModelConfig.DEFAULT_INPUT_DIR
    if bottom_folder is None:
        bottom_folder = ModelConfig.DEFAULT_OUTPUT_DIR
    if output_folder is None:
        output_folder = ModelConfig.DEFAULT_VIDEO_DIR
    if fps is None:
        fps = ModelConfig.FPS

    os.makedirs(output_folder, exist_ok=True)

    # Build video file paths.
    combined_path = os.path.join(output_folder, "combined_video.mp4")
    original_path = os.path.join(output_folder, "original_video.mp4")
    afterimage_path = os.path.join(output_folder, "afterimage_video.mp4")
    blended_path = os.path.join(output_folder, "blended_video.mp4")

    top_frames = list_images(top_folder)
    bottom_frames = list_images(bottom_folder)
    if not top_frames or not bottom_frames:
        print("No frames found in one or both folders.")
        return

    frame_count = min(len(top_frames), len(bottom_frames))
    first_frame = cv2.imread(os.path.join(top_folder, top_frames[0]))
    if first_frame is None:
        print("Failed to read the first frame from the top folder.")
        return

    # Determine frame dimensions.
    if target_resolution is not None:
        width, height = target_resolution
    else:
        height, width, _ = first_frame.shape

    # Combined video: three frames stacked vertically.
    combined_height = height * 3

    # Use a modern codec (H.264 via 'avc1')
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    combined_video = cv2.VideoWriter(combined_path, fourcc, fps, (width, combined_height))
    original_video = cv2.VideoWriter(original_path, fourcc, fps, (width, height))
    afterimage_video = cv2.VideoWriter(afterimage_path, fourcc, fps, (width, height))
    blended_video = cv2.VideoWriter(blended_path, fourcc, fps, (width, height))

    for i in range(frame_count):
        top_img_path = os.path.join(top_folder, top_frames[i])
        bottom_img_path = os.path.join(bottom_folder, bottom_frames[i])
        top_frame = cv2.imread(top_img_path)
        bottom_frame = cv2.imread(bottom_img_path)
        if top_frame is None or bottom_frame is None:
            print(f"Skipping frame {i} due to read error.")
            continue

        # Resize frames if target resolution is set.
        if target_resolution is not None:
            top_frame = cv2.resize(top_frame, (width, height))
            bottom_frame = cv2.resize(bottom_frame, (width, height))

        # Create blended frame.
        blended_frame = cv2.addWeighted(top_frame, alpha, bottom_frame, 1 - alpha, 0)
        # Create combined frame by stacking original, afterimage, and blended frames.
        combined_frame = np.vstack((top_frame, bottom_frame, blended_frame))

        combined_video.write(combined_frame)
        original_video.write(top_frame)
        afterimage_video.write(bottom_frame)
        blended_video.write(blended_frame)

    combined_video.release()
    original_video.release()
    afterimage_video.release()
    blended_video.release()

    print("Videos saved to:")
    print("  Combined video:", combined_path)
    print("  Original video:", original_path)
    print("  Afterimage video:", afterimage_path)
    print("  Blended video:", blended_path)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate four videos from original and afterimage frame sequences.")
    parser.add_argument("--top_folder", default=ModelConfig.DEFAULT_INPUT_DIR,
                        help="Folder containing original frames (default: ModelConfig.DEFAULT_INPUT_DIR)")
    parser.add_argument("--bottom_folder", default=ModelConfig.DEFAULT_OUTPUT_DIR,
                        help="Folder containing afterimage frames (default: ModelConfig.DEFAULT_OUTPUT_DIR)")
    parser.add_argument("--output_folder", default=ModelConfig.DEFAULT_VIDEO_DIR,
                        help="Folder to save generated videos (default: ModelConfig.DEFAULT_VIDEO_DIR)")
    parser.add_argument("--fps", type=int, default=ModelConfig.FPS,
                        help="Frames per second (default: ModelConfig.FPS)")
    parser.add_argument("--alpha", type=float, default=0.5,
                        help="Blending factor for the blended video (default: 0.5)")
    parser.add_argument("--width", type=int, default=None, help="Target frame width (optional)")
    parser.add_argument("--height", type=int, default=None, help="Target frame height (optional)")
    args = parser.parse_args()

    target_resolution = None
    if args.width is not None and args.height is not None:
        target_resolution = (args.width, args.height)

    generate_combined_and_separate_videos(args.top_folder, args.bottom_folder, args.output_folder, args.fps, args.alpha,
                                          target_resolution)


if __name__ == "__main__":
    main()

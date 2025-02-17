import numpy as np
import cv2
import os
from model.receptor_kinetics import update_opsin_concentration
from model.utils import read_image_color, save_image

def process_frame_sequence(input_folder: str, output_folder: str, params: dict):
    print(f"Starting color afterimage processing...")
    os.makedirs(output_folder, exist_ok=True)

    frame_files = sorted([f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.png'))])
    if not frame_files:
        print("No valid images found!")
        return

    opsin = None

    for i, frame_file in enumerate(frame_files):
        input_path = os.path.join(input_folder, frame_file)
        output_path = os.path.join(output_folder, frame_file)

        # Read as a color image
        frame = read_image_color(input_path)
        if opsin is None:
            opsin = np.ones_like(frame)

        ca, cd, dt = params['ca'], params['cd'], params['dt']
        for _ in range(params['iterations']):
            for c in range(3):  # Apply photoreceptor kinetics to each color channel
                opsin[:, :, c] = update_opsin_concentration(opsin[:, :, c], frame[:, :, c], ca=ca, cd=cd, dt=dt)

        afterimage = np.clip(1.0 - opsin, 0, 1) * params['intensity']
        output_frame = (afterimage * 255).astype(np.uint8)

        save_image(output_path, output_frame)
        print(f"Processed color frame {i+1}/{len(frame_files)}: {output_path}")

    print("Color afterimage batch processing completed!")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Apply afterimage effects to a sequence of frames.")
    parser.add_argument("input_folder", help="Path to the folder containing input frames.")
    parser.add_argument("output_folder", help="Path to save the processed frames.")
    args = parser.parse_args()

    # Define default model parameters (can be adjusted as needed)
    params = {
        'intensity': 2.0,
        'ca': 0.4,
        'cd': 0.2,
        'dt': 0.05,
        'iterations': 20
    }

    # Run the frame sequence processor
    process_frame_sequence(args.input_folder, args.output_folder, params)

    print("Frame sequence processing complete!")
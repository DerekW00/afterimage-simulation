# Photoreceptor Eye Model

A Python-based simulation of human photoreceptor responses that models afterimage effects and HDR radiance processing.  
This project is inspired by seminal work in visual perception (e.g., Ritschel & Eisemann, 2012) and includes recent
enhancements to simulate persistent afterimage overlays and color-specific responses.

## Table of Contents

- About the Project
- Getting Started
    - Prerequisites
    - Installation
- Usage
    - Image Processing
    - Video Processing Pipeline
- Project Structure
- Contributing
- License
- Contact
- Acknowledgments

## About the Project

This project simulates photoreceptor responses in the human eye with a focus on afterimage effects. It includes:

- Core modeling of photoreceptor kinetics and anatomical constraints.
- Afterimage simulation that generates color afterimages rather than simple greyscale inversions.
- A video processing pipeline that extracts frames from an input video, applies afterimage processing (with a persistent
  overlay that blends the previous frame's afterimage onto the current frame), and compiles four distinct videos:
    1. Original video (raw frames)
    2. Afterimage video (processed frames)
    3. Blended video (a weighted blend of original and afterimage)
    4. Persistent overlay video (each frame shows the current original overlaid with the previous frame’s afterimage)

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Virtual environment tool (e.g., `venv`)
- OpenCV, NumPy, and other dependencies listed in `requirements.txt`

### Installation

1. Clone the Repository:

```
git clone https://github.com/derekw00/photoreceptor-eye-model.git
cd photoreceptor-eye-model
```

2. Create and Activate a Virtual Environment:

```
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install Dependencies:

```
pip install -r requirements.txt
```

4. Install the Package in Editable Mode (optional but recommended):

```
pip install -e .
```

## Usage

### Image Processing

To run a basic afterimage simulation on a single image:

```
python -m model.processing.afterimage path/to/input_image.jpg path/to/output_image.jpg
```

This command processes the input image using the photoreceptor kinetics model and generates an afterimage.

### Video Processing Pipeline

The project now includes a comprehensive video pipeline that:

1. Extracts frames from a given video.
2. Generates afterimage frames (using our afterimage model with persistent overlay).
3. Compiles four videos:
    - Original video: the raw extracted frames.
    - Afterimage video: frames processed with the afterimage model.
    - Blended video: each frame is a blend of the original and its corresponding afterimage.
    - Persistent overlay video: each frame is the current original frame overlaid with the previous frame’s afterimage.

To run the full video pipeline, use the provided script:

```
python -m model.video.process_video_pipeline
```

This script (located in `model/video/process_video_pipeline.py`) assumes your input video is located at
`data/afterimage/2_video/IMG_1124.mov` and uses default directories (set in `model/model_config.py`) for frame
extraction, afterimage processing, and video output. You can adjust these paths or override them via command-line
arguments if necessary.

## Project Structure

```
photoreceptor-eye-model/
├── docs/
├── model/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── anatomical.py
│   │   ├── hdr_processing.py
│   │   ├── photoreceptor_model.py
│   │   └── receptor_kinetics.py
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── afterimage.py
│   │   ├── afterimage_batch.py
│   │   ├── afterimage_batch_pysilsub.py
│   │   └── image_generator.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_utils.py
│   │   ├── pysilsub_integration.py
│   │   └── visualization.py
│   ├── video/
│   │   ├── __init__.py
│   │   ├── extract_video.py
│   │   ├── image_video_generator.py
│   │   └── process_video_pipeline.py
│   └── model_config.py
├── notebooks/
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

## Contributing

Contributions are welcome! Please fork the repository, create a new branch for your feature or fix, and submit a pull
request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Derek Derui Wang

- Email: derekderuiwang@gmail.com
- LinkedIn: [Profile](https://www.linkedin.com/in/derek-w)

## Acknowledgments

- Ritschel & Eisemann (2012) for foundational research on afterimage simulation.
- OpenCV and NumPy for computer vision and numerical operations.
- The pysilsub library for perceptual modeling.


class ModelConfig:
    # Photoreceptor kinetics parameters (for L, M, S cones)
    CA_RGB = (0.2, 0.3, 0.5)
    CD_RGB = (0.1, 0.15, 0.2)

    # Simulation parameters
    TIME_STEP = 0.05
    ITERATIONS = 20
    INTENSITY = 2.0

    # Default I/O directories (adjust as needed)
    DEFAULT_INPUT_DIR = "data/afterimage/1_batch_prototype/input"
    DEFAULT_OUTPUT_DIR = "data/afterimage/1_batch_prototype/output"
    DEFAULT_VIDEO_DIR = "data/afterimage/1_batch_prototype/videos"

    # Video settings
    FPS = 10
    ALPHA_BLEND = 0.5

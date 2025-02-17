# Photoreceptor Eye Model
A Python-based simulation of human photoreceptor responses, inspired by key research in visual perception.

## Table of Contents

- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

## About the Project

This project simulates photoreceptor responses in the human eye, focusing on afterimage effects and HDR radiance processing. It draws inspiration from the works of Ritschel & Eisemann (2012) and other seminal research in the field.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Virtual environment tool (e.g., `venv`)

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/derekw00/photoreceptor-eye-model.git
   cd photoreceptor-eye-model
   ```
2. **Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the afterimage simulation:

```bash
python -m model.afterimage data/afterimage/0_1_frame_prototype/input/0.jpg data/afterimage/0_1_frame_prototype/output/0.jpg
```

Replace `0.jpg` with your desired input image.

## Project Structure

```plaintext
photoreceptor-eye-model/
├── model/
│   ├── afterimage.py
│   ├── photoreceptor.py
│   ├── hdr_processing.py
│   ├── anatomical.py
│   ├── receptor_kinetics.py
│   ├── utils.py
│   └── visualization.py
├── notebooks/
├── tests/
├── data/
│   ├── afterimage/
│   │   ├── input/
│   │   └── output/
├── setup.py
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Derek Derui Wang 
- [derekderuiwang@gmail.com](mailto:derekderuiwang@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/derekderuiwang/)

## Acknowledgments

- Ritschel & Eisemann (2012) for their foundational work on afterimage simulation.
- [Other references or inspirations]
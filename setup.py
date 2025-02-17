from setuptools import setup, find_packages

setup(
    name='photoreceptor-eye-model',
    version='0.1.0',  # Initial version
    description='A Python implementation of a photoreceptor model for afterimage simulation and eye dynamics.',
    author='Derek W.',
    author_email='derekderuiwang@gmail.com',
    url='https://github.com/DerekW00/photoreceptor-eye-model',
    packages=find_packages(where='.'),  # Automatically find all packages
    package_dir={'': '.'},  # Packages are located in the current directory
    include_package_data=True,
    install_requires=[
        'numpy>=1.21.0',
        'opencv-python>=4.5.0',
        'matplotlib>=3.4.0',
    ],
    entry_points={
        'console_scripts': [
            'afterimage-sim=model.afterimage:main',
            'photoreceptor-sim=model.photoreceptor:main',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
    python_requires='>=3.9',
)

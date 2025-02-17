from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='photoreceptor-eye-model',
    version='0.1.0',
    description='A Python implementation of a photoreceptor model for afterimage simulation and eye dynamics.',
    author='Derek W.',
    author_email='derekderuiwang@gmail.com',
    url='https://github.com/DerekW00/photoreceptor-eye-model',
    packages=find_packages(where='.'),
    package_dir={'': '.'},
    include_package_data=True,
    install_requires=requirements,  # Automatically populate from requirements.txt
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
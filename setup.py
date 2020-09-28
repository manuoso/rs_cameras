# python3.8
from setuptools import setup, find_packages

setup(
    name='rscameras',
    version='0.0.1',
    description='Python wrapper for Intel Realsense cameras',
    url='https://github.com/manuoso/rs_cameras',
    author='Manuel Perez Jimenez',
    author_email='manuperezj@gmail.com',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: GNU GPL",
        "Operating System :: OS Independent",
    ],
)

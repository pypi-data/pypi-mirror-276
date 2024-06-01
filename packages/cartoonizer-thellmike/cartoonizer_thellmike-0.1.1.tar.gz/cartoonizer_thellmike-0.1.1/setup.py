from setuptools import setup, find_packages

setup(
    name='cartoonizer-thellmike',
    version='0.1.1',  # Incremented version number
    description='A library for converting normal pictures to cartoon-like images',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sachin Harshitha',
    author_email='sachinharshitha971@gmail.com',
    url='https://github.com/thelllmike/cartoonizer.git',
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'numpy',
        'opencv-python',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

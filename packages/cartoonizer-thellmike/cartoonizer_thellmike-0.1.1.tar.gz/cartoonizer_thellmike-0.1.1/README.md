# Cartoonizer

Cartoonizer is a Python library that converts normal pictures into cartoon-like images.

## Installation

To install the library, use pip:

```sh
pip install cartoonizer-thellmike
```

## Project Structure

Ensure your project directory looks like this:

```
my_project/
├── input_image.jpg
├── output_image.png
├── use_cartoonizer.py
└── venv/  # Optional, if you are using a virtual environment
```

## Usage

Create a Python script named `use_cartoonizer.py` and add the following code:

```python
from cartoonizer import apply_cartoon_effect

# Path to the input image
input_image_path = 'input_image.jpg'

# Path to save the output cartoon image
output_image_path = 'output_image.png'

# Apply the cartoon effect
apply_cartoon_effect(input_image_path, output_image_path)

print(f"Cartoon effect applied and saved to {output_image_path}")
```

## Running the Script

Make sure you have an image named `input_image.jpg` in the same directory or provide the correct path to an image.

```sh
from cartoonizer import apply_cartoon_effect

# Path to the input image
input_image_path = 'input_image.jpg'

# Path to save the output cartoon image
output_image_path = 'output_image.png'

# Apply the cartoon effect
apply_cartoon_effect(input_image_path, output_image_path)

print(f"Cartoon effect applied and saved to {output_image_path}")
```

Run the script:

```sh
python use_cartoonizer.py
```


from PIL import Image, ImageOps, ImageFilter

def preprocess_image(image_path):
    image = Image.open(image_path).convert('RGB')
    image = image.filter(ImageFilter.MedianFilter(7))  # Apply median blur
    return image

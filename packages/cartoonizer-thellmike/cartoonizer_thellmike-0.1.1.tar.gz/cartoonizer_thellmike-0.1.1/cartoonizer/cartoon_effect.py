from PIL import Image
import numpy as np
import cv2
from .preprocessing import preprocess_image
from .edge_detection import detect_edges
from .color_quantization import color_quantization

def apply_cartoon_effect(image_path, output_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    
    # Detect edges
    edges = detect_edges(preprocessed_image)
    
    # Apply color quantization
    quantized_image = color_quantization(np.array(preprocessed_image))
    
    # Combine edges and quantized image
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    cartoon_image = cv2.bitwise_and(quantized_image, edges_colored)
    
    # Save the result
    result_image = Image.fromarray(cartoon_image)
    result_image.save(output_path)

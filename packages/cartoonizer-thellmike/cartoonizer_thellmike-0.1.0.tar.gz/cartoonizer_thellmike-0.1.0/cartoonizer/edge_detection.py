import cv2
import numpy as np

def detect_edges(image):
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    edges = cv2.adaptiveThreshold(cv2.medianBlur(gray_image, 5), 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 2)
    return edges

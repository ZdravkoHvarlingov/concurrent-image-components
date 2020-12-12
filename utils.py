import random
import numpy as np


def are_lab_colors_similar(pixel1, pixel2):
    # h0 = int(pixel1[0])
    # h1 = int(pixel2[0])
    # hueDistance = abs(h1-h0) # min(abs(h1-h0), 179-abs(h1-h0));
    
    # return hueDistance < 2
    pixel1 = pixel1.astype('int32')
    pixel2 = pixel2.astype('int32')
    distance = np.linalg.norm(pixel1-pixel2)
    return distance < 10


def is_cell_inside_image(row, col, image):
    return (row >= 0 
            and row < image.shape[0] 
            and col >= 0
            and col < image.shape[1])


def cell_to_linear_index(row, col, image):
    rows = image.shape[0]
    cols = image.shape[1]

    return row * cols + col


def linear_index_to_cell(index, image):
    rows = image.shape[0]
    cols = image.shape[1]

    return (index // cols, index % cols)


def generate_random_hsv_color():
    #HSV in opencv (0-179, 0-255, 0-255)
    return [random.randint(0, 179), random.randint(0, 255), random.randint(0, 255)]

def generate_random_lab_color():
    #LAB in opencv (0-255, 0-255, 0-255)
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

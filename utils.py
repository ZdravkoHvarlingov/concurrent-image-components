import random
import numpy as np


def are_grayscale_colors_similar(pixel1, pixel2):
    pixel1 = int(pixel1)
    pixel2 = int(pixel2)
    return abs(pixel1 - pixel2) < 6


def is_cell_inside_region(row, col, row_min, row_max, col_min, col_max):
    return (row >= row_min
            and row <= row_max
            and col >= col_min
            and col <= col_max)

def cell_to_linear_index(row, col, image):
    rows = image.shape[0]
    cols = image.shape[1]

    return row * cols + col


def linear_index_to_cell(index, image):
    rows = image.shape[0]
    cols = image.shape[1]

    return (index // cols, index % cols)


def generate_random_rgb_color():
    #RGB in opencv (0-255, 0-255, 0-255)
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

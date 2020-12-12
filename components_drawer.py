import cv2
import utils
import numpy as np
from components_finder import ComponentsFinder


class ComponentsDrawer:
    
    def __init__(self):
        pass
    
    def draw_and_save(self, image_path):
        numpy_image = cv2.imread(image_path)
        numpy_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2HSV)

        components_finder = ComponentsFinder(1)
        components = components_finder.find_components(numpy_image)

        color_map = dict()
        rows = numpy_image.shape[0]
        cols = numpy_image.shape[1]
        for row in range(rows):
            for col in range(cols):
                linear_index = utils.cell_to_linear_index(row, col, numpy_image)
                numpy_image[row][col] = np.array(self.get_color(color_map, components[linear_index]))
        
        numpy_image = cv2.cvtColor(numpy_image, cv2.COLOR_HSV2BGR)
        image_name = image_path.split('/')[-1]
        cv2.imwrite(f'results/{image_name}', numpy_image)

    def get_color(self, color_map, component_id):
        if color_map.get(component_id, None) is None:
            color_map[component_id] = utils.generate_random_lab_color()
        
        return color_map[component_id]

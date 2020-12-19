import cv2
import utils
import numpy as np
from components_finder import ComponentsFinder


class ComponentsDrawer:
    
    MIN_PIXELS_INSIDE_COMPONENT = 10

    def __init__(self):
        pass
    
    def draw_and_save(self, image_path):
        numpy_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        components_finder = ComponentsFinder(4, numpy_image)
        components = components_finder.find_components()
        comp_count = self.component_counter(components)

        color_map = dict()
        rows = numpy_image.shape[0]
        cols = numpy_image.shape[1]
        result_rgb_image = np.zeros(shape=(rows, cols, 3))
        for row in range(rows):
            for col in range(cols):
                linear_index = utils.cell_to_linear_index(row, col, numpy_image)
                if comp_count.get(components[linear_index], 0) > ComponentsDrawer.MIN_PIXELS_INSIDE_COMPONENT:
                    result_rgb_image[row][col] = np.array(self.get_color(color_map, components[linear_index]))
        
        print(f'Number of components: {len(color_map)}')
        image_name = image_path.split('/')[-1]
        cv2.imwrite(f'results/grayscale_{image_name}', numpy_image)
        cv2.imwrite(f'results/{image_name}', result_rgb_image)


    def get_color(self, color_map, component_id):
        if color_map.get(component_id, None) is None:
            color_map[component_id] = utils.generate_random_rgb_color()
        
        return color_map[component_id]
    
    def component_counter(self, components):
        comp_count = dict()
        for comp in components:
            comp_count[comp] = comp_count.get(comp, 0) + 1

        return comp_count

from union_find import UnionFind
import utils
import time


class ComponentsFinder:
    def __init__(self, number_of_thread: int):
        self._number_of_threads = number_of_thread

    def find_components(self, image):
        start = time.time()

        components = UnionFind(image.shape[0] * image.shape[1])
        rows = image.shape[0]
        cols = image.shape[1]

        row_move = [0, 1, 0, -1]
        col_move = [1, 0, -1, 0]
        for row in range(rows):
            for col in range(cols):
                for move in range(len(row_move)):
                    new_row = row + row_move[move]
                    new_col = col + col_move[move]

                    if (utils.is_cell_inside_image(new_row, new_col, image)
                        and utils.are_lab_colors_similar(image[row][col], image[new_row][new_col])):
                            components.union(utils.cell_to_linear_index(row, col, image), utils.cell_to_linear_index(new_row, new_col, image))
        
        components.compress_paths()

        end = time.time()
        print(f'Components finding execution time: {(end - start)}')

        return components.parents

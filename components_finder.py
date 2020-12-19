from union_find import UnionFind
import utils
import time
import threading


class ComponentsFinder:

    def __init__(self, number_of_thread: int, image):
        self._number_of_threads = number_of_thread
        self._image = image
        self._components = UnionFind(image.shape[0] * image.shape[1])
        self._ready_flags = [False for _ in range(number_of_thread)]
        self._locks = [threading.Lock() for _ in range(number_of_thread)]
        self._construct_thread_regions()

    def _construct_thread_regions(self):
        columns = self._image.shape[1]
        number_of_thread_cols = columns // self._number_of_threads

        self._thread_regions = [(0, 0) for num in range(self._number_of_threads)]
        for thread_num in range(self._number_of_threads - 1):
            self._thread_regions[thread_num] = (thread_num * number_of_thread_cols, (thread_num + 1) * number_of_thread_cols - 1)

        self._thread_regions[self._number_of_threads - 1] = ((self._number_of_threads - 1) * number_of_thread_cols, columns - 1)

    def _loop_until_ready(self, waiting_thread, waited_thread):
        print(f'Thread {waiting_thread} starts waiting thread {waited_thread}')
        start = time.time()
        self._locks[waited_thread].acquire()
        end = time.time()
        print(f'Thread {waiting_thread} waited for thread {waited_thread} for {(end - start)} seconds.')

    def _merge_regions(self, factor, merge_col, thread_num):
        start_col = self._thread_regions[thread_num][0]
        end_col = self._thread_regions[thread_num][1]
        print(f'Thread {thread_num} executing in the column range {start_col} - {end_col}.')
        start = time.time()

        rows = self._image.shape[0]

        row_move = [-1, 0, 1]
        col_move = [1, 1, 1]
        for row in range(rows):
            for move in range(len(row_move)):
                    new_row = row + row_move[move]
                    new_col = merge_col + col_move[move]
                    if (utils.is_cell_inside_region(new_row, new_col, 0, rows - 1, start_col, end_col)
                        and utils.are_grayscale_colors_similar(self._image[row][merge_col], self._image[new_row][new_col])):
                            self._components.union(utils.cell_to_linear_index(row, merge_col, self._image), utils.cell_to_linear_index(new_row, new_col, self._image)) 

        end = time.time()
        print(f'Thread {thread_num} components finding execution time: {(end - start)}')

        merge_thread = thread_num + factor // 2
        if thread_num % factor != 0 or merge_thread >= self._number_of_threads:
            print(f'Thread {thread_num} finished execution.')
            self._ready_flags[thread_num] = True
            self._locks[thread_num].release()
            return

        self._loop_until_ready(thread_num, merge_thread)
        self._thread_regions[thread_num] = (start_col, self._thread_regions[merge_thread][1])
        self._merge_regions(factor * 2, end_col, thread_num)

    def _construct_components(self, factor, thread_num):
        self._locks[thread_num].acquire()
        start_col = self._thread_regions[thread_num][0]
        end_col = self._thread_regions[thread_num][1]
        print(f'Thread {thread_num} executing in the column range {start_col} - {end_col}.')
        start = time.time()

        rows = self._image.shape[0]

        row_move = [0, 1, 0, -1, -1, -1, 1, 1]
        col_move = [1, 0, -1, 0, -1, 1, 1, -1]

        for row in range(rows):
            for col in range(start_col, end_col + 1):
                for move in range(len(row_move)):
                    new_row = row + row_move[move]
                    new_col = col + col_move[move]
                    if (utils.is_cell_inside_region(new_row, new_col, 0, rows - 1, start_col, end_col)
                        and utils.are_grayscale_colors_similar(self._image[row][col], self._image[new_row][new_col])):
                            self._components.union(utils.cell_to_linear_index(row, col, self._image), utils.cell_to_linear_index(new_row, new_col, self._image))
        
        end = time.time()
        print(f'Thread {thread_num} components finding execution time: {(end - start)}')

        merge_thread = thread_num + factor // 2
        if thread_num % factor != 0 or merge_thread >= self._number_of_threads:
            print(f'Thread {thread_num} finished execution.')
            self._ready_flags[thread_num] = True
            self._locks[thread_num].release()
            return
        self._loop_until_ready(thread_num, merge_thread)
        self._thread_regions[thread_num] = (start_col, self._thread_regions[merge_thread][1])
        self._merge_regions(factor * 2, end_col, thread_num)

    def find_components(self):
        if any(self._ready_flags):
            return self._components.parents

        start = time.time()
        threads = []
        for thread_num in range(self._number_of_threads):
            thread = threading.Thread(target=self._construct_components, args=(2, thread_num))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        self._components.compress_paths()

        end = time.time()
        print(f'Components finding execution time: {(end - start)}')
        print(f'Flags: {self._ready_flags}')

        return self._components.parents

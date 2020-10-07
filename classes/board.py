from time import sleep
from classes.cell import Cell
from utils.helper import print_cell


class Board:
    """
        A class representing board on which cells are spawn.
        The board is rendered by RED '+' signs and GREEN 'O' characters.

        Attributes
        ----------
        active_cells : dict
            The dictionary which contains tuples with active cells coordinates as the key
            and instance of the Cell class as the value.
        active_cells_candidates : dict
            The dictionary which contains tuples with coordinates of cells, which possibly can be 
            active cells in the next stage as the key and instance of the Cell class as the value.
        iteration : int
            The number of iteration of the Game Of Life.
        offset : int
            The minimal distance between the edge of the rendered board and the outermost active cell.
        border_position : dict
            The absolute position of each edge of the rendered board from the previous step
        SLEEP_TIME : float
            Time in seconds for how long should game sleep between iterations.
    """

    def __init__(self, active_cells, offset):
        self.active_cells = active_cells
        self.iteration = 0

        self.offset = offset
        self.border_position = {
            'top': offset,
            'right': offset,
            'bottom': offset,
            'left': offset
        }

        self.SLEEP_TIME = 0.5

    def remove_dead_cells(self, cells):
        """
            Apply move() method from Cell class to each Cell object in cells dictionary.
            If cell in the next step will be dead, remove its key from the dictionary.
        """

        cells_copy = cells.copy()
        for coordinates, cell in cells_copy.items():
            cell.move()
            if not cell.is_active:
                del cells[coordinates]                

    def calculate_next_step(self, cells, candidates=True):
        """
            For every cell in `self.active_cells` and `self.active_cells_candidates take their closest surroundings.
            - If the active cell has coordinates (3, 2), the surrounding elements for discussion will have coordinates:
              (2, 1), (3, 1), (4, 1), (3, 1), (3, 3) etc. but NOT (3, 2).
            - If there is an active cell on discussed coordinates, inrement the number of its neighbours. Otherwise,
              if we are discussing the surroundings of the cells which belong to `self.active_cells dictionary`, mark
              the coordinates as possible active cell for the next iteration due to one of the rules of the Game Of Life.
        """

        for coordinates, cell in cells.items():
            for y in range(cell.pos_y - 1, cell.pos_y + 2):
                for x in range(cell.pos_x - 1, cell.pos_x + 2):
                    if (x, y) == coordinates:
                        continue

                    if (x, y) in self.active_cells:
                        cell.number_of_neighbours += 1
                    elif candidates:
                        self.active_cells_candidates[(x, y)] = Cell(x, y, False, 0)

    def prepare_for_next_step(self):
        """
            Set critical parametres to their initial states:
            - Number of neighbours of each cell should be `0` before calculating the next step.
            - Active cell candidates dictionary should be empty before calculating the next step. 
        """

        for cell in self.active_cells.values():
            cell.number_of_neighbours = 0

        self.active_cells_candidates = {}

    def merge_active_cells(self):
        """
            Merge actual active cells with the active cell candidates.
            Increment the number of iteration.
        """

        self.active_cells.update(self.active_cells_candidates)
        self.iteration += 1

    def render_board(self):
        """
            Method which renders the board based on the positions of active cells and the minimal
            offset from the outermost cells. (To actually see the motion of the cells.)
        """

        # Print the number of current iteration
        print(f'\nIteration number: {self.iteration}')

        # Get the minimal and maximal coordinates in each axis
        # If the ValueError is raised -> there is no active cell, and the population exctint
        try:
            x_min = min(self.active_cells.keys(), key=lambda x: x[0])[0]
            x_max = max(self.active_cells.keys(), key=lambda x: x[0])[0]
            y_min = min(self.active_cells.keys(), key=lambda x: x[1])[1]
            y_max = max(self.active_cells.keys(), key=lambda x: x[1])[1]
        except ValueError:
            # Render board with RED '+' sign with the same dimensions as in iteration before
            for _ in range(self.border_position['top'], self.border_position['bottom'] + 1):
                for _ in range(self.border_position['left'], self.border_position['right'] + 1):
                    print_cell('dead')
                print()
            exit()

        # Count the offset, to see the motion.
        # We do not want to shrink the distance from the border compared to the iteration before
        if y_min - self.offset < self.border_position['top']:
            self.border_position['top'] = y_min - self.offset
        if y_max + self.offset > self.border_position['bottom']:
            self.border_position['bottom'] = y_max + self.offset
        if x_min - self.offset < self.border_position['left']:
            self.border_position['left'] = x_min - self.offset
        if x_max + self.offset > self.border_position['right']:
            self.border_position['right'] = x_max + self.offset

        # Render the board based on positions of active cells
        for y in range(self.border_position['top'], self.border_position['bottom'] + 1):
            for x in range(self.border_position['left'], self.border_position['right'] + 1):
                print_cell('active') if (x, y) in self.active_cells else print_cell('dead')
            print()

    def play(self):
        """Method which starts the simulation."""

        while True:
            self.render_board()
            self.prepare_for_next_step()
            self.calculate_next_step(self.active_cells)
            self.calculate_next_step(self.active_cells_candidates, candidates=False)

            self.remove_dead_cells(self.active_cells)
            self.remove_dead_cells(self.active_cells_candidates)

            self.merge_active_cells()

            sleep(self.SLEEP_TIME)

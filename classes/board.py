# The 1st version of the Game Of Life -> Fixed board size


import re

from time import sleep
from classes.cell import Cell


class Board:

    def __init__(self, init_cells_coord):
        self.width = 20
        self.height = 20

        self.init_cells_coord = init_cells_coord

    def step_zero(self):
        """Method which initialize the board, based on initial coordninations of cells which are alive"""

        self.cells = [[Cell(row, col, False, 0) for row in range(self.width)] for col in range(self.height)]
        for init_cell in self.init_cells_coord:
            pos_x = init_cell[0]
            pos_y = init_cell[1]
            self.cells[pos_y][pos_x].is_alive = True

        self.render_board()

    def move_cells(self):
        """Apply move() method from Cell class to each Cell object in self.cells 2D list"""

        for row in self.cells:
            for cell in row:
                cell.move()

        self.render_board()

    def count_neighbours(self):
        """Method which iteratively goes through `self.cells` 2D list and count adjacent cells which are alive"""

        for row in self.cells:
            for cell in row:
                # clean counter each round
                cell.number_of_neighbours = 0
                # X and Y coordinates of each Cell object
                x_cell_pos = cell.pos_x
                y_cell_pos = cell.pos_y
                # The tuples describing the surrounding of each Cell object which should be inspected
                x_neigh_range = (x_cell_pos - 1 if x_cell_pos > 0 else 0, x_cell_pos + 2 if x_cell_pos < self.width - 1 else self.width)
                y_neigh_range = (y_cell_pos - 1 if y_cell_pos > 0 else 0, y_cell_pos + 2 if y_cell_pos < self.height - 1 else self.height)
                for x_neigh_pos in range(*x_neigh_range):
                    for y_neigh_pos in range(*y_neigh_range):
                        # If the coordinates equals, that's the same Cell object
                        if x_neigh_pos == x_cell_pos and  y_neigh_pos == y_cell_pos:
                            continue

                        # If the neighbour cell is alive, increment neighbours counter of current cell
                        if self.cells[y_neigh_pos][x_neigh_pos].is_alive:
                            cell.number_of_neighbours += 1

    def render_board(self):
        """Render board with '+' and 'O' characters dependent on each cell's live status"""

        print(' ' + '_'*self.width + ' ')
        for row in self.cells:
            print('|', end='')
            for cl in row:
                cl.print_cell()
            print('|')
        print(' ' + '_'*self.width + ' ')

    def play(self):
        """Method which starts simulation."""

        self.step_zero()
        sleep(0.5)

        while True:
            self.count_neighbours()
            self.move_cells()

            sleep(0.5)

    @staticmethod
    def load_data_from_file(file_path):
        """Load tuples from file and return them as list of tuples for further processing."""
        default_coord = [(7, 6),
                         (7, 7),
                         (7, 8),
                         (6, 7),
                         (5, 8)]

        try:
            with open(file_path, 'r') as input_file:
                # Parse coordinates tuples from input file
                # If tuples was not found, or the path to file is wrong,
                # return default coordinates
                content = input_file.read()
                pattern = r'\(\d+, \d+\)'
                matches = re.findall(pattern, content)
                try:
                    return map(eval, matches)
                except TypeError as e:
                    print(f'Provided file with bad / wrong formatting. Returning the default cell coordinates.') 
                    return default_coord               
        except FileNotFoundError:
            print('Couldn\'t find file on desired path. Returning the default cell coordinates.')
            return default_coord
    
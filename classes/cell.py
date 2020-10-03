class Cell:

    def __init__(self, pos_x, pos_y, is_alive, number_of_neighbours):
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.is_alive = is_alive
        self.number_of_neighbours = number_of_neighbours

    def move(self):
        """
            Make move of cell, based on rules of Game Of Life.
            For more info check https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
        """

        if self.is_alive:
            if self.number_of_neighbours not in [2, 3]:
                self.is_alive = False
        else:
            if self.number_of_neighbours == 3:
                self.is_alive = True

    def print_cell(self):
        """
            Print GREEN 'O' for cells which are alive.
            Otherwise print RED '+'.
        """

        print('\033[92mO\033[00m', end='') if self.is_alive else print('\033[91m+\033[00m', end='')

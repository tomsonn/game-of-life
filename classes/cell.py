class Cell:
    """
        A class representing the living entity of the Game Of Life

        Attributes
        ----------
        pos_x : int
            X coordinate of the cell
        pos_y : int
            Y coordinate of the cell
        is_active : bool
            Status of the cell if it should be rendered during next iteration or not
        number_of_neighbours : int
            The number of living neighbours of the cell. It indicates wheter during next iteration
            cell should be dead or alive
    """

    def __init__(self, pos_x, pos_y, is_active, number_of_neighbours):
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.is_active = is_active
        self.number_of_neighbours = number_of_neighbours

    def move(self):
        """
            Set the status of the cell for next iteration, based on the rules of Game Of Life.
            For more info check https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
        """

        if self.is_active:
            if self.number_of_neighbours not in [2, 3]:
                self.is_active = False
        else:
            if self.number_of_neighbours == 3:
                self.is_active = True

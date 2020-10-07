#!/usr/bin/env python3


import click

from classes.board import Board
from utils.helper import load_data_from_file

@click.command()
@click.option('--file', '-f',
              type=str,
              required=True,
              help="""Path to the file with cells coordinations initialized in step zero.
                      Should be in format: [(x1, y1), (x2, y2), ..., (xn, yn)])""")
def run(file):
    init_cells = load_data_from_file(file) # Parsed coordinates of active cells during the "step zero"
    offset = 5 # The minimal distance between the outermosts active cells and the edge of the board
    board = Board(init_cells, offset)
    board.play()

if __name__ == '__main__':
    run()

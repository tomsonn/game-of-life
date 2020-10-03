#!/usr/bin/env python3


import click

from classes.board import Board

@click.command()
@click.option('--file', '-f',
              type=str,
              required=True,
              help="""Path to the file with cells coordinations initialized in step zero.
                      Should be in format: [(x1, y1), (x2, y2), ..., (xn, yn)])""")
def run(file):
    init_cells = Board.load_data_from_file(file)
    board = Board(init_cells)
    board.play()

if __name__ == '__main__':
    run()

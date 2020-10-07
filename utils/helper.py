import re

from classes.cell import Cell


class BadInitCoordinatesError(Exception):
    """
        Exception class is raised, when the input file does not contain
        coordinates in valid format or the file is empty.
    """

    def __init__(self):
        self.message = 'Coordinates red from input file are not in valid format. Returning the default cell coordinates.'
        super().__init__(self.message)

def load_data_from_file(file_path):
    """
        Load coordinates as tuples from the input file and return the dictionary.
        If the dictionary is empty, use the default coordinates instead.
    """

    default_coordinates = '[(7, 6), (7, 7), (7, 8), (6, 7), (5, 8)]'

    try:
        with open(file_path, 'r') as input_file:
            content = input_file.read()
            return get_dict_of_coordinates_from_string(content)
    except BadInitCoordinatesError as e:
        print(e)
    except FileNotFoundError:
        print('Couldn\'t find file on desired path. Returning the default cell coordinates.')

    return get_dict_of_coordinates_from_string(default_coordinates)

def get_dict_of_coordinates_from_string(coordinates_list_string):
    """
        Parses the tuples of coordinates from input file and returns the dictionary, where:
        - Key -> the tuple of coordinates of active cell 
        - Value -> instance of the Cell class
    """

    # Look for tuples in input file and parse them
    coordinates_tuple_pattern = r'\([-]{0,1}\d+, [-]{0,1}\d+\)'
    coordinates_tuples_parsed = re.findall(coordinates_tuple_pattern, coordinates_list_string)

    active_cells_dict = {}
    # Iterate through every tuple and parse both X and Y coordinate from it
    for coordinates_tuple_parsed in coordinates_tuples_parsed:
        coordinate_single_pattern = r'[-]{0,1}\d+'
        coordinates_parsed = re.findall(coordinate_single_pattern, coordinates_tuple_parsed)

        try:
            # Create a tuple consists X and Y coordinates as an Integer
            coordinates_tuple = (int(coordinates_parsed[0]), int(coordinates_parsed[1]))
            active_cells_dict[coordinates_tuple] = Cell(coordinates_tuple[0], coordinates_tuple[1], True, 0)
        except Exception as e:
            print(f'Some error occured, skipping current cell coordinates. Error: {e}')

    # If the dict is empty, raise BadInitCoordinateError
    if not active_cells_dict:
        raise BadInitCoordinatesError() 

    return active_cells_dict

def print_cell(status):
    """Print GREEN 'O' for cells which are alive (status == 'active'), otherwise print RED '+'."""

    print('\033[92mO\033[00m', end='') if status == 'active' else print('\033[91m+\033[00m', end='')

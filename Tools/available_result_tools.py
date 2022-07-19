"""
This module contains functions used throughout the available results processing modules to parse user inputs
"""


def column_contents(column_start: int, column_end: int, block: list[str]):
    """
    Generates a list of items in a specific column of a block

    :param column_start: start index of the column
    :param column_end:   end index of the column
    :param block:        block of data for which the column data is requested

    :return:    list of items in the column excluding "****" (which indicates a warning)
    """
    contents = []
    exclude = ('****',)
    for line in block:
        column_contents = line[column_start:column_end].strip()
        if column_contents and not column_contents.startswith(exclude):
            contents.append(column_contents)

    return contents


def valid_names(names: list[str], user_selection: tuple[int, str], set_index: int):
    """
    Uses the user selection criteria to parse a list of all names and returns a list of names matching the user
    selection.
    :param names:           list of names
    :param user_selection:  user input selection from results selection window
    :param set_index:       index of the specific result set for which the information is requested

    :return:                list of names from 'names' which meet the user criteria
    """
    item_choice = user_selection[set_index][0]
    item_input = user_selection[set_index][1]
    valid_names = []
    if item_choice == 2:
        for name in names:
            if name.startswith(item_input):
                valid_names.append(name)
            else:
                pass
    elif item_choice == 3:
        for name in names:
            if name.endswith(item_input):
                valid_names.append(name)
            else:
                pass
    elif item_choice == 4:
        for name in names:
            if item_input in name:
                valid_names.append(name)
            else:
                pass
    elif item_choice == 5:
        beam_list = "".join(item_input.upper()).replace(" ", "").split(',')
        for item in beam_list:
            valid_names.append(item)
    else:
        valid_names = names

    return valid_names


def valid_loads(load_names: list[list[str]], user_selection: tuple[int, str], set_index: int):
    """
    Uses the user selection criteria to parse a list of all loads and returns a list of loads matching the user
    selection.
    :param load_names:      list of list of load_names
    :param user_selection:  user input selection from results selection window
    :param set_index:       index of the specific result set for which the information is requested

    :return:                list of list of load names from 'load_names' which meet the user criteria
    """
    load_choice = user_selection[set_index][0]
    load_input = user_selection[set_index][1]
    user_loads = []
    if load_choice == 2:
        for loads in load_names:
            matching_loads = [l for l in loads if l.startswith(load_input)]
            user_loads.append(matching_loads)
    elif load_choice == 3:
        for loads in load_names:
            matching_loads = [l for l in loads if l.endswith(load_input)]
            user_loads.append(matching_loads)
    elif load_choice == 4:
        for loads in load_names:
            matching_loads = [l for l in loads if load_input in l]
            user_loads.append(matching_loads)
    elif load_choice == 5:
        load_list = "".join(load_input.upper()).replace(" ", "").split(',')
        for loads in load_names:
            matching_loads = [l for l in load_list if l in loads]
            user_loads.append(matching_loads)
    else:
        user_loads = load_names

    return user_loads

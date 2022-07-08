import os.path
from tkinter import filedialog
from tkinter.ttk import *
import datetime
"""
This module generates an input file in the form of a .txt file that contains a detailed breakdown of the user
requested results parameters.

"""


def read_results_parameters(results_selection_window: Treeview, tab_name: str) -> dict:
    """
    reads results parameters frame from each tab and returns a dictionary of the tab and requested results values
    :param results_selection_window: results selection window on the tab on which the button was pressed
    :param tab_name: name of active tab
    :return: dictionary containing tab name and requested results values
    """
    print(results_selection_window.children)
    print(tab_name)
    return {results_selection_window: tab_name}


def generate_header(input_file_name) -> list[str]:
    """
    Generates header based on input file name
    :return: formatted header based on save date/time and tab name
    """
    line1 = f'Data Extraction Tool Input File'
    line2 = f'Input File {os.path.basename(input_file_name)} Generated at {datetime.date.today()}'
    line3 = f'*********************************'

    return [line1, line2, line3]


def get_input_file_name() -> str:
    """
    gets the file name of the user generated input file
    :return: returns the name of the saved input file
    """
    input_file_name = filedialog.asksaveasfilename(filetypes=[('*.txt - DET Input File', '*.txt')], defaultextension='txt')
    return input_file_name


def format_result_parameter(result: dict) -> list[list[str]]:
    """
    formats the results dictionary into a nested list of strings for printing
    :param result: dictionary containing the results from the results selection window
    :return: returns a nested list of formatted strings for printing in the input file
    """
    result_1 = ['some info', 'some more info']
    result_2 = ['additional info', 'some additional info']
    return [result_1, result_2]


def print_input_file(results_selection_window: Treeview, tab_name: str):
    """
    prints and saves an input file containing a formatted display of the results selection window
    :param results_selection_window:
    :param tab_name:
    :return: None
    """
    input_file_name = get_input_file_name()
    header = generate_header(input_file_name)
    results = read_results_parameters(results_selection_window, tab_name)
    formatted_input = format_result_parameter(results)
    final_output = header
    for result in formatted_input:
        for line in result:
            final_output.append(line)
    with open(input_file_name, 'w') as file:
        file.writelines('\n'.join(final_output))


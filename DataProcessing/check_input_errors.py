"""
This module checks the user inputs for any errors. If errors are found, returns a list of those errors to report to the
user
"""
from DataProcessing.parse_file_for_input_data import ParseFileForData
from DataProcessing import extract_code_check as ecc
from Tools import shared_stuff
from error_handling import ErrorHandling
from Tools.available_result_tools import column_contents, get_items_in_col
from Tools.utilities import UserSelectionOption, TabName


def is_user_criteria_valid(available_results: list, user_choice: int, user_criteria: str) -> bool:
    """
    Takes the user choice and available results list and returns a parsed list containing only the results that match
    the user choice criteria

    :param user_choice: int representing the user choice
    :param available_results: list of all available results
    :param user_criteria: str containing the user requested criteria

    :return: True if available results contains matching user criteria, else False
    """
    user_criteria_up = user_criteria.upper()
    if user_choice == UserSelectionOption.ALL.value:
        return True
    if user_choice == UserSelectionOption.STARTSWITH:
        return any(True for item in available_results if item.startswith(user_criteria_up))
    if user_choice == UserSelectionOption.ENDSWITH:
        return any(True for item in available_results if item.endswith(user_criteria_up))
    if user_choice == UserSelectionOption.CONTAINS:
        return any(True for item in available_results if user_criteria_up in item)
    if user_choice == UserSelectionOption.LIST:
        name_list = "".join(user_criteria_up).replace(" ", "").split(',')
        for item in name_list:
            if item not in available_results:
                return False
        return True


def get_invalid_results(available_results: list, user_choice: int, user_criteria: str) -> list:
    """
    returns a list of invalid user criteria

    :param user_choice: int representing the user choice
    :param available_results: list of all available results
    :param user_criteria: str containing the user requested criteria

    :return: list containing invalid user criteria
    """
    user_criteria_up = user_criteria.upper()
    if user_choice == UserSelectionOption.ALL:
        return []
    elif user_choice == UserSelectionOption.LIST:
        name_list = "".join(user_criteria_up).replace(" ", "").split(',')
        return [item for item in name_list if item not in available_results]
    else:
        return [user_criteria_up]


def input_text_error(valid_options: list, user_choice: int, user_spec: str):
    """

    :param valid_options: list of valid options in result set
    :param user_choice: int representing the results selection window user choice
    :param user_spec: str containing the user requested criteria

    :return: False if no errors were found, otherwise a list of errors
    """
    if is_user_criteria_valid(valid_options, user_choice, user_spec):
        return False
    else:
        input_error = get_invalid_results(valid_options, user_choice, user_spec)
        return input_error


def ir_errors(ir_list: list, ir_choice: int, ir_spec: tuple):
    """

    :param ir_list: list of valid IRs in result set
    :param ir_choice: int representing the results selection window choice
    :param ir_spec: tuple of the user IR selection values

    :return: str to display in error window if errors are found, otherwise returns False
    """
    upper_ir = ir_spec[1]
    lower_ir = ir_spec[0]
    try:
        [float(item) for item in ir_spec if not item == '']
    except ValueError:
        if not ir_choice == UserSelectionOption.ALL:
            return 'IR selection not valid'
    if ir_choice == UserSelectionOption.LESS_THAN:
        user_ir = [p for p in ir_list if float(p) < float(upper_ir)]
        if not user_ir:
            return f'< {upper_ir}'
    elif ir_choice == UserSelectionOption.GREATER_THAN:
        user_ir = [p for p in ir_list if float(p) > float(lower_ir)]
        if not user_ir:
            return f'> {lower_ir}'
    elif ir_choice == UserSelectionOption.BETWEEN:
        if float(lower_ir) > float(upper_ir) or (float(lower_ir) or float(upper_ir)) < 0:
            return 'Invalid IR range'
        else:
            user_ir = [p for p in ir_list if float(lower_ir) < float(p) < float(upper_ir)]
            if not user_ir:
                return f'between {lower_ir} and {upper_ir}'
    else:
        return False


class FindInputErrors:
    """
    Checks user inputs for errors (i.e. input values that have no corresponding valid results in the input file.

    :param tab_name     Name of active tab
    """

    def __init__(self, tab_name):
        self.tab_name = tab_name
        self.results = shared_stuff.data_store
        self.results.tab_name = tab_name
        self.name_id = self.results.name
        self.num_of_sets = len(self.results.set_index)
        self.error_dict = {}

    def is_input_error(self, initial_window):
        """
        Checks if an error exists in the user input
        :param initial_window: Tkinter instance of current active window
        :return: True if error exists, False if no error
        """
        for num in range(self.num_of_sets):
            self.find_error(num)
        sets_with_errors = [k for k, v in self.error_dict.items() if any(item for item in v)]
        if not sets_with_errors:
            return False
        if self.tab_name in [TabName.MEMBER_FORCE.value, TabName.JOINT_REACTION.value]:
            name_error = []
            load_error = []
            for set_num in sets_with_errors:
                name_error.append(self.error_dict[set_num][0])
                load_error.append(self.error_dict[set_num][1])
            ErrorHandling(initial_window).item_not_found(sets_with_errors, name_error, load_error, self.tab_name)
            return True
        elif self.tab_name == TabName.CODE_CHECK.value:
            name_error = []
            profile_error = []
            ir_error = []
            for set_num in sets_with_errors:
                name_error.append(self.error_dict[set_num][0])
                profile_error.append(self.error_dict[set_num][1])
                ir_error.append(self.error_dict[set_num][2])
            ErrorHandling(initial_window).item_not_found(sets_with_errors, name_error, profile_error, self.tab_name,
                                                         ir_errors=ir_error)
            return True

    def find_error(self, set_num):
        """
        Checks user member and joint reaction inputs for errors and stores the invalid input in error dictionary

        :param set_num: user result set number
        """
        extracted_result_list, _, _ = ParseFileForData(set_num, self.tab_name).get_result_list_info()
        if self.tab_name in [TabName.MEMBER_FORCE.value, TabName.JOINT_REACTION.value]:
            if self.tab_name == TabName.MEMBER_FORCE.value:
                load_col = 10, 19
            else:
                load_col = 19, 27
            names = column_contents(0, 9, extracted_result_list[1:-1])
            loads = list(set(column_contents(load_col[0], load_col[1], extracted_result_list[1:-1])))
            name_error = input_text_error(names, self.name_id[set_num][0], self.name_id[set_num][1])
            load_error = input_text_error(loads, self.results.load[set_num][0], self.results.load[set_num][1])
            self.error_dict[set_num + 1] = (name_error, load_error)
        else:
            code_check_list = ecc.GenerateOutputArray(self.tab_name, set_num, extracted_result_list).code_check_array()
            name_col = get_items_in_col(code_check_list, 0)
            profile_col = get_items_in_col(code_check_list, 11)
            ir_col = get_items_in_col(code_check_list, 5)
            name_error = input_text_error(name_col, self.name_id[set_num][0], self.name_id[set_num][1])
            profile_error = input_text_error(profile_col, self.results.profile[set_num][0],
                                             self.results.profile[set_num][1])
            ir_error = ir_errors(ir_col, self.results.ir_range[set_num][0], self.results.ir_range[set_num][1])
            self.error_dict[set_num + 1] = (name_error, profile_error, ir_error)

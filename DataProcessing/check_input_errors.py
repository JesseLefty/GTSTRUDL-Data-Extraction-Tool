"""
This module checks the user inputs for any errors. If errors are found, returns a list of those errors to report to the
user
"""
from DataProcessing.parse_file_for_input_data import ParseFileForData
from DataProcessing import extract_member_forces as emf
from DataProcessing import extract_joint_reactions as ejr
from DataProcessing import extract_code_check as ecc
from Tools import shared_stuff
from error_handling import ErrorHandling


def is_user_criteria_valid(user_choice: int, available_results: list, user_criteria: str) -> bool:
    """
    Takes the user choice and available results list and returns a parsed list containing only the results that match
    the user choice criteria

    :param user_choice: int representing the user choice
    :param available_results: list of all available results
    :param user_criteria: str containing the user requested criteria

    :return: True if available results contains matching user criteria, else False
    """
    user_criteria_up = user_criteria.upper()
    if user_choice == 1:
        return True
    elif user_choice == 2:
        return any(True for item in available_results if item.startswith(user_criteria_up))
    elif user_choice == 3:
        return any(True for item in available_results if item.endswith(user_criteria_up))
    elif user_choice == 4:
        return any(True for item in available_results if user_criteria_up in item)
    elif user_choice == 5:
        name_list = "".join(user_criteria_up).replace(" ", "").split(',')
        for item in name_list:
            if item not in available_results:
                return False
        return True


def get_invalid_results(user_choice: int, available_results: list, user_criteria: str) -> list:
    """
    returns a list of invalid user criteria

    :param user_choice: int representing the user choice
    :param available_results: list of all available results
    :param user_criteria: str containing the user requested criteria

    :return: list containing invalid user criteria
    """
    user_criteria_up = user_criteria.upper()
    if user_choice == 1:
        return []
    elif 1 < user_choice < 5:
        return [user_criteria_up]
    elif user_choice == 5:
        name_list = "".join(user_criteria_up).replace(" ", "").split(',')
        return [item for item in name_list if item not in available_results]


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
        if self.tab_name in ['Member Force', 'Joint Reaction']:
            for num in range(self.num_of_sets):
                self.find_error(num)
            if self.error_dict.keys():
                sets_with_errors = self.error_dict.keys()
                name_error = [item[0] for item in self.error_dict.values()]
                load_error = [item[1] for item in self.error_dict.values()]
                ErrorHandling(initial_window).item_not_found(sets_with_errors, name_error, load_error, self.tab_name)
                return True
            else:
                return False
        elif self.tab_name == 'Code Check':
            for num in range(self.num_of_sets):
                self.code_errors(num)
            if self.error_dict.keys():
                sets_with_errors = self.error_dict.keys()
                name_error = [item[0] for item in self.error_dict.values()]
                profile_error = [item[1] for item in self.error_dict.values()]
                ir_error = [item[2] for item in self.error_dict.values()]
                ErrorHandling(initial_window).item_not_found(sets_with_errors, name_error, profile_error, self.tab_name,
                                                             ir_errors=ir_error)
                return True
            else:
                return False

    def find_error(self, set_num):
        """
        Checks user member and joint reaction inputs for errors and stores the invalid input in error dictionary

        :param set_num: user result set number
        """
        names = None
        loads = None
        extracted_result_list, _, _ = ParseFileForData(set_num, self.tab_name).get_result_list_info()
        if self.tab_name == 'Member Force':
            _, names, loads = emf.GenerateOutputArray(self.tab_name, set_num, extracted_result_list).member_force_array()
        elif self.tab_name == 'Joint Reaction':
            _, names, loads = ejr.GenerateOutputArray(self.tab_name, set_num, extracted_result_list).joint_reaction_list()
        flat_names = [item for sub_list in names for item in sub_list]
        flat_loads = [item for sub_list in loads for item in sub_list]
        name_choice = self.name_id[set_num][0]
        name_spec = self.name_id[set_num][1]
        load_choice = self.results.load[set_num][0]
        load_spec = self.results.load[set_num][1]
        set_num_error = False
        if not is_user_criteria_valid(name_choice, flat_names, name_spec):
            name_error = get_invalid_results(name_choice, flat_names, name_spec)
            set_num_error = set_num + 1
        else:
            name_error = False
        if not is_user_criteria_valid(load_choice, flat_loads, load_spec):
            load_error = get_invalid_results(load_choice, flat_loads, load_spec)
            set_num_error = set_num + 1
        else:
            load_error = False
        if set_num_error:
            self.error_dict[set_num + 1] = (name_error, load_error)
        else:
            pass

    def code_errors(self, set_num):
        """
        Checks user code check inputs for errors and returns error dictionary of invalid items

        :param set_num:
        :return: user result set number
        """
        extracted_result_list, _, _ = ParseFileForData(set_num, self.tab_name).get_result_list_info()
        code_check_list = ecc.GenerateOutputArray(self.tab_name, set_num, extracted_result_list).code_check_array()
        name_col = []
        profile_col = []
        ir_col = []
        ir_error = []
        set_num_error = []
        for row in code_check_list:
            name_col.append(row[0])
            profile_col.append(row[11])
            ir_col.append(row[5])
        name_choice = self.name_id[set_num][0]
        name_spec = self.name_id[set_num][1]
        profile_choice = self.results.profile[set_num][0]
        profile_spec = self.results.profile[set_num][1]
        ir_choice = self.results.ir_range[set_num][0]
        ir_max = self.results.ir_range[set_num][1][1]
        ir_min = self.results.ir_range[set_num][1][0]

        if not is_user_criteria_valid(name_choice, name_col, name_spec):
            name_error = get_invalid_results(name_choice, name_col, name_spec)
            set_num_error = set_num + 1
        else:
            name_error = False

        if not is_user_criteria_valid(profile_choice, profile_col, profile_spec):
            profile_error = get_invalid_results(profile_choice, profile_col, profile_spec)
            set_num_error = set_num + 1
        else:
            profile_error = False

        try:
            [float(item) for item in self.results.ir_range[set_num][1] if not item == '']
            not_number = False
        except ValueError:
            not_number = True
        if not_number and not ir_choice == 1:
            ir_error = 'IR selection not valid'
            set_num_error = set_num + 1
        else:
            if ir_choice == 1:
                pass
            elif ir_choice == 2:
                ir_less_than = float(ir_max)
                user_ir = [p for p in ir_col if float(p) < ir_less_than]
                if not user_ir:
                    ir_error = f'< {ir_less_than}'
                    set_num_error = set_num + 1
            elif ir_choice == 3:
                ir_greater_than = float(ir_min)
                user_ir = [p for p in ir_col if float(p) > ir_greater_than]
                if not user_ir:
                    ir_error = f'> {ir_greater_than}'
                    set_num_error = set_num + 1
            elif ir_choice == 4:
                lower_ir = float(ir_min)
                upper_ir = float(ir_min)
                if lower_ir > upper_ir or (lower_ir or upper_ir) < 0:
                    ir_error = 'Invalid IR range'
                    set_num_error = set_num + 1
                else:
                    user_ir = [p for p in ir_col if lower_ir < float(p) < upper_ir]
                    if not user_ir:
                        ir_error = f'between {lower_ir} and {upper_ir}'
                        set_num_error = set_num + 1
        if set_num_error:
            self.error_dict[set_num + 1] = (name_error, profile_error, ir_error)
        else:
            pass

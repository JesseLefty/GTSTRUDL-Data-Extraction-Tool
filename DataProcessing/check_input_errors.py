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
        self.num_of_sets = self.results.set_index
        self.error_dict = {}

    def is_input_error(self, initial_window):
        """
        Checks if an error exists in the user input
        :param initial_window: Tkinter instance of current active window
        :return: True if error exists, False if no error
        """
        if self.tab_name in ['Member Force', 'Joint Reaction']:
            for num in range(len(self.num_of_sets)):
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
            for num in range(len(self.num_of_sets)):
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
        load_id = self.results.load
        extracted_result_list, _, _ = ParseFileForData(set_num, self.tab_name).get_result_list_info()
        if self.tab_name == 'Member Force':
            _, names, loads = emf.GenerateOutputArray(self.tab_name, set_num, extracted_result_list).member_force_array()
        elif self.tab_name == 'Joint Reaction':
            _, names, loads = ejr.GenerateOutputArray(self.tab_name, set_num, extracted_result_list).joint_reaction_list()
        flat_names = [item for sub_list in names for item in sub_list]
        flat_loads = [item for sub_list in loads for item in sub_list]
        name_choice = self.name_id[set_num][0]
        load_choice = load_id[set_num][0]
        name_error = []
        load_error = []
        set_num_error = []
        error = False
        if name_choice == 1:
            pass
        elif name_choice == 2:
            name_starts_with = self.name_id[set_num][1]
            if not any(item.startswith(name_starts_with) for item in flat_names):
                name_error = name_starts_with
                set_num_error = set_num + 1
            else:
                pass
        elif name_choice == 3:
            name_ends_with = self.name_id[set_num][1]
            if not any(item.endswith(name_ends_with) for item in flat_names):
                name_error = name_ends_with
                set_num_error = set_num + 1
            else:
                pass
        elif name_choice == 4:
            name_contains = self.name_id[set_num][1]
            if not any(name_contains in item for item in flat_names):
                name_error = name_contains
                set_num_error = set_num + 1
        elif name_choice == 5:
            name_text = self.name_id[set_num][1].upper()
            name_list = "".join(name_text).replace(" ", "").split(',')
            for item in name_list:
                if item not in flat_names:
                    name_error.append(item)
                    error = True
                else:
                    error = False
            if error:
                set_num_error = set_num + 1
        if load_choice == 1:
            pass
        elif load_choice == 2:
            load_starts_with = load_id[set_num][1]
            if not any(item.startswith(load_starts_with) for item in flat_loads):
                load_error = load_starts_with
                set_num_error = set_num + 1
            else:
                pass
        elif load_choice == 3:
            load_ends_with = load_id[set_num][1]
            if not any(item.endswith(load_ends_with) for item in flat_loads):
                load_error = load_ends_with
                set_num_error = set_num + 1
            else:
                pass
        elif load_choice == 4:
            load_contains = load_id[set_num][1]
            if not any(load_contains in item for item in flat_loads):
                load_error = load_contains
                set_num_error = set_num + 1
        elif load_choice == 5:
            load_text = load_id[set_num][1].upper()
            load_list = "".join(load_text).replace(" ", "").split(',')
            for item in load_list:
                if item not in flat_loads:
                    load_error.append(item)
                    error = True
                else:
                    error = False
                if error:
                    set_num_error = set_num + 1
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
        profile = self.results.profile
        ir_range = self.results.ir_range
        name_col = []
        profile_col = []
        ir_col = []
        name_error = []
        profile_error = []
        ir_error = []
        set_num_error = []
        error = False
        for row in code_check_list:
            name_col.append(row[0])
            profile_col.append(row[11])
            ir_col.append(row[5])
        name_choice = self.name_id[set_num][0]
        profile_choice = profile[set_num][0]
        ir_choice = ir_range[set_num][0]
        if name_choice == 1:
            pass
        elif name_choice == 2:
            name_starts_with = self.name_id[set_num][1]
            if not any(item.startswith(name_starts_with) for item in name_col):
                name_error = name_starts_with
                set_num_error = set_num + 1
            else:
                pass
        elif name_choice == 3:
            name_ends_with = self.name_id[set_num][1]
            if not any(item.startswith(name_ends_with) for item in name_col):
                name_error = name_ends_with
                set_num_error = set_num + 1
            else:
                pass
        elif name_choice == 4:
            name_contains = self.name_id[set_num][1]
            if not any(name_contains in item for item in name_col):
                name_error = name_contains
                set_num_error = set_num + 1
        elif name_choice == 5:
            name_text = self.name_id[set_num][1].upper()
            name_list = "".join(name_text).replace(" ", "").split(',')
            for item in name_list:
                if item not in name_col:
                    name_error.append(item)
                    error = True
                else:
                    error = False
            if error:
                set_num_error = set_num + 1
        if profile_choice == 1:
            pass
        elif profile_choice == 2:
            profile_starts_with = profile[set_num][1]
            if not any(item.startswith(profile_starts_with) for item in profile_col):
                profile_error = profile_starts_with
                set_num_error = set_num + 1
            else:
                pass
        elif profile_choice == 3:
            profile_ends_with = profile[set_num][1]
            if not any(item.startswith(profile_ends_with) for item in profile_col):
                profile_error = profile_ends_with
                set_num_error = set_num + 1
            else:
                pass
        elif profile_choice == 4:
            profile_contains = profile[set_num][1]
            if not any(profile_contains in item for item in profile_col):
                profile_error = profile_contains
                set_num_error = set_num + 1
        elif profile_choice == 5:
            profile_text = profile[set_num][1].upper()
            profile_list = "".join(profile_text).replace(" ", "").split(',')
            for item in profile_list:
                if item not in profile_col:
                    profile_error.append(item)
                    error = True
                else:
                    error = False
            if error:
                set_num_error = set_num + 1
        try:
            [float(item) for item in ir_range[set_num][1] if not item == '']
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
                ir_less_than = float(ir_range[set_num][1][1])
                user_ir = [p for p in ir_col if float(p) < ir_less_than]
                if not user_ir:
                    ir_error = f'< {ir_less_than}'
                    set_num_error = set_num + 1
            elif ir_choice == 3:
                ir_greater_than = float(ir_range[set_num][1][0])
                user_ir = [p for p in ir_col if float(p) > ir_greater_than]
                if not user_ir:
                    ir_error = f'> {ir_greater_than}'
                    set_num_error = set_num + 1
            elif ir_choice == 4:
                lower_ir = float(ir_range[set_num][1][0])
                upper_ir = float(ir_range[set_num][1][1])
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

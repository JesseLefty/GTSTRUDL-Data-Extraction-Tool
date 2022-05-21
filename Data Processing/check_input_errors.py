from parse_file_for_input_data import ParseFileForData
import extract_member_forces as emf
import extract_joint_reactions as ejr
import extract_code_check as ecc
import shared_stuff
from error_handling import ErrorHandling


class FindInputErrors:

    def __init__(self, tab_name):
        self.tab_name = tab_name
        self.results = shared_stuff.data_store
        self.results.tab_name = tab_name
        self.name_id = self.results.name
        self.num_of_sets = self.results.set_index
        self.error_dict = {}

    def consolidate_errors(self, initial_window):
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
                ErrorHandling(initial_window).item_not_found(sets_with_errors, name_error, profile_error, self.tab_name, ir_errors=ir_error)
                return True
            else:
                return False

    def find_error(self, items):
        names = None
        loads = None
        load_id = self.results.load
        extracted_result_list, _, _ = ParseFileForData(items, self.tab_name).get_result_list_info()
        if self.tab_name == 'Member Force':
            _, names, loads = emf.GenerateOutputArray(self.tab_name, items, extracted_result_list).member_force_array()
        elif self.tab_name == 'Joint Reaction':
            _, names, loads = ejr.GenerateOutputArray(self.tab_name, items, extracted_result_list).joint_reaction_list()
        flat_names = [item for sub_list in names for item in sub_list]
        flat_loads = [item for sub_list in loads for item in sub_list]
        print(f'flat loads = {flat_loads}')
        name_choice = self.name_id[items][0]
        load_choice = load_id[items][0]
        name_error = []
        load_error = []
        set_num_error = []
        error = False
        if name_choice == 1:
            pass
        elif name_choice == 2:
            name_starts_with = self.name_id[items][1]
            if not any(item.startswith(name_starts_with) for item in flat_names):
                name_error = name_starts_with
                set_num_error = items + 1
            else:
                pass
        elif name_choice == 3:
            name_ends_with = self.name_id[items][1]
            if not any(item.startswith(name_ends_with) for item in flat_names):
                name_error = name_ends_with
                set_num_error = items + 1
            else:
                pass
        elif name_choice == 4:
            name_contains = self.name_id[items][1]
            if not any(name_contains in item for item in flat_names):
                name_error = name_contains
                set_num_error = items + 1
        elif name_choice == 5:
            name_text = self.name_id[items][1].upper()
            name_list = "".join(name_text).replace(" ", "").split(',')
            for item in name_list:
                if item not in flat_names:
                    name_error.append(item)
                    error = True
                else:
                    error = False
            if error:
                set_num_error = items + 1
        if load_choice == 1:
            pass
        elif load_choice == 2:
            load_starts_with = load_id[items][1]
            if not any(item.startswith(load_starts_with) for item in flat_loads):
                load_error = load_starts_with
                set_num_error = items + 1
            else:
                pass
        elif load_choice == 3:
            load_ends_with = load_id[items][1]
            if not any(item.startswith(load_ends_with) for item in flat_loads):
                load_error = load_ends_with
                set_num_error = items + 1
            else:
                pass
        elif load_choice == 4:
            load_contains = load_id[items][1]
            if not any(load_contains in item for item in flat_loads):
                load_error = load_contains
                set_num_error = items + 1
        elif load_choice == 5:
            load_text = load_id[items][1].upper()
            load_list = "".join(load_text).replace(" ", "").split(',')
            for item in load_list:
                if item not in flat_loads:
                    load_error.append(item)
                    error = True
                else:
                    error = False
                if error:
                    set_num_error = items + 1
        if set_num_error:
            self.error_dict[items + 1] = (name_error, load_error)
        else:
            pass

    def code_errors(self, items):
        extracted_result_list, _, _ = ParseFileForData(items, self.tab_name).get_result_list_info()
        code_check_list = ecc.GenerateOutputArray(self.tab_name, items, extracted_result_list).code_check_array()
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
        for idx, row in enumerate(code_check_list):
            name_col.append(row[0])
            profile_col.append(row[11])
            ir_col.append(row[5])
        name_choice = self.name_id[items][0]
        profile_choice = profile[items][0]
        ir_choice = ir_range[items][0]
        if name_choice == 1:
            pass
        elif name_choice == 2:
            name_starts_with = self.name_id[items][1]
            if not any(item.startswith(name_starts_with) for item in name_col):
                name_error = name_starts_with
                set_num_error = items + 1
            else:
                pass
        elif name_choice == 3:
            name_ends_with = self.name_id[items][1]
            if not any(item.startswith(name_ends_with) for item in name_col):
                name_error = name_ends_with
                set_num_error = items + 1
            else:
                pass
        elif name_choice == 4:
            name_contains = self.name_id[items][1]
            if not any(name_contains in item for item in name_col):
                name_error = name_contains
                set_num_error = items + 1
        elif name_choice == 5:
            name_text = self.name_id[items][1].upper()
            name_list = "".join(name_text).replace(" ", "").split(',')
            for item in name_list:
                if item not in name_col:
                    name_error = item
                    error = True
                else:
                    error = False
            if error:
                set_num_error = items + 1
        if profile_choice == 1:
            pass
        elif profile_choice == 2:
            profile_starts_with = profile[items][1]
            if not any(item.startswith(profile_starts_with) for item in profile_col):
                profile_error = profile_starts_with
                set_num_error = items + 1
            else:
                pass
        elif profile_choice == 3:
            profile_ends_with = profile[items][1]
            if not any(item.startswith(profile_ends_with) for item in profile_col):
                profile_error = profile_ends_with
                set_num_error = items + 1
            else:
                pass
        elif profile_choice == 4:
            profile_contains = profile[items][1]
            if not any(profile_contains in item for item in profile_col):
                profile_error = profile_contains
                set_num_error = items + 1
        elif profile_choice == 5:
            profile_text = profile[items][1].upper()
            profile_list = "".join(profile_text).replace(" ", "").split(',')
            for item in profile_list:
                if item not in profile_col:
                    profile_error = item
                    error = True
                else:
                    error = False
            if error:
                set_num_error = items + 1
        try:
            [float(item) for item in ir_range[items][1]]
            not_number = False
        except ValueError:
            not_number = True
        if not_number:
            ir_error = 'IRs must be numbers'
            set_num_error = items + 1
        else:
            if ir_choice == 1:
                pass
            elif ir_choice == 2:
                ir_less_than = float(ir_range[items][1][1])
                user_ir = [p for p in ir_col if float(p) < ir_less_than]
                if not user_ir:
                    ir_error = f'< {ir_less_than}'
                    set_num_error = items + 1
            elif ir_choice == 3:
                ir_greater_than = float(ir_range[items][1][0])
                user_ir = [p for p in ir_col if float(p) > ir_greater_than]
                if not user_ir:
                    ir_error = f'> {ir_greater_than}'
                    set_num_error = items + 1
            elif ir_choice == 4:
                lower_ir = float(ir_range[items][1][0])
                upper_ir = float(ir_range[items][1][1])
                if lower_ir > upper_ir or (lower_ir or upper_ir) < 0:
                    ir_error = 'Invalid IR range'
                    set_num_error = items + 1
                else:
                    user_ir = [p for p in ir_col if lower_ir < float(p) < upper_ir]
                    if not user_ir:
                        ir_error = f'between {lower_ir} and {upper_ir}'
                        set_num_error = items + 1
        if set_num_error:
            self.error_dict[items + 1] = (name_error, profile_error, ir_error)
            print(self.error_dict)
        else:
            pass

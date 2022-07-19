"""
This module provides tools for generating an 'input file' based on the what options the user has selected when
generating results
"""
from Tools import shared_stuff
from Tools.config import rb_options, sort_order_dict, sort_direction_dict


def convert_bool_to_yes_no(bool_val: bool) -> str:
    """
    converts a boolean to a yes or no string

    :param bool_val: True / False boolean value
    :return: 'YES' or 'NO' string
    """
    return 'Yes' if bool_val else 'No'


class ProcessResultsPrinting:

    def __init__(self, tab_name: str):
        self.results = shared_stuff.data_store
        self.results.tab_name = tab_name

    def get_name_spec(self, item: int):
        """
        gets name spec from list of stored results parameters
        """
        name_option = rb_options[self.results.name[item][0]]
        name_choices = self.results.name[item][1]
        return name_option, name_choices

    def get_load_spec(self, item: int):
        """
        gets load spec from list of stored results parameters
        """
        load_option = rb_options[self.results.load[item][0]]
        load_choices = self.results.load[item][1]
        return load_option, load_choices

    def get_joint_sepc(self, item: int):
        """
        gets joint spec from list of stored results parameters
        """
        return self.results.joint[item]

    def get_set_name(self, item: int):
        """
        gets set name from list of stored results parameters
        """
        return self.results.set_name[item]

    def get_profile_spec(self, item: int):
        """
        gets profile spec from list of stored results parameters
        """
        profile_option = rb_options[self.results.profile[item][0]]
        profile_choices = self.results.profile[item][1]
        return profile_option, profile_choices

    def get_ir_spec(self, item: int):
        """
        gets IR spec from list of stored results parameters and provides some string formatting based on
        selected user options
        """
        min_ir, max_ir = self.results.ir_range[item][1]
        if min_ir and max_ir:
            ir_val = f'{min_ir} < IR < {max_ir}'
        elif min_ir and not max_ir:
            ir_val = f'IR > {min_ir}'
        elif max_ir and not min_ir:
            ir_val = f'IR < {max_ir}'
        else:
            ir_val = 'All IRs'
        return ir_val

    def get_sort_criteria(self, item: int):
        """
        gets sort criteria list of from stored results parameters
        """
        if self.results.sort[item]:
            sort_selection = []
            rev_sort_order_dict = {v: k for k, v in sort_order_dict.items()}
            for t in self.results.sort_order[item]:
                sort_selection.append(rev_sort_order_dict[t[0]])
        else:
            sort_selection = ['N/A']
        return sort_selection

    def get_sort_direction(self, item: int):
        """
        gets ascending or descending sort direction from list of stored results parameters
        """
        if self.results.sort[item]:
            sort_direction = []
            for val in self.results.reverse[item]:
                sort_direction.append(sort_direction_dict[val])
        else:
            sort_direction = ['N/A']
        return sort_direction

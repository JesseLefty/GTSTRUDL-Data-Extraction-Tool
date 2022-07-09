"""
This module updates the selected results window Treeview after the user makes changes to the results selection
"""
from Tools import shared_stuff
from Tools.result_printing_tools import ProcessResultsPrinting, convert_bool_to_yes_no


class UpdateResultTree:
    """
    Updates the results selection window display after the user makes any changes to the selected results or imports
    new results

    :param tab_name active tab name
    :param selected_results_tree - Tkinter Treeview object
    """

    def __init__(self, tab_name, selected_results_tree):
        self.tab_name = tab_name
        self.selected_results_tree = selected_results_tree
        self.results = shared_stuff.data_store
        self.results.tab_name = self.tab_name
        print(f'update results value = {self.results.results_parameters}')
        self.set_name = self.results.set_name

    def update_result_tree(self):
        """
        Updates the results selection window based on user requested results
        """
        parent = ''
        index = 'end'
        print_data = ProcessResultsPrinting(self.tab_name)
        for item in self.selected_results_tree.get_children():
            self.selected_results_tree.delete(item)

        for idx in range(len(self.results.set_name)):
            idd = idx + 1
            text = print_data.get_set_name(idx)
            name_option, name_choices = print_data.get_name_spec(idx)

            if self.tab_name == 'Member Force':
                load_option, load_choices = print_data.get_load_spec(idx)
                joint_option = print_data.get_joint_sepc(idx)
                values = (idd,
                          text,
                          joint_option,
                          f'{name_option} {name_choices}',
                          f'{load_option} {load_choices}')

            elif self.tab_name == 'Joint Reaction':
                load_option, load_choices = print_data.get_load_spec(idx)
                values = (idd,
                          text,
                          f'{name_option} {name_choices}',
                          f'{load_option} {load_choices}')

            else:
                profile_option, profile_choices = print_data.get_profile_spec(idx)
                ir_val = print_data.get_ir_spec(idx)
                sort_select = convert_bool_to_yes_no(self.results.sort[idx])
                values = (idd,
                          text,
                          f'{name_option} {name_choices}',
                          f'{profile_option} {profile_choices}',
                          f'{ir_val}',
                          f'{sort_select}'
                          )
            self.selected_results_tree.insert(parent=parent, index=index, iid=idd, text=text, values=values)

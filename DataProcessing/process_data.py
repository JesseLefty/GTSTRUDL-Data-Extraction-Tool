"""
Processes data from the results selection window as well as modifies, deletes, imports, or exports result information
based on user actions.
"""
import json
from tkinter import filedialog
import os
from DataProcessing import check_input_errors
import error_handling
from DataProcessing import save_output
from Tools.config import output_file_types, store_file_types
from GUI.update_results_tree import UpdateResultTree
from Tools import shared_stuff


class ProcessData:
    """

    :param tab_name: name of active tab
    :param selection_idd: index of result set to process
    :param modify: True/False if modify button was pressed
    :param selected_results_tree: Tkinter selected results Treeview object
    :param initial_window: Tkinter active window
    """

    def __init__(self, tab_name, selection_idd=0, modify=False, selected_results_tree=None,
                 initial_window=None):
        self.tab_name = tab_name
        self.results = shared_stuff.data_store
        self.results.tab_name = self.tab_name
        self.modify = modify
        self.selection_idd = selection_idd
        self.directory = self.results.directory
        self.selected_results_tree = selected_results_tree
        self.initial_window = initial_window

    def results_parameters(self):
        return self.results

    def store_results(self, first_text, second_text, joint_rb=None, selected_result=None, ir_range=None,
                      sort=None, fail=None, sort_order=None, reverse=None):
        """
        Runs data storage functions based on the active tab name when 'store' button is pressed in Results Selection
        Window

        :param first_text: text in the first text box
        :param second_text: text in the second text box
        :param joint_rb: value of the joint radio button
        :param selected_result: index of the selected result
        :param ir_range: user input IR range criteria
        :param sort: True/False if sort radio button is checked
        :param fail: True/False if fail radio button is checked
        :param sort_order: or in which to sort the code check results
        :param reverse: True/False for ascending or descending sort order
        """

        if self.tab_name == 'Member Force':
            self.store_mem_force(first_text, second_text, joint_rb)
        elif self.tab_name == 'Joint Reaction':
            self.store_joint_reaction(first_text, second_text)
        else:
            self.store_code_check(first_text, second_text, ir_range, sort, fail, sort_order, reverse)
        self.store_name_index(selected_result)
        UpdateResultTree(self.tab_name, self.selected_results_tree).update_result_tree()

    def store_mem_force(self, first_text, second_text, joint_rb):
        """
        stores parameters related to member force output

        :param first_text: text in the first text box
        :param second_text: text in the second text box
        :param joint_rb: value of the joint radio button

        """
        if self.modify:
            self.results.joint[self.selection_idd] = joint_rb
            self.results.name[self.selection_idd] = first_text
            self.results.load[self.selection_idd] = second_text
        else:
            self.results.joint.append(joint_rb)
            self.results.name.append(first_text)
            self.results.load.append(second_text)

    def store_joint_reaction(self, first_text, second_text):
        """
        stores parameters related to joint reaction output

        :param first_text: text in the first text box
        :param second_text: text in the second text box
        """
        if self.modify:
            self.results.name[self.selection_idd] = first_text
            self.results.load[self.selection_idd] = second_text
        else:
            self.results.name.append(first_text)
            self.results.load.append(second_text)

    def store_code_check(self, first_text, second_text, ir_range, sort, fail, sort_order, reverse):
        """
        stores results related to code check output

        :param first_text: text in the first text box
        :param second_text: text in the second text box
        :param ir_range: user input IR range criteria
        :param sort: True/False if sort radio button is checked
        :param fail: True/False if fail radio button is checked
        :param sort_order: or in which to sort the code check results
        :param reverse: True/False for ascending or descending sort order
        """

        if self.modify:
            self.results.name[self.selection_idd] = first_text
            self.results.profile[self.selection_idd] = second_text
            self.results.ir_range[self.selection_idd] = ir_range
            self.results.sort[self.selection_idd] = sort
            self.results.fail[self.selection_idd] = fail
            self.results.sort_order[self.selection_idd] = sort_order
            self.results.reverse[self.selection_idd] = reverse
        else:
            self.results.name.append(first_text)
            self.results.profile.append(second_text)
            self.results.ir_range.append(ir_range)
            self.results.sort.append(sort)
            self.results.fail.append(fail)
            self.results.sort_order.append(sort_order)
            self.results.reverse.append(reverse)

    def store_name_index(self, selected_result):
        """
        stores the set name and set number of the selected result

        :param selected_result: tuple of the set name and set number for which results are requested
        """
        set_num_selected = selected_result[0]
        set_name_selected = selected_result[1]
        if self.modify:
            pass
        else:
            self.results.set_name.append(set_name_selected)
            self.results.set_index.append(set_num_selected)

    def delete_result(self):
        """
        deletes results from ResultsParameters if user clicks 'delete' button
        """
        if self.tab_name == 'Member Force':
            del self.results.joint[self.selection_idd]
            del self.results.load[self.selection_idd]
        elif self.tab_name == 'Joint Reaction':
            del self.results.load[self.selection_idd]
        else:
            del self.results.profile[self.selection_idd]
            del self.results.ir_range[self.selection_idd]
            del self.results.sort[self.selection_idd]
            del self.results.fail[self.selection_idd]
            del self.results.sort_order[self.selection_idd]
            del self.results.reverse[self.selection_idd]

        del self.results.set_name[self.selection_idd]
        del self.results.set_index[self.selection_idd]
        del self.results.name[self.selection_idd]
        UpdateResultTree(self.tab_name, self.selected_results_tree).update_result_tree()
        if self.selected_results_tree.get_children():
            child_id = self.selected_results_tree.get_children()[0]
            self.selected_results_tree.selection_set(child_id)
        else:
            pass

    def store_inputs(self):
        """
        generates a .prop file of current contents in the ResultsParameters object. This file can be imported into
        the program at any time
        """
        if not self.selected_results_tree.get_children():
            print('no stored results')
        else:
            prop_file_name = filedialog.asksaveasfilename(filetypes=store_file_types, defaultextension='*.prop')
            stored_results = {self.tab_name: self.results.results_parameters}
            try:
                with open(prop_file_name, 'w') as f:
                    json.dump(stored_results, f, indent=4)
            except FileNotFoundError as e:
                print(e)

    def load_existing_result_set(self):
        """
        loads existing .prop file into the ResultsParameters object
        """
        load_existing_file_path = filedialog.askopenfilename(initialdir=self.directory, title="select file",
                                                             filetypes=store_file_types)
        try:
            with open(load_existing_file_path) as json_file:
                data = json.load(json_file)
            if self.tab_name in data.keys():
                loaded_results = data[self.tab_name]
                self.results.name = loaded_results['Name']
                self.results.set_name = loaded_results['Set Name']
                self.results.set_index = loaded_results['Set Index']
                if self.tab_name == 'Member Force':
                    self.results.joint = loaded_results['Joint']
                    self.results.load = loaded_results['Load']
                elif self.tab_name == 'Joint Reaction':
                    self.results.load = loaded_results['Load']
                else:
                    self.results.profile = loaded_results['Profile']
                    self.results.ir_range = loaded_results['IR Range']
                    self.results.sort = loaded_results['Sort']
                    self.results.fail = loaded_results['Fail']
                    self.results.sort_order = loaded_results['Sort Order']
                    self.results.reverse = loaded_results['Reverse']
                UpdateResultTree(self.tab_name, self.selected_results_tree).update_result_tree()

            else:
                error_handling.ErrorHandling(self.initial_window).wrong_properties_file(self.tab_name)

        except FileNotFoundError as e:
            print('file not found')
            print(e)
        except UnboundLocalError as e:
            print(e)

    def generate_results(self):
        """
        checks for errors in the user input and if no errors are found prompts the user to select output file type and
        generates the results output file.
        """
        errors = check_input_errors.FindInputErrors(self.tab_name).is_input_error(self.initial_window)
        if not self.results.set_index:
            error_handling.ErrorHandling(self.initial_window).no_result_set()
        elif not errors:
            output_file_path = filedialog.asksaveasfilename(filetypes=output_file_types, defaultextension='xlsx')
            out_format = os.path.splitext(output_file_path)[1]
            try:
                save_output.RunProgram(self.tab_name, out_format, output_file_path, self.results.set_index,
                                       self.initial_window)

            except FileNotFoundError as e:
                print(e)
                print('no file selected / action canceled')

import json
from tkinter import filedialog
from config import file_types
from update_results_tree import UpdateResultTree
import shared_stuff


class ProcessData:

    def __init__(self, tab_name, selection_idd=0, modify=False, directory=None, selected_results_tree=None):
        self.tab_name = tab_name
        self.results = shared_stuff.data_store
        self.results.tab_name = self.tab_name
        self.modify = modify
        self.selection_idd = selection_idd
        self.directory = directory
        self.selected_results_tree = selected_results_tree

    def results_parameters(self):
        return self.results

    def store_results(self, first_text, second_text, joint_rb=None, selected_result=None, ir_range=None,
                      sort=None, fail=None, sort_order=None, reverse=None):

        if self.tab_name == 'Member Force':
            self.store_mem_force(first_text, second_text, joint_rb)
        elif self.tab_name == 'Joint Reaction':
            self.store_joint_reaction(first_text, second_text)
        else:
            self.store_code_check(first_text, second_text, ir_range, sort, fail, sort_order, reverse)
        self.store_name_index(selected_result)
        UpdateResultTree(self.tab_name, self.selected_results_tree).update_result_tree()

    def store_mem_force(self, first_text, second_text, joint_rb):
        if self.modify or self.selection_idd == 0:
            self.results.joint[self.selection_idd] = joint_rb
            self.results.name[self.selection_idd] = first_text
            self.results.load[self.selection_idd] = second_text
        else:
            self.results.joint.append(joint_rb)
            self.results.name.append(first_text)
            self.results.load.append(second_text)

    def store_joint_reaction(self, first_text, second_text):
        if self.modify or self.selection_idd == 0:
            self.results.name[self.selection_idd] = first_text
            self.results.load[self.selection_idd] = second_text
        else:
            self.results.name.append(first_text)
            self.results.load.append(second_text)

    def store_code_check(self, first_text, second_text, ir_range, sort, fail, sort_order, reverse):

        if self.modify or self.selection_idd == 0:
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
        set_num_selected = selected_result[0]
        set_name_selected = selected_result[1]
        if self.selection_idd == 0 and not self.modify:
            self.results.set_name[self.selection_idd] = set_name_selected
            self.results.set_index[self.selection_idd] = set_num_selected
        elif self.modify:
            pass
        else:
            self.results.set_name.append(set_name_selected)
            self.results.set_index.append(set_num_selected)

    def delete_result(self):
        print('delete results')

    def store_inputs(self):
        prop_file_name = filedialog.asksaveasfilename(filetypes=file_types, defaultextension='*.prop')
        # TODO: grey out store input button if there are no results sets or raise error
        stored_results = {self.tab_name: self.results.results_parameters}
        try:
            with open(prop_file_name, 'w') as f:
                json.dump(stored_results, f, indent=4)
        except FileNotFoundError:
            pass

    def load_existing_result_set(self):
        # todo: perhaps provide a warning that loading a results file will overwrite all other results
        load_existing_file_path = filedialog.askopenfilename(initialdir=self.directory, title="select file",
                                                             filetypes=file_types)
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
                UpdateResultTree(self.tab_name, self.selected_results_tree).update_result_tree()
            else:
                print('wrong file')

        except FileNotFoundError:
            print('file not found')
            pass
        except UnboundLocalError:
            pass

    def generate_results(self):
        print('generate results')

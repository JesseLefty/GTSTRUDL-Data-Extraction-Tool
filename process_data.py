from data_storage import ResultsParameters
import json
from tkinter import filedialog
from config import file_types
from update_results_tree import UpdateResultTree


class ProcessData:

    def __init__(self, tab_name, selection_idd=0, modify=False, directory=None, selected_results_tree=None):
        self.tab_name = tab_name
        self.results = ResultsParameters(self.tab_name)
        self.modify = modify
        self.selection_idd = selection_idd
        self.directory = directory
        self.selected_results_tree = selected_results_tree
        self.set_num = self.results.results_parameters['Set Index']
        self.set_name = self.results.results_parameters['Set Name']
        self.name = self.results.results_parameters['Name']
        if self.tab_name == 'Member Force':
            self.joint = self.results.results_parameters['Joint']
            self.load = self.results.results_parameters['Load']
        elif self.tab_name == 'Joint Reaction':
            self.load = self.results.results_parameters['Load']
        else:
            self.profile = self.results.results_parameters['Profile']
            self.ir_range = self.results.results_parameters['IR Range']
            self.sort = self.results.results_parameters['Sort']
            self.fail = self.results.results_parameters['Fail']
            self.sort_order = self.results.results_parameters['Sort Order']
            self.reverse = self.results.results_parameters['Reverse']

        print(f'init results = {self.results.results_parameters}')

    def store_results(self, first_text, second_text, joint_rb=None, selected_result=None, ir_range=None,
                      sort=None, fail=None, sort_order=None, reverse=None):

        if self.tab_name == 'Member Force':
            self.store_mem_force(first_text, second_text, joint_rb)
        elif self.tab_name == 'Joint Reaction':
            self.store_joint_reaction(first_text, second_text)
        else:
            self.store_code_check(first_text, second_text, ir_range, sort, fail, sort_order, reverse)
        self.store_name_index(selected_result)

    def store_mem_force(self, first_text, second_text, joint_rb):
        if self.modify or self.selection_idd == 0:
            self.joint[self.selection_idd] = joint_rb
            self.name[self.selection_idd] = first_text
            self.load[self.selection_idd] = second_text
        else:
            self.joint.append(joint_rb)
            self.name.append(first_text)
            self.load.append(second_text)

        self.results.joint = self.joint
        self.results.mem_name = self.name
        self.results.mem_load = self.load

    def store_joint_reaction(self, first_text, second_text):
        if self.modify or self.selection_idd == 0:
            self.name[self.selection_idd] = first_text
            self.load[self.selection_idd] = second_text
        else:
            self.name.append(first_text)
            self.load.append(second_text)

        self.results.joint_name = self.name
        self.results.joint_load = self.load

    def store_code_check(self, first_text, second_text, ir_range, sort, fail, sort_order, reverse):

        if self.modify or self.selection_idd == 0:
            self.name[self.selection_idd] = first_text
            self.profile[self.selection_idd] = second_text
            self.ir_range[self.selection_idd] = ir_range
            self.sort[self.selection_idd] = sort
            self.fail[self.selection_idd] = fail
            self.sort_order[self.selection_idd] = sort_order
            self.reverse[self.selection_idd] = reverse
        else:
            self.name.append(first_text)
            self.profile.append(second_text)
            self.ir_range.append(ir_range)
            self.sort.append(sort)
            self.fail.append(fail)
            self.sort_order.append(sort_order)
            self.reverse.append(reverse)

        self.results.code_name = self.name
        self.results.profile = self.profile
        self.results.ir_range = self.ir_range
        self.results.sort = self.sort
        self.results.fail = self.fail
        self.results.sort_order = self.sort_order
        self.results.reverse = self.reverse

    def store_name_index(self, selected_result):
        set_num_selected = selected_result[0]
        set_name_selected = selected_result[1]
        if self.selection_idd == 0 and not self.modify:
            self.set_name[self.selection_idd] = set_name_selected
            self.set_num[self.selection_idd] = set_num_selected
        elif self.modify:
            pass
        else:
            self.set_name.append(set_name_selected)
            self.set_num.append(set_num_selected)

        if self.tab_name == 'Member Force':
            self.results.mem_set_name = self.set_name
            self.results.mem_set_index = self.set_num
        elif self.tab_name == 'Joint Reaction':
            self.results.joint_set_name = self.set_name
            self.results.joint_set_index = self.set_num
        else:
            self.results.code_set_name = self.set_name
            self.results.code_set_index = self.set_num

    def print_results(self):
        print(f'final results dict = {self.results.results_parameters}')

    def delete_result(self):

        # del self.joint[self.selection_idd]
        # self.results.joint = self.joint
        # print(f'results = {self.results}')
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
                print(self.results.results_parameters)
                loaded_results = data[self.tab_name]
                self.name = loaded_results['Name']
                self.set_name = loaded_results['Set Name']
                self.set_num = loaded_results['Set Index']
                if self.tab_name == 'Member Force':
                    self.joint = loaded_results['Joint']
                    self.load = loaded_results['Load']

                    self.results.joint = self.joint
                    self.results.mem_name = self.name
                    self.results.mem_load = self.load
                    self.results.mem_set_name = self.set_name
                    self.results.mem_set_index = self.set_num

                elif self.tab_name == 'Joint Reaction':
                    self.results.joint_set_name = self.set_name
                    self.results.joint_set_index = self.set_num
                else:
                    self.results.code_set_name = self.set_name
                    self.results.code_set_index = self.set_num
                self.results.results_parameters = loaded_results
                print(self.results.results_parameters)
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

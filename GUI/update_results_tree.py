from config import rb_options
import shared_stuff


class UpdateResultTree:

    def __init__(self, tab_name, selected_results_tree):
        self.tab_name = tab_name
        self.selected_results_tree = selected_results_tree
        self.results = shared_stuff.data_store
        self.results.tab_name = self.tab_name
        print(f'update results value = {self.results.results_parameters}')
        self.set_name = self.results.set_name
    rb_config = rb_options

    def update_result_tree(self):
        parent = ''
        index = 'end'
        for item in self.selected_results_tree.get_children():
            self.selected_results_tree.delete(item)
        for idx, set_name in enumerate(self.results.set_name):
            idd = idx + 1
            text = self.set_name[idx]
            if self.tab_name == 'Member Force':
                values = (idd,
                          text,
                          self.results.joint[idx],
                          f'{self.rb_config[self.results.name[idx][0]]} {self.results.name[idx][1]}',
                          f'{self.rb_config[self.results.load[idx][0]]} {self.results.load[idx][1]}'
                          )
            elif self.tab_name == 'Joint Reaction':
                values = (idd,
                          text,
                          f'{self.rb_config[self.results.name[idx][0]]} {self.results.name[idx][1]}',
                          f'{self.rb_config[self.results.load[idx][0]]} {self.results.load[idx][1]}'
                          )
            else:
                values = (idd,
                          text,
                          f'{self.rb_config[self.results.name[idx][0]]} {self.results.name[idx][1]}',
                          f'{self.rb_config[self.results.profile[idx][0]]} {self.results.profile[idx][1]}',
                          f'{self.results.ir_range[idx][1][0]}, {self.results.ir_range[idx][1][1]}',
                          f'{self.results.sort[idx]}'
                          )
            self.selected_results_tree.insert(parent=parent, index=index, iid=idd, text=text, values=values)

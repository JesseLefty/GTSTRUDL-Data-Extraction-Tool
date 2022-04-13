from data_storage import ResultsParameters
from config import rb_options


class UpdateResultTree:

    def __init__(self, tab_name, selected_results_tree):
        self.tab_name = tab_name
        self.selected_results_tree = selected_results_tree
        print('about to call RESULTS PARAMETERS')
        self.results = ResultsParameters(self.tab_name).results_parameters
        print('just called RESULTS PARAMETERS')
        self.set_name = self.results['Set Name']

        print('update tree')
        print(self.results)
    rb_config = rb_options

    def update_result_tree(self):
        parent = ''
        index = 'end'
        for item in self.selected_results_tree.get_children():
            self.selected_results_tree.delete(item)
        for idx, set_name in enumerate(self.results['Set Name']):
            idd = idx + 1
            text = self.set_name[idx]
            if self.tab_name == 'Member Force':
                values = (idd,
                          text,
                          self.results['Joint'][idx],
                          f'{self.rb_config[self.results["Name"][idx][0]]} {self.results["Name"][idx][1]}',
                          f'{self.rb_config[self.results["Load"][idx][0]]} {self.results["Load"][idx][1]}'
                          )
            elif self.tab_name == 'Joint Reaction':
                values = (idd,
                          text,
                          f'{self.rb_config[self.results["Name"][idx][0]]} {self.results["Name"][idx][1]}',
                          f'{self.rb_config[self.results["Load"][idx][0]]} {self.results["Load"][idx][1]}'
                          )
            else:
                values = (idd,
                          text,
                          f'{self.rb_config[self.results["Name"][idx][0]]} {self.results["Name"][idx][1]}',
                          f'{self.rb_config[self.results["Profile"][idx][0]]} {self.results["Profile"][idx][1]}',
                          f'{self.results["IR Range"][idx][1][0]} - {self.results["IR Range"][idx][1][1]}',
                          f'{self.results["Sort"][idx]}'
                          )
            self.selected_results_tree.insert(parent=parent, index=index, iid=idd, text=text, values=values)

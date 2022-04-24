class ResultsParameters:

    def __init__(self, result_type=None):
        """
        Sets default result parameter values
        :param result_type: the major result type being requested (will correspond to the active tab name)
        """
        self._tab_name = result_type
        self._input_file = None
        self._results_parameters = {
            'Member Force': {
                'Joint': ['ALL'],
                'Name': [(1, 'ALL')],
                'Load': [(1, 'ALL')],
                'Set Index': [None],
                'Set Name': ["Default"]
            },
            'Joint Reaction': {
                'Name': [(1, 'ALL')],
                'Load': [(1, 'ALL')],
                'Set Index': [None],
                'Set Name': ["Default"]
            },
            'Code Check': {
                'Name': [(1, 'ALL')],
                'Profile': [(1, 'ALL')],
                'IR Range': [(1, ('MIN', 'MAX'))],
                'Sort': [False],
                'Fail': [False],
                'Sort Order': [[(0, False), (5, False), (8, False)]],
                'Reverse': [[False, False, False]],
                'Set Index': [None],
                'Set Name': ["Default"]
            }
        }

    @property
    def tab_name(self):
        return self._tab_name

    @property
    def results_parameters(self):
        return self._results_parameters[self._tab_name]

    @property
    def joint(self):
        return self._results_parameters[self._tab_name]['Joint']

    @property
    def name(self):
        return self._results_parameters[self._tab_name]['Name']

    @property
    def load(self):
        return self._results_parameters[self._tab_name]['Load']

    @property
    def profile(self):
        return self._results_parameters[self._tab_name]['Profile']

    @property
    def ir_range(self):
        return self._results_parameters[self._tab_name]['IR Range']

    @property
    def sort(self):
        return self._results_parameters[self._tab_name]['Sort']

    @property
    def fail(self):
        return self._results_parameters[self._tab_name]['Fail']

    @property
    def sort_order(self):
        return self._results_parameters[self._tab_name]['Sort Order']

    @property
    def reverse(self):
        return self._results_parameters[self._tab_name]['Reverse']

    @property
    def set_index(self):
        return self._results_parameters[self._tab_name]['Set Index']

    @property
    def set_name(self):
        return self._results_parameters[self._tab_name]['Set Name']

    @property
    def input_file(self):
        return self._input_file

    @tab_name.setter
    def tab_name(self, value):
        self._tab_name = value

    @joint.setter
    def joint(self, value):
        self._results_parameters[self._tab_name]['Joint'] = value

    @name.setter
    def name(self, value):
        self._results_parameters[self._tab_name]['Name'] = value

    @load.setter
    def load(self, value):
        self._results_parameters[self._tab_name]['Load'] = value

    @profile.setter
    def profile(self, value):
        self._results_parameters[self._tab_name]['Profile'] = value

    @ir_range.setter
    def ir_range(self, value):
        self._results_parameters[self._tab_name]['IR Range'] = value

    @sort.setter
    def sort(self, value):
        self._results_parameters[self._tab_name]['Sort'] = value

    @fail.setter
    def fail(self, value):
        self._results_parameters[self._tab_name]['Fail'] = value

    @sort_order.setter
    def sort_order(self, value):
        self._results_parameters[self._tab_name]['Sort Order'] = value

    @reverse.setter
    def reverse(self, value):
        self._results_parameters[self._tab_name]['Reverse'] = value

    @set_name.setter
    def set_name(self, value):
        self._results_parameters[self._tab_name]['Set Name'] = value

    @set_index.setter
    def set_index(self, value):
        self._results_parameters[self._tab_name]['Set Index'] = value

    @input_file.setter
    def input_file(self, value):
        self._input_file = value

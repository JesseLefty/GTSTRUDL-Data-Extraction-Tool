"""
Class which holds data used throughout other modules of the program.
"""


class ResultsParameters:
    """
    Sets default result parameter values
    """
    def __init__(self):
        self._tab_name = None
        self._input_file = None
        self._directory = None
        self._results_parameters = {}
        self.reset()

    def reset(self):
        """
        Resets the stored data to default values
        """
        self._tab_name = None
        self._input_file = None
        self._directory = None
        self._results_parameters = {
            'Member Force': {
                'Joint': [],
                'Name': [],
                'Load': [],
                'Set Index': [],
                'Set Name': []
            },
            'Joint Reaction': {
                'Name': [],
                'Load': [],
                'Set Index': [],
                'Set Name': []
            },
            'Code Check': {
                'Name': [],
                'Profile': [],
                'IR Range': [],
                'Sort': [],
                'Fail': [],
                'Sort Order': [],
                'Reverse': [],
                'Set Index': [],
                'Set Name': []
            }
        }

    @property
    def tab_name(self):
        """
        Active tab name
        :return: str: name of active tab
        """
        return self._tab_name

    @property
    def results_parameters(self):
        """
        Dictionary of all results parameters
        :return: dictionary of results parameters applicable to the active tab
        """
        return self._results_parameters[self._tab_name]

    @property
    def joint(self):
        """
        Joint parameter selection
        :return: tuple: value of joint selection for active tab
        """
        return self._results_parameters[self._tab_name]['Joint']

    @property
    def name(self):
        """
        Element name selection (joint, member, beam)
        :return: tuple: value of name selection for active tab
        """
        return self._results_parameters[self._tab_name]['Name']

    @property
    def load(self):
        """
        Load case parameter selection
        :return: tuple: value of load selection for active tab
        """
        return self._results_parameters[self._tab_name]['Load']

    @property
    def profile(self):
        """
        Profile parameter selection (ex. W10x49)
        :return: tuple: value of profile selection for active tab
        """
        return self._results_parameters[self._tab_name]['Profile']

    @property
    def ir_range(self):
        """
        IR range parameter selection
        :return: tuple: value of IR range selection for active tab
        """
        return self._results_parameters[self._tab_name]['IR Range']

    @property
    def sort(self):
        """
        Sort parameter selection
        :return: True if sort option is selected, None if not selected corresponding to active tab
        """
        return self._results_parameters[self._tab_name]['Sort']

    @property
    def fail(self):
        """
        Code check Fail parameter selection
        :return: True if fail option is selected, None if not selected corresponding to active tab
        """
        return self._results_parameters[self._tab_name]['Fail']

    @property
    def sort_order(self):
        """
        Sort order parameter selection
        :return: list: order in which to sort code check results corresponding to active tab
        """
        return self._results_parameters[self._tab_name]['Sort Order']

    @property
    def reverse(self):
        """
        Sort type, ascending or descending parameter selection
        :return: list: True of ascending, False for descending corresponding to active tab
        """
        return self._results_parameters[self._tab_name]['Reverse']

    @property
    def set_index(self):
        """
        Index of input file result set parameter
        :return: list: index number of selected available result corresponding to active tab
        """
        return self._results_parameters[self._tab_name]['Set Index']

    @property
    def set_name(self):
        """
        Name of selected available result set
        :return: list: name of selected available result set corresponding to active tab
        """
        return self._results_parameters[self._tab_name]['Set Name']

    @property
    def input_file(self):
        """
        Input file selected to parse
        :return: str: input file selected to parse
        """
        return self._input_file

    @property
    def directory(self):
        """
        Working directory selected by user
        :return: str: input file selected to parse
        """
        return self._directory

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

    @directory.setter
    def directory(self, value):
        self._directory = value

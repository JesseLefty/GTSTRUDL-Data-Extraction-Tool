class ResultsParameters:

    def __init__(self, result_type='default'):
        """
        Sets default result parameter values
        :param result_type: the major result type being requested (will correspond to the active tab name)
        """
        self.type = result_type

# todo: something is happening that I don't understand. values get set to default when I don't expect them to

    _joint = ['ALL']
    _mem_name = [(1, 'ALL')]
    _joint_name = [(1, 'ALL')]
    _code_name = [(1, 'ALL')]
    _mem_load = [(1, 'ALL')]
    _joint_load = [(1, 'ALL')]
    _profile = [(1, 'ALL')]
    _ir_range = [(1, ('MIN', 'MAX'))]
    _sort = [False]
    _fail = [False]
    _sort_order = [[(0, False), (5, False), (8, False)]]
    _reverse = [[False, False, False]]
    _mem_set_index = [None]
    _joint_set_index = [None]
    _code_set_index = [None]
    _mem_set_name = ["Default"]
    _joint_set_name = ["Default"]
    _code_set_name = ["Default"]

    # dictionary of major result type and corresponding stored value options - will expand to all values used
    # throughout program
    possible_result_types = {'Member Force': {'Joint': _joint,
                                              'Name': _mem_name,
                                              'Load': _mem_load,
                                              'Set Index': _mem_set_index,
                                              'Set Name': _mem_set_name},
                             'Joint Reaction': {'Name': _joint_name,
                                                'Load': _joint_load,
                                                'Set Index': _joint_set_index,
                                                'Set Name': _joint_set_name},
                             'Code Check': {'Name': _code_name,
                                            'Profile': _profile,
                                            'IR Range': _ir_range,
                                            'Sort': _sort,
                                            'Fail': _fail,
                                            'Sort Order': _sort_order,
                                            'Reverse': _reverse,
                                            'Set Index': _code_set_index,
                                            'Set Name': _code_set_name}
                             }
    print('init of data storage')
    _results_parameters = {}

    # dictionary to be used in generating final output
    @property
    def results_parameters(self):
        print(f'inside results parameter full results before set = {self._results_parameters}')
        print(f'set name inside results parameters = {self._mem_set_name}')
        self._results_parameters = {'Member Force': {'Joint': self._joint,
                                                     'Name': self._mem_name,
                                                     'Load': self._mem_load,
                                                     'Set Index': self._mem_set_index,
                                                     'Set Name': self._mem_set_name},
                                    'Joint Reaction': {'Name': self._joint_name,
                                                       'Load': self._joint_load,
                                                       'Set Index': self._joint_set_index,
                                                       'Set Name': self._joint_set_name},
                                    'Code Check': {'Name': self._code_name,
                                                   'Profile': self._profile,
                                                   'IR Range': self._ir_range,
                                                   'Sort': self._sort,
                                                   'Fail': self._fail,
                                                   'Sort Order': self._sort_order,
                                                   'Reverse': self._reverse,
                                                   'Set Index': self._code_set_index,
                                                   'Set Name': self._code_set_name}
                                    }
        print(f'inside results parameter full results after set = {self._results_parameters}')
        return self._results_parameters[self.type]

    @property
    def joint(self):
        return self._joint

    @property
    def mem_name(self):
        return self._mem_name

    @property
    def joint_name(self):
        return self._joint_name

    @property
    def code_name(self):
        return self._code_name

    @property
    def mem_load(self):
        return self._mem_load

    @property
    def joint_load(self):
        return self._joint_load

    @property
    def profile(self):
        return self._profile

    @property
    def ir_range(self):
        return self._ir_range

    @property
    def sort(self):
        return self._sort

    @property
    def fail(self):
        return self._fail

    @property
    def sort_order(self):
        return self._sort_order

    @property
    def reverse(self):
        return self._reverse

    @property
    def mem_set_index(self):
        return self._mem_set_index

    @property
    def joint_set_index(self):
        return self._joint_set_index

    @property
    def code_set_index(self):
        return self._code_set_index

    @property
    def mem_set_name(self):
        return self._mem_set_name

    @property
    def joint_set_name(self):
        return self._joint_set_name

    @property
    def code_set_name(self):
        return self._code_set_name

    @results_parameters.setter
    def results_parameters(self, value):
        self._results_parameters = value

    @joint.setter
    def joint(self, value):
        self._joint = value

    @mem_name.setter
    def mem_name(self, value):
        self._mem_name = value

    @joint_name.setter
    def joint_name(self, value):
        self._joint_name = value

    @code_name.setter
    def code_name(self, value):
        self._code_name = value

    @mem_load.setter
    def mem_load(self, value):
        self._mem_load = value

    @joint_load.setter
    def joint_load(self, value):
        self._joint_load = value

    @profile.setter
    def profile(self, value):
        self._profile = value

    @ir_range.setter
    def ir_range(self, value):
        self._ir_range = value

    @sort.setter
    def sort(self, value):
        self._sort = value

    @fail.setter
    def fail(self, value):
        self._fail = value

    @sort_order.setter
    def sort_order(self, value):
        self._sort_order = value

    @reverse.setter
    def reverse(self, value):
        self._reverse = value

    @mem_set_name.setter
    def mem_set_name(self, value):
        self._mem_set_name = value

    @joint_set_name.setter
    def joint_set_name(self, value):
        self._joint_set_name = value

    @code_set_name.setter
    def code_set_name(self, value):
        self._code_set_name = value

    @mem_set_index.setter
    def mem_set_index(self, value):
        self._mem_set_index = value

    @joint_set_index.setter
    def joint_set_index(self, value):
        self._joint_set_index = value

    @code_set_index.setter
    def code_set_index(self, value):
        self._code_set_index = value



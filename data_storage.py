class ResultsParameters:

    def __init__(self, result_type):
        """
        Sets default result parameter values
        :param result_type: the major result type being requested (will correspond to the active tab name)
        """
        self.type = result_type

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

    # dictionary to be used in generating final output
    @property
    def results_parameters(self):
        return self.possible_result_types[self.type]

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

    @joint.setter
    def joint(self, value):
        pass

    @mem_name.setter
    def mem_name(self, value):
        pass

    @joint_name.setter
    def joint_name(self, value):
        pass

    @code_name.setter
    def code_name(self, value):
        pass

    @mem_load.setter
    def mem_load(self, value):
        pass

    @joint_load.setter
    def joint_load(self, value):
        pass

    @mem_set_name.setter
    def mem_set_name(self, value):
        pass

    @joint_set_name.setter
    def joint_set_name(self, value):
        pass

    @code_set_name.setter
    def code_set_name(self, value):
        pass

    @mem_set_index.setter
    def mem_set_index(self, value):
        pass

    @joint_set_index.setter
    def joint_set_index(self, value):
        pass

    @code_set_index.setter
    def code_set_index(self, value):
        pass

    @profile.setter
    def profile(self, value):
        pass

    @joint.deleter  # deletes the corresponding dictionary entry, may want to use this to set values to default
    # instead of just deleting them. Need to figure out how to address that the 'values' are
    # actually lists and I may only want to delete a specific value within that list, not the
    # whole value
    def joint(self):
        key = 'Joint'
        if key in self.possible_result_types[self.type]:
            del self.possible_result_types[self.type][key]
        else:
            pass

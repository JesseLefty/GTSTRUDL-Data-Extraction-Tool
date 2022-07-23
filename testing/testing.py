#!/usr/bin/env python3

import sys
import os
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__))+'/..')
from Tools import utilities, data_storage, shared_stuff
from DataProcessing import check_input_errors


test_input_file = 'test_input_file.gto'
shared_stuff.data_store = data_storage.ResultsParameters()


class TestUtilities:

    def test_read_input_file(self):

        test_file_list = utilities.ReadInputFile(test_input_file).file_list()
        expected_output = '    *RESULTS OF LATEST ANALYSES*'
        assert test_file_list[1463] == expected_output

    def test_get_display(self):

        test_index1, result1 = utilities.GenerateDisplayData(test_input_file).get_display('Member Force')
        test_index2, result2 = utilities.GenerateDisplayData(test_input_file).get_display('Joint Reaction')
        test_index3, result3 = utilities.GenerateDisplayData(test_input_file).get_display('Code Check')

        assert test_index1[2] == "LIST FORCES GRP 'SBRACE'"
        assert result1[2] == '{  673}'
        assert test_index2[0] == "LIST REACTIONS"
        assert result2[0] == '{  670}'
        assert test_index3[1] == "CHECK MEM GRP 'FBRACE' GRP 'STWF' 149 151 AS COLUMN"
        assert result3[1] == '{  703}'


class TestDataStorage:

    test_results_parameters = data_storage.ResultsParameters()
    test_results_parameters.tab_name = 'Member Force'

    def test_reset(self):
        self.test_results_parameters.name = (2, 'starts')
        self.test_results_parameters.load = (3, 'ends')
        assert self.test_results_parameters.name == (2, 'starts')
        assert self.test_results_parameters.load == (3, 'ends')
        self.test_results_parameters.reset()
        self.test_results_parameters.tab_name = 'Member Force'
        assert self.test_results_parameters.name == []
        assert self.test_results_parameters.load == []


class TestCheckInputErrors:

    test_results_parameters = shared_stuff.data_store
    test_results_parameters.input_file = test_input_file

    def test_is_input_error(self):
        self.test_results_parameters.tab_name = 'Member Force'
        self.test_results_parameters.load = [(2, 'nonsense')]
        self.test_results_parameters.name = [(1, 'ALL')]
        self.test_results_parameters.joint = ['ALL']
        self.test_results_parameters.set_index = [0]
        test_dict = check_input_errors.FindInputErrors('Member Force')
        test_dict.find_error(0)
        print(test_dict.error_dict)
        assert test_dict.error_dict[1] == (False, ['NONSENSE'])
        assert test_dict.is_input_error(None) is True

    def test_is_user_criteria_valid(self):
        user_choice = [1, 2, 3, 4, 5]
        available_results = ['BEAM1', 'BEAM10', 'BEAM20', 'LOAD1', 'LOAD10', 'LOAD20']
        user_criteria_valid = ['ALL', 'B', '10', '1', 'Beam10, Load20, Beam1']
        test_valid_results = [True, True, True, True, True]
        user_criteria_invalid = ['ALL', 'A', '15', 'Z', 'BEAM10, LOAD020, BEAM1']
        test_invalid_results = [True, False, False, False, False]
        invalid_results_list = [[], ['A'], ['15'], ['Z'], ['LOAD020']]

        for index, item in enumerate(user_choice):
            print(index, item, user_criteria_valid[index])
            print(check_input_errors.is_user_criteria_valid(item, available_results, user_criteria_valid[index]))
            assert check_input_errors.is_user_criteria_valid(item, available_results, user_criteria_valid[index]) == \
                   test_valid_results[index]
            assert check_input_errors.is_user_criteria_valid(item, available_results, user_criteria_invalid[index]) == \
                   test_invalid_results[index]
            assert check_input_errors.get_invalid_results(item, available_results, user_criteria_invalid[index]) == \
                   invalid_results_list[index]






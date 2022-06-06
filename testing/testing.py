#!/usr/bin/env python3

import sys
import os
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__))+'/..')
from Tools import utilities, data_storage

test_input_file = 'test_input_file.gto'


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
        assert test_index2[0] == "RESULTANT JOINT LOADS SUPPORTS"
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



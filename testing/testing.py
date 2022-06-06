#!/usr/bin/env python3

import sys
import os
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__))+'/..'+'/Tools')
import utilities


class TestUtilities:

    def test_read_input_file(self):

        test_file_list = utilities.ReadInputFile('test_input_file.gto').file_list()
        expected_output = ' {   52} > 38		-25.25		433.396		40.083'
        assert test_file_list[4] == expected_output


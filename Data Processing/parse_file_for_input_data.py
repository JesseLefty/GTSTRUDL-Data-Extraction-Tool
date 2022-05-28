"""
This module provides the first pass parsing of the .gto file and generates information related to the member force
results, joint reaction results, and code check results such as .gto file line number and .gto input syntax.
"""
import utilities
import shared_stuff
from config import result_configuration_parameters


class ParseFileForData:
    """
            Reads GTO file and returns list of lines containing relevant result information.

            :param:
                set_num (int): index of the user generated result set for which the data is requested
                tab_name (str): name of the tab from which the user clicked 'generate'
            """
    def __init__(self, set_num, tab_name):
        self.tab_name = tab_name
        self.results = shared_stuff.data_store
        self.results.tab_name = self.tab_name
        self.set_num = set_num
        self.input_file = self.results.input_file
        self.result_set = self.results.set_index
        self.file_list = utilities.ReadInputFile(self.input_file).file_list()

    def get_result_positions(self):
        """
        Searches the input file for trigger. Returns a list of line numbers in input file which contain the trigger.
                :param:
                    self

                :return:
                    index_list (int): the index position of the specific result set being requested
        """
        trigger_string = result_configuration_parameters[self.tab_name]['Trigger String']
        index_list = [i for i, e in enumerate(self.file_list) if trigger_string in e]
        return index_list[self.result_set[self.set_num]]

    def get_result_list_info(self):
        """
        Determines the index (line number) of first useful line and last useful line of the input file which contains
        the block of requested data for the joint set. Generates a list containing every line of the input file in the
        requested data block.

            :param:
                self

            :return:
                extracted_result_list (list):       flattened list of all lines in requested data block
                end_index (int):                    index at end of requested data block
                first_useful_line (int):            index at start of requested data block
        """
        index_for_result_set = self.get_result_positions()
        first_useful_line = index_for_result_set + result_configuration_parameters[self.tab_name]['Skip Lines']
        end_index = 0
        extracted_result_list = []
        stop = False
        end_trigger = result_configuration_parameters[self.tab_name]['End Trigger']
        for i, line in enumerate(self.file_list[first_useful_line:]):
            if self.tab_name == 'Code Check':
                if end_trigger in self.file_list[first_useful_line + i]:
                    stop = True
            else:
                if self.file_list[first_useful_line + i].startswith(end_trigger):
                    stop = True
            if stop:
                end_index = first_useful_line + i
                extracted_result_list.append(line)
                break
            extracted_result_list.append(line)
        extracted_result_list = [x for x in extracted_result_list if x != ""]
        return extracted_result_list, end_index, first_useful_line

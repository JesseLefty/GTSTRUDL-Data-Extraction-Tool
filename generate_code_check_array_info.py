import utilities_GUI


class ParseFileForData:
    """
            Parses the input file for data specific to joint reactions.

            Parameters:
                code_list_index (int): index of the user generated result set for which the data is requested
                input_file (str): input file to be parsed
                code_list (list): list of all requested code checks
            """
    def __init__(self, code_list_index, input_file, code_list):
        self.code_list_index = code_list_index
        self.input_file = input_file
        self.code_list = code_list
        self.file_list = utilities_GUI.ReadInputFile(input_file).file_list()

    def get_check_positions(self):
        """
        Searches the input file for trigger. Returns a list of line numbers in input file which contain the trigger.
                :parameter
                    self

                Returns:
                    index (int): the index position of the specific code check set being requested
        """
        trigger_string = 'DESIGN TRACE OUTPUT'
        result = []
        for index, row in enumerate(self.file_list):
            if trigger_string in row:
                result.append(index)
            else:
                pass
        index = result[self.code_list[self.code_list_index]]
        return index

    def get_code_check_list_info(self):
        """
        Determines the index (line number) of first useful line and last useful line of the input file which contains
        the block of requested data for the code check set. Generates a list containing every line of the input file in
        the requested data block.

            Parameters:
                self

            Returns:
                code_check (list):      flattened list of all lines in requested data block
                end_index (int):           index at end of requested data block
                first_useful_line (int):   index at start of requested data block
        """
        index_for_check_set = self.get_check_positions()
        first_useful_line = index_for_check_set + 13
        end_index = 0
        code_check = []
        for i, line in enumerate(self.file_list[first_useful_line:]):
            if 'END OF TRACE OUTPUT' in self.file_list[first_useful_line + i]:
                end_index = first_useful_line + i
                code_check.append(line)
                break
            else:
                code_check.append(line)
        code_check = [x for x in code_check if x != ""]
        return code_check, end_index, first_useful_line

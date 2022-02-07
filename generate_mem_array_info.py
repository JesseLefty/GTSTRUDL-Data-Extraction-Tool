import utilities_GUI


class ParseFileForData:
    """
            Parses the input file for data specific to joint reactions.

            Parameters:
                num_mem_set (int): index of the user generated result set for which the data is requested
                input_file (str): input file to be parsed
                member_set (list): list of all requested joint sets
            """
    def __init__(self, num_mem_set, input_file, member_set):
        self.num_mem_set = num_mem_set
        self.input_file = input_file
        self.member_set = member_set
        self.file_list = utilities_GUI.ReadInputFile(input_file).file_list()

    def get_force_positions(self):
        """
        Searches the input file for trigger. Returns a list of line numbers in input file which contain the trigger.
                Parameters:
                    self

                Returns:
                    index_list (int): the index position of the specific joint set being requested
        """
        trigger_string = 'LIST FOR'
        result = [v for v in self.file_list if trigger_string in v]
        index_list = [self.file_list.index(result[i]) for i in range(len(result))]
        return index_list[self.member_set[self.num_mem_set]]

    def get_member_force_list_info(self):
        """
        Determines the index (line number) of first useful line and last useful line of the input file which contains
        the block of requested data for the joint set. Determines the number of load combinations and number of joints
        in the requested data set. Generates a list containing every line of the input file in the requested data block.

            Parameters:
                self

            Returns:
                joint_reactions (list):    flattened list of all lines in requested data block
                lc_count (int):            the number of load combinations
                truss_member (bool):       True / False to indicate whether the data block contains a truss member
                joint_num (int):           number of joints in data block
                end_index (int):           index at end of requested data block
                first_useful_line (int):   index at start of requested data block
        """
        index_for_mem_set = self.get_force_positions()
        first_useful_line = index_for_mem_set + 24
        end_index = 0
        next_line = 0
        for i, line in enumerate(self.file_list):
            if not self.file_list[first_useful_line + next_line].startswith('1'):
                next_line += 1
            else:
                end_index = first_useful_line + next_line
                break
        blanks = self.file_list[first_useful_line:end_index].count("")
        mem_num = blanks + 1
        member_forces = list(filter(None, self.file_list[first_useful_line - 2:end_index]))
        truss_member = False
        if not any('MOMENT' in st for st in self.file_list[index_for_mem_set:first_useful_line - 2]):
            lc_count = int((end_index - first_useful_line - blanks) / mem_num)
            truss_member = True
        else:
            lc_count = int((end_index - first_useful_line - blanks) / (mem_num * 2))
        return member_forces, lc_count, truss_member, mem_num, end_index, first_useful_line

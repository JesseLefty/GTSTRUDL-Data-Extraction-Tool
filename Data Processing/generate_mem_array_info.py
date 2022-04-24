import utilities_GUI
import shared_stuff


class ParseFileForData:
    """
            Parses the input file for data specific to joint reactions.

            Parameters:
                num_mem_set (int): index of the user generated result set for which the data is requested
                tab_name (str): name of the tab from which the user clicked 'generate'
            """
    def __init__(self, num_mem_set, tab_name):
        self.results = shared_stuff.data_store
        self.results.tab_name = tab_name
        self.num_mem_set = num_mem_set
        self.input_file = self.results.input_file
        self.member_set = self.results.set_index
        self.file_list = utilities_GUI.ReadInputFile(self.input_file).file_list()

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
        the block of requested data for the joint set. Generates a list containing every line of the input file in the
        requested data block.

            Parameters:
                self

            Returns:
                member_forces (list):      flattened list of all lines in requested data block
                end_index (int):           index at end of requested data block
                first_useful_line (int):   index at start of requested data block
        """
        index_for_mem_set = self.get_force_positions()
        first_useful_line = index_for_mem_set + 22
        end_index = 0
        member_forces = []
        for i, line in enumerate(self.file_list[first_useful_line:]):
            if self.file_list[first_useful_line + i].startswith('1'):
                end_index = first_useful_line + i
                member_forces.append(line)
                break
            else:
                member_forces.append(line)
        member_forces = [x for x in member_forces if x != ""]

        return member_forces, end_index, first_useful_line

import utilities_GUI
import shared_stuff


class ParseFileForData:
    """
            Parses the input file for data specific to joint reactions.

            Parameters:
                num_joint_set (int): index of the user generated result set for which the data is requested
                tab_name (str): name of the tab from which the user clicked 'generate'
            """
    def __init__(self, num_joint_set, tab_name):
        self.results = shared_stuff.data_store
        self.results.tab_name = tab_name
        self.num_joint_set = num_joint_set
        self.input_file = self.results.input_file
        self.joint_set = self.results.set_index
        self.file_list = utilities_GUI.ReadInputFile(self.input_file).file_list()

    def get_reaction_positions(self):
        """
        Searches the input file for trigger. Returns a list of line numbers in input file which contain the trigger.
                Parameters:
                    self

                Returns:
                    index_list (int): the index position of the specific joint set being requested
        """
        trigger_string = 'RESULTANT JOINT LOADS SUPPORTS'
        index_list = [i for i, e in enumerate(self.file_list) if trigger_string in e]
        return index_list[self.joint_set[self.num_joint_set]]

    def get_joint_reaction_list_info(self):
        """
        Determines the index (line number) of first useful line and last useful line of the input file which contains
        the block of requested data for the joint set. Determines the number of load combinations and number of joints
        in the requested data set. Generates a list containing every line of the input file in the requested data block.

            Parameters:
                self

            Returns:
                joint_reactions (list):    flattened list of all lines in requested data block
                end_index (int):           index at end of requested data block
                first_useful_line (int):   index at start of requested data block
        """
        index_for_joint_set = self.get_reaction_positions()
        first_useful_line = index_for_joint_set + 3
        end_index = 0
        joint_reactions = []
        for i, line in enumerate(self.file_list[first_useful_line:]):
            if self.file_list[first_useful_line + i].startswith('1'):
                end_index = first_useful_line + i
                joint_reactions.append(line)
                break
            else:
                joint_reactions.append(line)
        joint_reactions = [x for x in joint_reactions if x != ""]
        return joint_reactions, end_index, first_useful_line

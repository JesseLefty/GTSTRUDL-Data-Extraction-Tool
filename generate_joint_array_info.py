import utilities_GUI
import pprint

class ParseFileForData:
    """
            Parses the input file for data specific to joint reactions.

            Parameters:
                num_joint_set (int): index of the user generated result set for which the data is requested
                input_file (str): input file to be parsed
                joint_set (list): list of all requested joint sets
            """
    def __init__(self, num_joint_set, input_file, joint_set):
        self.num_joint_set = num_joint_set
        self.input_file = input_file
        self.joint_set = joint_set
        self.file_list = utilities_GUI.ReadInputFile(input_file).file_list()

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


# input_file = 'C:/Users/Jesse/PycharmProjects/GTSTRUDL_Load_Pulling/Supporting Documents/CALC-49 Rev1_v6.0.gto'
# member_set = [0, 1, 2]
# num_mem_set = 2
# file_list = utilities_GUI.ReadInputFile
# items = 0
# beam_id = [(4, 'ALL')]
# load_id = [(3, 'SSE')]
# joint = ['ALL']
#
# ParseFileForData(num_mem_set, input_file, member_set).get_joint_reaction_list_info()

"""
This module generates a default dictionary of joint reaction results from the .gto file, parses the default dictionary
based on user input requirements, and provides a final dictionary containing only the subset of items matching the user
requirements. This module works for joint reaction result at a time.
"""
from Tools.utilities import TupleDict
from Tools import shared_stuff
from Tools.available_result_classes import JointReactionBlock
from Tools.available_result_tools import valid_names, valid_loads


class GenerateOutputArray:
    """
    Formats the joint reaction list and compiles a list of results which meet the user requirements.

    :param  tab_name (str):             name of active tab
    :param  num_joint_set (int):        index of the user generated result set for which the data is requested
    :param  joint_reactions (list):     flattened list of all lines in requested data block
    """
    def __init__(self, tab_name, num_joint_set, joint_reactions):
        self.num_joint_set = num_joint_set
        self.results = shared_stuff.data_store
        self.results.tab_name = tab_name
        self.joint_reactions = joint_reactions
        self.joint_spec = self.results.name
        self.load_spec = self.results.load

    def joint_reaction_list(self):
        """
        Generates a formatted dictionary of joint reactions with all elements in list containing joint, load, and 6
        results. Also generates a list of joint names and corresponding load cases

        :return full_d (list):      dictionary of formatted joint results
        :return joint_names (list): list joint meeting user joint_spec criteria
        :return load_cases (list):  list of loads meeting user load_spec criteria
        """
        complete_column_start_idx = [0, 10, 19, 28, 44, 59, 75, 91, 107]
        line_end = [123]
        joint_reactions_result_block = JointReactionBlock(self.joint_reactions[1:-1], complete_column_start_idx + line_end)
        headers = joint_reactions_result_block.header
        column_start = complete_column_start_idx[0:len(headers) + 3] + line_end
        value_columns = complete_column_start_idx[4: 4 + len(headers)] + line_end
        full_d = {}
        full_d = TupleDict(full_d)
        load_cases = []
        joint_names = valid_names(joint_reactions_result_block.joint_names, self.joint_spec, self.num_joint_set)
        for joint in joint_names:
            block = joint_reactions_result_block.get_block(joint)
            loads = joint_reactions_result_block.get_load_names(block)
            for row_id, row in enumerate(block[1:], 1):
                numbers = []
                joint_reaction_row = "".join(block[row_id]).split()
                joint_reaction_row.insert(0, joint)
                for ih, col_id in enumerate(value_columns):
                    if col_id > len(row) + 1:
                        numbers.append(False)
                    elif "." in row[column_start[ih + 3]:col_id]:
                        numbers.append(True)
                    else:
                        numbers.append(False)
                for number_id, value in enumerate(numbers):
                    if value:
                        pass
                    else:
                        joint_reaction_row.insert(2 + number_id, " ")
                k = tuple(joint_reaction_row[0:2])
                full_d[k] = joint_reaction_row[2:]
            load_cases.append(loads)
        return full_d, joint_names, load_cases

    def requested_joint_reaction_dict(self):
        """
        Builds a dictionary of key / value pairs which match the joint and load criteria requested by the user.

        :return output (dict):     dictionary of key / value pairs which match all joint and load, criteria
                                    specified by the user
        """
        d, all_joints, all_loads = self.joint_reaction_list()
        user_joints = valid_names(all_joints, self.joint_spec, self.num_joint_set)
        user_loads = valid_loads(all_loads, self.load_spec, self.num_joint_set)
        output = {}
        for j_idx, joints in enumerate(user_joints):
            for loads in user_loads[j_idx]:
                t = (joints, loads)
                output[t] = d[t]
        for k, v in output.items():
            output[k] = [float(x) if not x == ' ' else x for x in v]
        return output

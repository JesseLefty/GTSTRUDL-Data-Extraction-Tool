"""
This module generates a default dictionary of member force results from the .gto file, parses the default dictionary
based on user input requirements, and provides a final dictionary containing only the subset of items matching the user
requirements. This module works for member force result at a time.
"""
from Tools.utilities import TupleDict
from Tools import shared_stuff
from Tools.available_result_classes import MemberForceBlock
from Tools.available_result_tools import valid_names, valid_loads


class GenerateOutputArray:
    """
        Formats the joint reaction list and compiles a list of results which meet the user requirements.

        :param  tab_name (str):             name of active tab
        :param  mem_set_index (int):        index of the user generated result set for which the data is requested
        :param  member_forces (list):     flattened list of all lines in requested data block
        """
    def __init__(self, tab_name, mem_set_index, member_forces):
        self.mem_set_index = mem_set_index
        self.results = shared_stuff.data_store
        self.results.tab_name = tab_name
        self.joint = self.results.joint[self.mem_set_index]
        self.member_forces = member_forces
        self.beam_id = self.results.name
        self.load_id = self.results.load

    def member_force_array(self):
        """
        Generates a formatted dictionary of joint reactions with all elements in list containing joint, load, and 6
        results. Also generates a list of joint names and corresponding load cases

        :return full_d (list):      dictionary of formatted member force
        :return beam_names (list): list joint meeting user beam spec criteria
        :return load_names (list):  list of loads meeting user load_spec criteria
        """
        complete_column_start_idx = [0, 10, 19, 28, 44, 60, 76, 92, 108]
        line_end = [124]
        member_force_result_block = MemberForceBlock(self.member_forces[1:-1], complete_column_start_idx + line_end)
        headers = member_force_result_block.header
        column_start = complete_column_start_idx[0:len(headers) + 3] + line_end
        value_columns = complete_column_start_idx[4: 4 + len(headers)] + line_end
        full_d = {}
        full_d = TupleDict(full_d)
        load_cases = []
        beam_names = valid_names(member_force_result_block.member_names, self.beam_id, self.mem_set_index)
        for beam in beam_names:
            block = member_force_result_block.get_block(beam)
            loads = member_force_result_block.get_load_names(block)
            for row_id, row in enumerate(block):
                numbers = []
                column_2 = row[column_start[1]: column_start[2]].strip()
                formatted_array = "".join(block[row_id]).split()
                if row_id > 0:
                    formatted_array.insert(0, beam)
                if column_2:
                    load = row[column_start[1]: column_start[2]].strip()
                if column_2 == "":
                    formatted_array.insert(1, load)
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
                        formatted_array.insert(3 + number_id, " ")
                k = tuple(formatted_array[0:3])
                full_d[k] = formatted_array[3:]
            load_cases.append(loads)
        return full_d, beam_names, load_cases

    def requested_member_force_array(self):
        """
        Builds a dictionary of key / value pairs which match the beam and load criteria requested by the user.

        :return output (dict):     dictionary of key / value pairs which match all beam and load, criteria
                                    specified by the user
        """
        d, all_beams, all_loads = self.member_force_array()
        user_beams = valid_names(all_beams, self.beam_id, self.mem_set_index)
        user_loads = valid_loads(all_loads, self.load_id, self.mem_set_index)
        d_joints = {}
        output = {}
        for key, value in d.items():
            if (key[0] in d_joints) and (key[2] not in d_joints[key[0]]):
                key_list = d_joints[key[0]]
                key_list.append(key[2])
                d_joints[key[0]] = key_list
            else:
                d_joints[key[0]] = [key[2]]
        for b_idx, beams in enumerate(user_beams):
            current_beam = beams
            indices = [0] if self.joint == 'START' else [1] if self.joint == 'END' else \
                range(len(d_joints[current_beam]))
            for loads in user_loads[b_idx]:
                current_load = loads
                for index in indices:
                    if index == len(d_joints[current_beam]):
                        index = 0
                    else:
                        pass
                    t = (current_beam, current_load, d_joints[current_beam][index])
                    output[t] = d[t]
        for k, v in output.items():
            output[k] = [float(x) if not x == ' ' else x for x in v]
        return output

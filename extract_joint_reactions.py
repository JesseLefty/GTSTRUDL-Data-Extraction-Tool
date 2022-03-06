import utilities_GUI
import generate_joint_array_info
import re


class GenerateOutputArray:
    """
            Formats the joint reaction list and compiles a dictionary of requested joints and load combinations and the
            corresponding results.

            Parameters:
                num_joint_set (int):        index of the user generated result set for which the data is requested
                joint_reactions (list):     flattened list of all lines in requested data block
                joint_spec (list):          list of tuples containing joint parameter id and user joint input text
                load_spec (list):           list of tuples containing load parameter id and user load input text
            """
    def __init__(self, num_joint_set, joint_reactions, joint_spec, load_spec):
        self.num_joint_set = num_joint_set
        self.joint_reactions = joint_reactions
        self.joint_spec = joint_spec
        self.load_spec = load_spec
        self.joint_error = []
        self.load_error = []

    def joint_reaction_list(self):
        """
        Generates a formatted list of joint reactions with all elements in list containing joint, load, and 6 results.
        Also returns the subset of joints and loads which meet the user requested joint and load specs.

            Parameters:
                self

            Returns:
                 formatted_reaction_list (list):    nested list of formatted joint results
                 joint_names (list):                list joint meeting user joint_spec criteria
                 joint_loads (list):                list of loads meeting user load_spec criteria
        """
        joint_names = []
        joint_index = []
        load_cases = []
        header_line = self.joint_reactions[0]
        headers = re.split(r'\s{2,}', header_line)[1:]
        joint_reactions = self.joint_reactions[1:]
        complete_column_start_idx = [0, 10, 19, 28, 44, 59, 75, 91, 107]
        line_end = [123]
        #TODO: Get rid of these magic numbers
        column_start = complete_column_start_idx[0:len(headers) + 3] + line_end
        value_columns = complete_column_start_idx[4: 4 + len(headers)] + line_end
        full_d = {}
        full_d = utilities_GUI.TupleDict(full_d)
        for row_num, line in enumerate(joint_reactions):
            column_1 = line[column_start[0]: column_start[1]].strip()
            if (column_1 or column_1.startswith('1')) and not column_1.startswith("****"):
                joint_names.append([column_1])
                joint_index.append(row_num)
        joint_names.pop()
        for block_id, joint in enumerate(joint_names):
            block_load = []
            block_start = joint_index[block_id: block_id + 2][0] + 1
            block_end = joint_index[block_id: block_id + 2][1]
            block = joint_reactions[block_start:block_end]
            for row_id, row in enumerate(block):
                numbers = []
                joint_reaction_row = "".join(block[row_id]).split()
                column_3 = row[column_start[2]: column_start[3]].strip()
                if '****' in joint_reaction_row[0]:
                    pass
                else:
                    joint_reaction_row.insert(0, joint[0])
                    if column_3:
                        load = row[column_start[2]: column_start[3]].strip()
                        block_load.append(load)
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
                load_cases.append(block_load)
        return full_d, joint_names, load_cases

    def user_input_sorting(self, joint_names, load_names):
        """
        Takes the full list of beam and load names and generates a sub list based on the user specified beam_id
        requirements. The returned values are nested lists in which the index of the nested list is the same for
        each beam and load in the block.

            Parameters:
                joint_names:         full list of joint names for each block
                load_names:          full list of load names for each block

            Returns:
                 user_joints (list):     list of lists of joint names which meet the user criteria
                 user_loads (list):      list of lists of load names which meet the user criteria
        """

        joint_choice = self.joint_spec[self.num_joint_set][0]
        load_choice = self.load_spec[self.num_joint_set][0]
        user_loads = []
        user_joints = []
        load = []
        if joint_choice == 2:
            joint_starts_with = self.joint_spec[self.num_joint_set][1]
            for b_idx, joints in enumerate(joint_names):
                if joints[0].startswith(joint_starts_with):
                    user_joints.append(joints)
                    load.append(load_names[b_idx])
                else:
                    pass
            if not user_joints:
                self.joint_error.append(joint_starts_with)
        elif joint_choice == 3:
            joint_ends_with = self.joint_spec[self.num_joint_set][1]
            for b_idx, joints in enumerate(joint_names):
                if joints[0].endswith(joint_ends_with):
                    user_joints.append(joints)
                    load.append(load_names[b_idx])
                else:
                    pass
            if not user_joints:
                self.joint_error.append(joint_ends_with)
        elif joint_choice == 4:
            joint_contains = self.joint_spec[self.num_joint_set][1]
            for b_idx, joints in enumerate(joint_names):
                if joint_contains in joints[0]:
                    user_joints.append(joints)
                    load.append(load_names[b_idx])
                else:
                    pass
            if not user_joints:
                self.joint_error.append(joint_contains)
        elif joint_choice == 5:
            joint_text = self.joint_spec[self.num_joint_set][1].upper()
            joint_list = "".join(joint_text).replace(" ", "").split(',')
            for item in joint_list:
                try:
                    b_idx = joint_names.index([item])
                    user_joints.append([item])
                    load.append(load_names[b_idx])
                except ValueError:
                    self.joint_error.append(item)
        else:
            user_joints = joint_names
            load = load_names
        if load:
            if load_choice == 2:
                load_starts_with = self.load_spec[self.num_joint_set][1]
                for l_idx, loads in enumerate(load):
                    matching_loads = [l for l in loads if l.startswith(load_starts_with)]
                    user_loads.append(matching_loads)
                if not user_loads[0]:
                    self.load_error.append(load_starts_with)
            elif load_choice == 3:
                load_ends_with = self.load_spec[self.num_joint_set][1]
                for l_idx, loads in enumerate(load):
                    matching_loads = [l for l in loads if l.endswith(load_ends_with)]
                    user_loads.append(matching_loads)
                if not user_loads[0]:
                    self.load_error.append(load_ends_with)
            elif load_choice == 4:
                load_contains = self.load_spec[self.num_joint_set][1]
                for l_idx, loads in enumerate(load):
                    matching_loads = [l for l in loads if load_contains in l]
                    user_loads.append(matching_loads)
                if not user_loads[0]:
                    self.load_error.append(load_contains)
            elif load_choice == 5:
                load_text = self.load_spec[self.num_joint_set][1].upper()
                load_list = "".join(load_text).replace(" ", "").split(',')
                for l_idx, loads in enumerate(load):
                    for item in load_list:
                        if item in load[l_idx]:
                            user_loads.append([item])
                        else:
                            self.load_error.append(item)
            else:
                user_loads = load
        else:
            pass
        if user_joints:
            if user_loads:
                for b_idx, joints in enumerate(user_joints):
                    if not user_loads[b_idx]:
                        del user_joints[b_idx]
                        del user_loads[b_idx]
            else:
                user_joints.clear()
        else:
            user_loads.clear()
        return user_joints, user_loads

    def requested_joint_reaction_dict(self):
        """
        Builds a dictionary key / value pairs which match the joint and load criteria requested by the user.
            Parameters:
                self

            Returns:
                 output (dict):     dictionary of key / value pairs which match all joint and load, criteria
                                    specified by the user
        """
        d, all_joints, all_loads = self.joint_reaction_list()
        user_joints, user_loads = self.user_input_sorting(all_joints, all_loads)
        output = {}
        if not user_joints or not user_loads:
            pass
        else:
            for j_idx, joints in enumerate(user_joints):
                current_joint = joints[0]
                for l_idx, loads in enumerate(user_loads[j_idx]):
                    current_load = loads
                    t = (current_joint, current_load)
                    output[t] = d[t]
        errors = (list(set(self.joint_error)), list(set(self.load_error)))
        return output, errors

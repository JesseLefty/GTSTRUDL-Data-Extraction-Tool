import utilities_GUI
import re


class GenerateOutputArray:
    """
            Formats the joint reaction list and compiles a dictionary of requested joint, load combinations, members
            and the corresponding results.

            Parameters:
                joint (list):               list indicating start, end, or all joints are requested
                mem_set_index (int):        index of the user generated result set for which the data is requested
                member_forces (list):       flattened list of all lines in requested data block
                beam_id (list):             list of tuples containing joint parameter id and user joint input text
                load_id (list):             list of tuples containing load parameter id and user load input text
            """
    def __init__(self, joint, mem_set_index, member_forces, beam_id, load_id):
        self.joint = joint[mem_set_index]
        self.mem_set_index = mem_set_index
        self.member_forces = member_forces
        self.beam_id = beam_id
        self.load_id = load_id

    def member_force_array(self):
        """
        Generates a formatted list of member forces with all elements in list containing beam, load, joint,
        and 6 results. Subdivides each result set into 'blocks'. The size of each block is the number of rows for a
        given member.

            Parameters:
                self

            Returns:
                 formatted_member_forces_array (list):      nested list of formatted member results
                 beam_names (list):                         list all beam names in the results set
                 load_names (list):                         list all load names in teh results set
        """
        beam_names = []
        formatted_member_forces_array = []
        beam_index = []
        header_line = self.member_forces[0]
        headers = re.split(r'\s{2,}', header_line)[1:]
        member_forces = self.member_forces[1:]
        complete_column_start_idx = [0, 10, 19, 28, 45, 61, 77, 93, 109]
        line_end = [124]
        column_start = complete_column_start_idx[0:len(headers) + 3] + line_end
        value_columns = column_start[4:]
        for row_num, line in enumerate(member_forces):
            column_1 = line[column_start[0]: column_start[1]].strip()
            if (column_1 or column_1.startswith('1')) and not column_1.startswith("****"):
                beam_names.append(column_1)
                beam_index.append(row_num)
        beam_names.pop()
        for block_id, beam in enumerate(beam_names):
            load_cases = []
            block_start = beam_index[block_id: block_id + 2][0]
            block_end = beam_index[block_id: block_id + 2][1]
            block = member_forces[block_start:block_end]
            for row_id, row in enumerate(block):
                numbers = []
                formatted_array = "".join(block[row_id]).split()
                column_2 = row[column_start[1]: column_start[2]].strip()
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
                        formatted_array.insert(3+number_id, " ")
                if '****' in formatted_array[0]:
                    pass
                else:
                    if row_id > 0:
                        formatted_array.insert(0, beam)
                    if column_2:
                        load = row[column_start[1]: column_start[2]].strip()
                        load_cases.append(load)
                    if column_2 == "":
                        formatted_array.insert(1, load)
                    formatted_member_forces_array.append(formatted_array)
        seen = set()
        seen_add = seen.add
        load_names = [x[1] for x in formatted_member_forces_array[:] if not (x[1] in seen or seen_add(x[1]))]
        return formatted_member_forces_array, beam_names, load_names

    def beam_names(self, beam_names):
        """
        Takes the full list of beam names and generates a sub list based on the user specified beam_id requirements.
            Parameters:
                beam_names:         full list of beam names

            Returns:
                 beam (list):       list of beams which meet the user specified criteria
        """
        beam_choice = self.beam_id[self.mem_set_index][0]
        if beam_choice == 2:
            beam_starts_with = self.beam_id[self.mem_set_index][1]
            beam = [b for b in beam_names if b.startswith(beam_starts_with)]
        elif beam_choice == 3:
            beam_ends_with = self.beam_id[self.mem_set_index][1]
            beam = [b for b in beam_names if b.endswith(beam_ends_with)]
        elif beam_choice == 4:
            beam_contains = self.beam_id[self.mem_set_index][1]
            beam = [b for b in beam_names if beam_contains in b]
        elif beam_choice == 5:
            beam = self.beam_id[self.mem_set_index][1].upper()
            beam = "".join(beam).replace(" ", "").split(',')
        else:
            beam = beam_names

        return beam

    def load_names(self, load_names):
        """
        Takes the full list of load names and generates a sub list based on the user specified load_id requirements.
            Parameters:
                load_names:         full list of load names

            Returns:
                 load (list):       list of loads which meet the user specified criteria
        """
        load_choice = self.load_id[self.mem_set_index][0]
        if load_choice == 2:
            load_starts_with = self.load_id[self.mem_set_index][1]
            load = [l for l in load_names if l.startswith(load_starts_with)]
        elif load_choice == 3:
            load_ends_with = self.load_id[self.mem_set_index][1]
            load = [l for l in load_names if l.endswith(load_ends_with)]
        elif load_choice == 4:
            load_contains = self.load_id[self.mem_set_index][1]
            load = [l for l in load_names if load_contains in l]
        elif load_choice == 5:
            load = self.load_id[self.mem_set_index][1].upper()
            load = "".join(load).replace(" ", "").split(',')
        else:
            load = load_names

        return load

    def requested_member_force_array(self):
        """
        Builds a dictionary key / value pairs which match the joint, load, and beam criteria requested by the user.
            Parameters:
                self

            Returns:
                 output (dict):     dictionary of key / value pairs which match all joint, load, and beam criteria
                                    specified by the user
                 key_error (list):  list of keys which have no corresponding value pair in the output dictionary
        """
        formatted_member_forces_array, all_beams, all_loads = self.member_force_array()
        if self.beam_id[self.mem_set_index][0] != 1:
            user_beams = self.beam_names(all_beams)
        else:
            user_beams = all_beams
        if self.load_id[self.mem_set_index][0] != 1:
            user_loads = self.load_names(all_loads)
        else:
            user_loads = all_loads
        key = [el[0:3] for el in formatted_member_forces_array[:]]
        beam_names = [el[0] for el in formatted_member_forces_array[:]]
        joint_names = [el[2] for el in formatted_member_forces_array[:]]
        value = [el[3:] for el in formatted_member_forces_array[:]]
        d = {}
        d_joints = {}
        for row, item in enumerate(key):
            d[(tuple(item))] = value[row]
            beam_name_row = ''.join(beam_names[row])
            if beam_name_row in d_joints:
                pass
            else:
                d_joints[beam_name_row] = [joint_names[row], joint_names[row + 1]]
        d = utilities_GUI.TupleDict(d)
        output = {}
        key_error = []
        for beams in user_beams:
            try:
                indices = [0] if self.joint == 'START' else [1] if self.joint == 'END' else \
                                                                                    range(len(d_joints[beams]))
            except KeyError:
                indices = [0]
            for loads in user_loads:
                for index in indices:
                    try:
                        t = (beams, loads, d_joints[beams][index])
                    except KeyError:
                        pass
                    try:
                        output[t] = d[t]
                    except KeyError:
                        key_error.append(t)
                    except UnboundLocalError:
                        pass
        else:
            pass
        key_error = list(set(key_error))
        return output, key_error

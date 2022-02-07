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
                lc_count (int):             number of load combinations
                truss_member (bool):        True / False to indicated whether data has a truss member
                beam_id (list):             list of tuples containing joint parameter id and user joint input text
                load_id (list):             list of tuples containing load parameter id and user load input text
            """
    def __init__(self, joint, mem_set_index, member_forces, lc_count, truss_member, beam_id, load_id):
        self.joint = joint[mem_set_index]
        self.mem_set_index = mem_set_index
        self.member_forces = member_forces
        self.lc_count = lc_count
        self.truss_member = truss_member
        self.beam_id = beam_id
        self.load_id = load_id

    key_err_load = []
    key_err_beam = []

    def member_force_array(self):
        """
        Generates a formatted list of member forces with all elements in list containing beam, load, joint,
        and 6 results. Also returns the subset of joints and loads which meet the user requested joint and load specs.

            Parameters:
                self

            Returns:
                 formatted_member_forces_array (list):      nested list of formatted member results
                 user_beams (list):                         list beams meeting user beam_spec criteria
                 user_loads (list):                         list of loads meeting user load_spec criteria
        """
        formatted_force_list = []
        beam_names = []
        load_names = []
        header_line = self.member_forces[0]
        headers = re.split(r'\s{2,}', header_line)[1:]
        member_forces = self.member_forces[1:]
        column_start = []
        column_width = 16
        for i in range(len(headers)):
            column_start.append(28 + (column_width + 1) * i)
        idx_load = 0
        idx_beam = - 1
        for all_rows, line in enumerate(member_forces):
            numbers = []
            raw_member_force_array = "".join(line).split()
            if self.truss_member:
                if all_rows % self.lc_count == 0:
                    beam_names.append(raw_member_force_array[0])
                if 0 < all_rows < self.lc_count:
                    load_names.append(raw_member_force_array[0])
                if all_rows == 0:
                    load_names.append(raw_member_force_array[1])
            else:
                if all_rows % (self.lc_count*2) == 0:
                    beam_names.append(raw_member_force_array[0])
                if 0 < all_rows < self.lc_count*2 - 1 and all_rows % 2 == 0:
                    load_names.append(raw_member_force_array[0])
                if all_rows == 0:
                    load_names.append((raw_member_force_array[1]))
            formatted_force_list.append(raw_member_force_array)
            for ih, header in enumerate(headers):
                pos = column_start[ih]
                if pos > len(line):
                    numbers.append(False)
                elif "." in line[pos:pos + column_width]:
                    numbers.append(True)
                else:
                    numbers.append(False)
            if self.truss_member:
                if not all_rows % self.lc_count == 0:
                    joint_insert = len(beam_names) - 1
                    raw_member_force_array.insert(0, beam_names[joint_insert])
                else:
                    pass
            else:
                if not all_rows % (self.lc_count*2) == 0:
                    if not all_rows % 2 == 0:
                        raw_member_force_array.insert(0, load_names[idx_load])
                        raw_member_force_array.insert(0, beam_names[idx_beam])
                    else:
                        raw_member_force_array.insert(0, beam_names[idx_beam])
                        idx_load += 1
                else:
                    idx_beam += 1
                    idx_load = 0
            for idx_numbers, value in enumerate(numbers):
                if value:
                    pass
                else:
                    raw_member_force_array.insert(3 + idx_numbers, " ")
        if self.beam_id[self.mem_set_index][0] == 2:
            beam_starts_with = self.beam_id[self.mem_set_index][1]
            beam = [b for b in beam_names if b.startswith(beam_starts_with)]
        elif self.beam_id[self.mem_set_index][0] == 3:
            beam_ends_with = self.beam_id[self.mem_set_index][1]
            beam = [b for b in beam_names if b.endswith(beam_ends_with)]
        elif self.beam_id[self.mem_set_index][0] == 4:
            beam_contains = self.beam_id[self.mem_set_index][1]
            beam = [b for b in beam_names if beam_contains in b]
        elif self.beam_id[self.mem_set_index][0] == 5:
            beam = self.beam_id[self.mem_set_index][1].upper()
            beam = "".join(beam).replace(" ", "").split(',')
        else:
            beam = beam_names
        if self.load_id[self.mem_set_index][0] == 2:
            load_starts_with = self.load_id[self.mem_set_index][1]
            load = [l for l in load_names if l.startswith(load_starts_with)]
        elif self.load_id[self.mem_set_index][0] == 3:
            load_ends_with = self.load_id[self.mem_set_index][1]
            load = [l for l in load_names if l.endswith(load_ends_with)]
        elif self.load_id[self.mem_set_index][0] == 4:
            load_contains = self.load_id[self.mem_set_index][1]
            load = [l for l in load_names if load_contains in l]
        elif self.load_id[self.mem_set_index][0] == 5:
            load = self.load_id[self.mem_set_index][1].upper()
            load = "".join(load).replace(" ", "").split(',')
        else:
            load = load_names
        return formatted_force_list, beam, load

    def requested_member_force_array(self):
        """
        Builds a dictionary key / value pairs which match the joint, load, and beam criteria requested by the user.
            Parameters:
                self

            Returns:
                 output (dict):     dictionary of key / value pairs which match all joint, load, and beam criteria
                                    specified by the user
        """
        formatted_member_forces_array, user_beams, user_loads = self.member_force_array()
        key = [el[0:3] for el in formatted_member_forces_array[:]]
        beam_names = [el[0] for el in formatted_member_forces_array[:]]
        joint_names = [el[2] for el in formatted_member_forces_array[::]]
        value = [el[3:] for el in formatted_member_forces_array[:]]
        d = {}
        d_joints = {}
        for row, item in enumerate(key):
            d[(tuple(key[row]))] = value[row]
            if ''.join(beam_names[row]) in d_joints:
                pass
            else:
                d_joints[''.join(beam_names[row])] = [joint_names[row], joint_names[row + 1]]
        d = utilities_GUI.TupleDict(d)
        output = {}
        self.key_err_beam.clear()
        self.key_err_load.clear()
        for beams in user_beams:
            try:
                indices = [0] if self.joint == 'START' or self.truss_member else [1] if self.joint == 'END' else \
                                                                                    range(len(d_joints[beams]))
            except KeyError as beam_error:
                self.key_err_beam.append(beam_error.args[0])
                indices = [0]
            for loads in user_loads:
                for index in indices:
                    try:
                        t = (beams, loads, d_joints[beams][index])
                    except KeyError:
                        pass
                    try:
                        output[t] = d[t]
                    except KeyError as err:
                        self.key_err_load.append(err.args[0][1])
                    except UnboundLocalError:
                        pass
        if self.key_err_beam:
            output = {'Beam Error': self.key_err_beam}
        elif self.key_err_load:
            output = {'Load Error': self.key_err_load}
        else:
            pass
        return output

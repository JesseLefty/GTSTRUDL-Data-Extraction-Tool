class TupleDict(dict):
    """
    Rebuilds a dictionary which allows searching a key of type tuple for any value. If any item in the tuple matches the
    requested value, the entire key is returned.

            Parameters:
                dict:   dictionary which is to be converted to searchable

            Returns:    a dictionary which has a searchable tuple key
    """
    def __contains__(self, key):
        if super(TupleDict, self).__contains__(key):
            return True
        return any(key in k for k in self)


class GenerateOutputArray:
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
        Generates list used for generating dictionary key / value pairs and a 2d array of all elements in data block
        with empty spaces filled with applicable data in which the key / value pairs are used.

            Parameters:
                self

            Returns:
                 all_member_force (array):      2d array (x, 9) of member results with empty spaces filled with correct
                                                member names and load combinations
                 beam (list(str)):              list of unique beam names in data block corresponding to selected
                                                beam option
                 load (list(str)):              list of unique load combinations in data block corresponding to selected
                                                load option
        """
        standard_member_force = [' ']*9
        len_first_truss_mem = len("".join(self.member_forces[0]).split())
        for all_rows in range(len(self.member_forces)):
            raw_member_force_array = "".join(self.member_forces[all_rows]).split()
            array_length = len(raw_member_force_array)
            if array_length < 9 and not self.truss_member:
                extend = 9 - array_length
                raw_member_force_array = [' ']*extend + raw_member_force_array
            elif self.truss_member:
                extend_back = 9 - len_first_truss_mem
                raw_member_force_array = raw_member_force_array + [' '] * extend_back
                extend_front = 9 - len(raw_member_force_array)
                raw_member_force_array = [' '] * extend_front + raw_member_force_array
            else:
                pass
            standard_member_force.extend(raw_member_force_array)
        formatted_member_forces_array = [standard_member_force[i:i + 9] for i in range(0, len(standard_member_force), 9)]
        del formatted_member_forces_array[0]
        for rows in range(len(formatted_member_forces_array)):
            if formatted_member_forces_array[rows][0] == " " and formatted_member_forces_array[rows][1] == " ":
                formatted_member_forces_array[rows][0] = formatted_member_forces_array[rows - 1][0]
                formatted_member_forces_array[rows][1] = formatted_member_forces_array[rows - 1][1]
            elif formatted_member_forces_array[rows][0] == " ":
                formatted_member_forces_array[rows][0] = formatted_member_forces_array[rows - 1][0]
            else:
                pass
        if not self.truss_member:
            beam = [el[0] for el in formatted_member_forces_array[::2*self.lc_count + 1]]
            load = [el[1] for el in formatted_member_forces_array[::self.lc_count + 1]]
        else:
            beam = [el[0] for el in formatted_member_forces_array[::self.lc_count + 1]]
            load = [el[1] for el in formatted_member_forces_array[:self.lc_count]]
        if self.beam_id[self.mem_set_index][0] == 1:
            pass
        elif self.beam_id[self.mem_set_index][0] == 2:
            beam_starts_with = self.beam_id[self.mem_set_index][1]
            beam = [b for b in beam if b.startswith(beam_starts_with)]
        elif self.beam_id[self.mem_set_index][0] == 3:
            beam_ends_with = self.beam_id[self.mem_set_index][1]
            beam = [b for b in beam if b.endswith(beam_ends_with)]
        elif self.beam_id[self.mem_set_index][0] == 4:
            beam_contains = self.beam_id[self.mem_set_index][1]
            beam = [b for b in beam if beam_contains in b]
        elif self.beam_id[self.mem_set_index][0] == 5:
            beam = self.beam_id[self.mem_set_index][1].upper()
            beam = "".join(beam).replace(" ", "").split(',')
        if self.load_id[self.mem_set_index][0] == 1:
            pass
        elif self.load_id[self.mem_set_index][0] == 2:
            load_starts_with = self.load_id[self.mem_set_index][1]
            load = [l for l in load if l.startswith(load_starts_with)]
        elif self.load_id[self.mem_set_index][0] == 3:
            load_ends_with = self.load_id[self.mem_set_index][1]
            load = [l for l in load if l.endswith(load_ends_with)]
        elif self.load_id[self.mem_set_index][0] == 4:
            load_contains = self.load_id[self.mem_set_index][1]
            load = [l for l in load if load_contains in l]
        elif self.load_id[self.mem_set_index][0] == 5:
            load = self.load_id[self.mem_set_index][1].upper()
            load = "".join(load).replace(" ", "").split(',')
        return formatted_member_forces_array, beam, load

    def requested_member_force_array(self):
        """
        Builds a dictionary key / value pairs which match the beam and load criteria requested by the user.
        Generates a second dictionary based on the joint specification(all, start, end)

            Parameters:
                self

            Returns:
                 output (dict):     dictionary of key / value pairs which match all beam, load, and joint criteria
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
        d = TupleDict(d)
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

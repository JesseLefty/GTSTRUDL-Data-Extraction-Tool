import numpy as np
import generate_mem_array_info as g_mem


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


def member_force_array(beam_option, load_option, file_list):
    """
    Generates list used for generating dictionary key / value pairs and a 2d array of all elements in data block
    with empty spaces filled with applicable data in which the key / value pairs are used.

        Parameters:
            None yet - will discuss beam option and load options

        Returns:
             all_member_force (array):      2d array (x, 9) of member results with empty spaces filled with correct
                                            member names and load combinations
             beam (list(str)):              list of unique beam names in data block corresponding to selected
                                            beam option
             load (list(str)):              list of unique load combinations in data block corresponding to selected
                                            load option
    """
    member_forces, lc_count, truss_member, ph_1, ph_2, ph_3 = g_mem.get_member_force_list_info(file_list)
    standard_member_force = [' ']*9
    len_first_truss_mem = len("".join(member_forces[0]).split())
    for all_rows in range(member_forces.shape[0]):
        raw_member_force_array = np.array("".join(member_forces[all_rows]).split())
        if raw_member_force_array.shape[0] == 9:
            pass
        elif raw_member_force_array.shape[0] < 9 and not truss_member:
            extend = 9 - raw_member_force_array.shape[0]
            raw_member_force_array = np.concatenate((np.array([' ']*extend), raw_member_force_array), axis=0)
        if truss_member:
            extend_back = 9 - len_first_truss_mem
            raw_member_force_array = np.concatenate((raw_member_force_array, np.array([' '] * extend_back)), axis=0)
            extend_front = 9 - raw_member_force_array.shape[0]
            raw_member_force_array = np.concatenate((np.array([' '] * extend_front), raw_member_force_array), axis=0)
        standard_member_force = np.vstack((standard_member_force, raw_member_force_array))
    all_member_force = np.copy(standard_member_force)
    all_member_force[:] = standard_member_force[:]
    for rows in range(all_member_force.shape[0]):
        if all_member_force[rows:rows + 1, 0:1] == " " and all_member_force[rows:rows + 1, 1:2] == " ":
            all_member_force[rows, 0] = all_member_force[rows - 1, 0]
            all_member_force[rows, 1] = all_member_force[rows - 1, 1]
        elif all_member_force[rows:rows + 1, 0:1] == " ":
            all_member_force[rows, 0] = all_member_force[rows - 1, 0]
        else:
            all_member_force = all_member_force
    name_array = standard_member_force[:, [0, 1]]
    beam = [np.array(b).tolist() for b in name_array[:, [0]] if not b == ' ']
    beam = [b for sub_b in beam for b in sub_b]
    load = [np.array(l).tolist() for l in name_array[:, [1]] if not l == ' ']
    load = [l for sub_l in load for l in sub_l][0:lc_count]
    if beam_option == 1:
        pass
    elif beam_option == 2:
        beam_starts_with = 'COL1001'
        beam = [b for b in beam if b.startswith(beam_starts_with)]
    elif beam_option == 3:
        beam = ['B4010011']
    if load_option == 1:
        pass
    elif load_option == 2:
        load_starts_with = '4D+L-'
        load = [l for l in load if l.startswith(load_starts_with)]
    elif load_option == 3:
        load = ['4D+L-SSE']
    np.delete(all_member_force, 0, axis=0)
    return all_member_force, beam, load, truss_member


def requested_member_force_array(joint, beam_option, load_option, file_list):
    """
    Builds a dictionary key / value pairs which match the beam and load criteria requested by the user.
    Generates a second dictionary based on the joint specification(all, start, end)

        Parameters:
            None yet - will discuss beam option and load options

        Returns:
             output (dict):     dictionary of key / value pairs which match all beam, load, and joint criteria
                                specified by the user
    """
    member_force_array_list, user_beams, user_loads, truss_member = member_force_array(beam_option, load_option, file_list)
    key = member_force_array_list[0:, [0, 1, 2]]
    beam_names = member_force_array_list[0:, [0]].tolist()
    joint_names = member_force_array_list[0:, [2]]
    value = member_force_array_list[0:, [3, 4, 5, 6, 7, 8]].tolist()
    d = {}
    d_joints = {}
    for row, item in enumerate(key):
        d[(tuple(key[row]))] = value[row]
        if ''.join(beam_names[row]) in d_joints:
            pass
        else:
            d_joints[''.join(beam_names[row])] = [joint_names[row][0], joint_names[row + 1][0]]
    d = TupleDict(d)
    output = {}
    for beams in user_beams:
        indices = [0] if joint == 'START' or truss_member else [1] if joint == 'END' else range(len(d_joints[beams]))
        for loads in user_loads:
            for index in indices:
                t = (beams, loads, d_joints[beams][index])
                output[t] = d[t]
    return output

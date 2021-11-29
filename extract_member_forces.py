# REFORMAT THE MEMBER FORCE LIST TO FILL EACH ROW WITH REQUIRED DATA

import numpy as np
import generate_mem_array_info as g_mem
joint = 'START'
beam_option = 1     # options so far are "all" (1) or "starts with" (2) or "specific names" (3), want to add "ends with" and "contains"
load_option = 1
lc_count = g_mem.load_comb_count()


# ENSURES THE ARRAY IS ALL THE SAME SIZE (X, 9) WHERE ALL POSITIONS OF ELEMENTS ARE RETAINED IN THEIR ORIGINAL COLUMNS
def member_force_array():
    member_forces = np.array(g_mem.member_forces)
    len_first_row = len("".join(member_forces[0]).split())
    standard_member_force = [' ']*9
    for all_rows in range(member_forces.shape[0]):
        raw_member_force_array = "".join(member_forces[all_rows]).split()
        while len(raw_member_force_array) < len_first_row:
            raw_member_force_array = np.insert(raw_member_force_array, 0, " ")
            # print(raw_member_force_array)
        if len(raw_member_force_array) < 9:
            while len(raw_member_force_array) < 9:
                raw_member_force_array = np.insert(raw_member_force_array, len(raw_member_force_array), " ")
        else:
            pass
        raw_member_force_array = raw_member_force_array
        standard_member_force = np.vstack((standard_member_force, raw_member_force_array))
    return standard_member_force


# FILLS IN THE EMPTY SPACES AT THE FRONT OF THE ARRAY  WITH THE REQUIRED DATA. I.E, START EACH ROW WITH MEMBER NAME
def filled_member_force_array():
    all_member_force = member_force_array()
    for rows in range(all_member_force.shape[0]):
        if all_member_force[rows:rows + 1, 0:1] == " " and all_member_force[rows:rows + 1, 1:2] == " ":
            all_member_force[rows, 0] = all_member_force[rows - 1, 0]
            all_member_force[rows, 1] = all_member_force[rows - 1, 1]
        elif all_member_force[rows:rows + 1, 0:1] == " ":
            all_member_force[rows, 0] = all_member_force[rows - 1, 0]
        else:
            all_member_force = all_member_force
    return np.delete(all_member_force, 0, axis=0)


# GENERATE A LIST OF BEAM NAMES IN ARRAY TO USE AS DICTIONARY KEYS BASED ON USER INPUT
def get_beam_names():
    beam_array = member_force_array()[:, [0]]
    beam = [np.array(b).tolist() for b in beam_array if not b == ' ']
    beam = [b for sub_b in beam for b in sub_b]
    if beam_option == 1:
        beam = beam
    elif beam_option == 2:
        starts_with = 'B40102'
        beam = [b for b in beam if b.startswith(starts_with)]
    elif beam_option == 3:
        beam = ['B4010011']
    else:
        print('no option selected')
    return beam


# GENERATE A LIST OF LOAD COMBINATION NAMES IN ARRAY TO USE AS DICTIONARY KEYS BASED ON USER INPUT
def get_load_names():
    load_array = member_force_array()[:, [1]]
    load = [np.array(l).tolist() for l in load_array if not l == ' ']
    load = [l for sub_l in load for l in sub_l][0:lc_count]
    if load_option == 1:
        load = load
    elif load_option == 2:
        starts_with = '4D+L-'
        load = [l for l in load if l.startswith(starts_with)]
    elif load_option == 3:
        load = ['4D+L-SSE']
    else:
        print('no option selected')
    return load


# allows me to search for any key in a tuple
class TupleDict(dict):
    def __contains__(self, key):
        if super(TupleDict, self).__contains__(key):
            return True
        return any(key in k for k in self)


# SEARCH THROUGH DICTIONARY TO FIND KEYS THAT MATCH BEAM, LOAD, AND JOINT CRITERIA
def requested_member_force_array():
    member_force_array_list = filled_member_force_array()
    key = member_force_array_list[0:, [0, 1, 2]]
    beam_names = member_force_array_list[0:, [0]].tolist()
    joint_names = member_force_array_list[0:, [2]]
    value = member_force_array_list[0:, [3, 4, 5, 6, 7, 8]].tolist()
    d = {}
    d_joints = {}
    for row in range(len(key)):
        d[(tuple(key[row]))] = value[row]
        if ''.join(beam_names[row]) in d_joints:
            pass
        else:
            d_joints[''.join(beam_names[row])] = [joint_names[row][0], joint_names[row + 1][0]]
    d = TupleDict(d)
    output_keys = []*3
    output_values = []*6
    user_beams = get_beam_names()
    user_loads = get_load_names()
    for beams in user_beams:
        if beams in d and joint == 'ALL':
            for loads in user_loads:
                if g_mem.truss_member:
                    output_keys.append([beams, loads, d_joints[beams][0]])
                    output_values.append(d[(beams, loads, d_joints[beams][0])])
                else:
                    i = 0
                    while i < 2:
                        output_keys.append([beams, loads, d_joints[beams][i]])
                        output_values.append(d[(beams, loads, d_joints[beams][i])])
                        i += 1
        elif beams in d and joint == 'START':
            for loads in user_loads:
                output_keys.append([beams, loads, d_joints[beams][0]])
                output_values.append(d[(beams, loads, d_joints[beams][0])])
        elif beams in d and joint == 'END':
            for loads in user_loads:
                output_keys.append([beams, loads, d_joints[beams][1]])
                output_values.append(d[(beams, loads, d_joints[beams][1])])
    output_array = np.hstack((np.array(output_keys), np.array(output_values)))
    return output_array

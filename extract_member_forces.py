import generate_clean_file
import numpy as np


def get_phrase_line(phrase_start, phrase_end):
    with open(generate_clean_file.output_file, 'r') as file:
        for number, all_line in enumerate(file):
            if phrase_start in all_line:
                line_start = number
            if phrase_end in all_line:
                line_end = number
    return [line_start, line_end]


def member_force_array(phrase_start, phrase_end):
    force_sta_end_line = get_phrase_line(phrase_start, phrase_end)
    clean_file = generate_clean_file.store_file_list()
    member_forces = clean_file[force_sta_end_line[0] + 10: force_sta_end_line[1]]
    print(*member_forces, sep='\n')
    all_member_force = ['Member', 'Load Combination', 'Joint', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']
    for all_rows in range(len(member_forces)):
        test_line = np.array("".join(member_forces[all_rows]).split())
        if len(test_line) < 9:
            test_line = np.insert(test_line, 0, " ")
            if len(test_line) < 9:
                test_line = np.insert(test_line, 0, " ")
        else:
            test_line = test_line
        all_member_force = np.vstack((all_member_force, test_line))
    return all_member_force


def member_force_final():
    load_combinations = 5
    member_forces = member_force_array('FORCE START', 'FORCE END')
    count_members = np.count_nonzero(member_forces[:, 0]) - 1
    print(count_members)
    for i in range((load_combinations*2)*count_members+1):
        if member_forces[i:i+1, 0:1] == " " and member_forces[i:i+1, 1:2] == " ":
            member_forces[i, 0] = member_forces[i-1, 0]
            member_forces[i, 1] = member_forces[i - 1, 1]
        elif member_forces[i:i+1, 0:1] == " ":
            member_forces[i, 0] = member_forces[i - 1, 0]
        else:
            member_forces = member_forces
    i = i + 1
    return member_forces

# READS .GTO FILE AND DETERMINES NUMBER OF OCCURRENCES OF 'LIST FORCES' AND RETURNS A LIST OF ELEMENTS IN THE USER
# SPECIFIED LIST FORCES SET. ALSO CALCULATED NUMBER OF MEMBERS AND NUMBER OF LOAD COMBINATIONS IN THE SET

input_file = 'RB Steel Framing_v34.gto'
member_set = 0      # based on input from user
increment = 0
blanks = 0
next_line = 0
trigger_string = 'LIST FOR'


with open(input_file, 'r') as f:
    file_list = []
    for lines in f:
        file_list.append(lines.rstrip())


result = [v for v in file_list if trigger_string in v]
index_list = [file_list.index(result[i]) for i in range(len(result))]
first_useful_line = index_list[member_set] + 24

for i in range(len(file_list)):
    if not file_list[first_useful_line + next_line].startswith('1'):
        next_line += 1
    else:
        end_index = first_useful_line + next_line
        break

blanks = file_list[first_useful_line:end_index].count("")
mem_num = blanks + 1
member_forces = list(filter(None, file_list[first_useful_line:end_index]))


def load_comb_count():
    if not any('MOMENT' in st for st in file_list[index_list[member_set]:first_useful_line - 2]):
        lc_count = int((end_index - first_useful_line - blanks) / mem_num)
        truss_member = True
    else:
        lc_count = int((end_index - first_useful_line - blanks) / (mem_num*2))
    return lc_count

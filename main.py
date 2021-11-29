# MAIN PROGRAM
# SAVES OUTPUT TEXT FILE AS FORMATTED TABLE AND PRINTS FILE NAME, SIZE, NUMBER OF LOAD COMBINATIONS, AND NUMBER OF BEAMS
# FOR A SINGLE OCCURRENCE OF 'LIST FORCES'
import extract_member_forces as emf
from tabulate import tabulate
import generate_mem_array_info as g_mem

member_forces = emf.requested_member_force_array()
output_file_name = 'member_forces.txt'

with open(output_file_name, 'w') as w:
    table_output = tabulate(member_forces, colalign=('left', 'center'))
    w.write(table_output)
    print(f'{output_file_name} saved successfully')
    print(f'file size = {member_forces.nbytes / 1000} KB')
    print(f'Number of Load Combinations = {g_mem.load_comb_count()}')
    print(f'Number of Members = {g_mem.mem_num}')
    print(f'number of rows = {g_mem.end_index - g_mem.first_useful_line}')




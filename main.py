#!/usr/bin/env python3
import extract_member_forces as emf
from tabulate import tabulate
import generate_mem_array_info as g_mem
import argparse

# beam_option = 1
# load_option = 1
# joint = 'ALL'
# input_file = 'RB_Steel_Framing_v34.gto'
# output_file_name = 'member_forces.txt'


def run_program(output_file_name, input_file, beam_option, load_option, joint):
    with open(input_file, 'r') as f:
        file_list = []
        for lines in f:
            file_list.append(lines.rstrip())
        member_forces = emf.requested_member_force_array(joint, beam_option, load_option, file_list)
        ph_1, load_comb_count, ph_2, mem_num, end_index, first_useful_line = g_mem.get_member_force_list_info(file_list)
        with open(output_file_name, 'w') as w:
            table_output = tabulate([list(k) + v for k, v in member_forces.items()], colalign=('left', 'center'))
            w.write(table_output)
        print(f'{output_file_name} saved successfully')
        print(f'Number of Load Combinations = {load_comb_count}')
        print(f'Number of Members = {mem_num}')
        print(f'number of rows = {end_index - first_useful_line}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
    **************
    * DESRIPTION *
    **************

    Pull out the needed information from a gto file. This program will return a txt file with the needed information.

    Examples of how to run as a CLI:
    ================================
    python3 main.py --help
    python3 main.py -out member_forces.txt -in /users/jesse/RB_Steel_Framing_v34.gto -b 1 -l 1 -j ALL
    """,
                                     epilog="",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-o", '--output_file_name', type=str, default='member_forces.txt',
                        help="The filename of the desired output file (default = %(default)s)")
    parser.add_argument("-i", "--input_file", type=str, required=True,
                        help="The absolute path and filename of the input file (default = %(default)s)")
    parser.add_argument("-b", "--beam_option", type=int, default=1,
                        help="required beams (default = %(default)s)")
    parser.add_argument("-l", "--load_option", type=int, default=1,
                        help="required loads (default = %(default)s)")
    parser.add_argument("-j", "--joint", type=str, default='ALL', choices=['ALL', 'START', 'END'],
                        help="required joints (ALL, START, END) (default = %(default)s)")
    args = parser.parse_args()
    run_program(**vars(args))


















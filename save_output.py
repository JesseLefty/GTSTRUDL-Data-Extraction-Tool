import extract_member_forces as emf
import generate_mem_array_info as g_mem
import csv
import openpyxl


def run_program(output_file_name, joint, member_set, out_format, input_file, file_as_list, beam_id, load_id):
    """
        Runs the full program. Saves all required outputs as selected by the user and saves either an xlsx file or a
        csv file.

            Parameters:

            Returns:
                 .xlsx or .csv file of requested user inputs
        """
    with open(output_file_name, 'w', newline='') as w:
        if out_format:
            wb = openpyxl.Workbook()
            for item in range(len(member_set)):
                member_forces, load_comb_count, truss_member, mem_num, end_index, first_useful_line = \
                    g_mem.ParseFileForData(item, input_file, member_set).get_member_force_list_info(file_as_list)
                sheet_name = 'Load Set ' + str(item)
                member_forces = emf.GenerateOutputArray(joint, item).requested_member_force_array(member_forces,
                                                                                                  load_comb_count,
                                                                                                  truss_member, beam_id,
                                                                                                  load_id)
                sheet = wb.create_sheet(f'{sheet_name}')
                d_list = [list(k) + v for k, v in member_forces.items()]
                for row, key in enumerate(member_forces.items(), start=1):
                    sheet[f"A{row}"] = (' '.join(d_list[row - 1])).replace(' ', ',')
            del wb['Sheet']
            wb.save(f'{output_file_name}.xlsx')
        else:
            with open(output_file_name + '.csv', 'w', newline='') as w:
                for item in range(len(member_set)):
                    member_forces, load_comb_count, truss_member, mem_num, end_index, first_useful_line = \
                        g_mem.ParseFileForData(item, input_file, member_set).get_member_force_list_info(file_as_list)
                    member_forces = emf.GenerateOutputArray(joint, item).requested_member_force_array(member_forces,
                                                                                                      load_comb_count,
                                                                                                      truss_member,
                                                                                                      beam_id, load_id)
                    with open(output_file_name + '.csv', 'a', newline='') as a:
                        csv.writer(a).writerows((list(k) + v for k, v in member_forces.items()))
                    # print(f'{output_file_name} saved successfully')
                    # print(f'Number of Load Combinations = {load_comb_count}')
                    # print(f'Number of Members = {mem_num}')
                    # print(f'number of rows = {end_index - first_useful_line}')

import error_handling
import extract_member_forces as emf
import generate_mem_array_info as g_mem
import csv
import openpyxl
from tkinter import *
from tkinter.ttk import *


class RunProgram:

    def __init__(self, initial_window=True):
        self.initial_window = initial_window

    member_set_errors = []
    list_errors = []
    beam_errors = []
    load_errors = []

    def run_program(self, output_file_name, joint, member_set, out_format, input_file, beam_id, load_id):
        """
            Runs the full program. Saves all required outputs as selected by the user and saves either an xlsx file or a
            csv file.

                Parameters:
                    output_file_name (str):     name of file in which to save the data
                    joint (tuple):              list containing "ALL", "STA", or "END" for joint specification
                    member_set (list):          list of values corresponding to the index of requested member set
                    out_format (str):           .csv or .xlsx
                    input_file (str):           input file in which to sear for data
                    beam_id (list):             list containing tuples of beam spec (int), and user beam input (str)
                    load_id (list):             list containing tuples of load spec (int), and user load input (str)

                Returns:
                     .xlsx or .csv file of requested user inputs
            """
        self.member_set_errors.clear()
        self.list_errors.clear()
        self.beam_errors.clear()
        self.load_errors.clear()
        if out_format == '.xlsx':
            wb = openpyxl.Workbook()
            for items in range(len(member_set)):
                member_forces, end_index, first_useful_line \
                    = g_mem.ParseFileForData(items, input_file, member_set).get_member_force_list_info()
                member_forces, errors = emf.GenerateOutputArray(joint, items, member_forces,
                                                        beam_id, load_id).requested_member_force_array()
                sheet_name = 'Load Set ' + str(items + 1)
                sheet = wb.create_sheet(f'{sheet_name}')
                d_list = [list(k) + v for k, v in member_forces.items()]
                if len(member_forces) == 0:
                    self.member_set_errors.append(items + 1)

                if errors[0] or errors[1]:
                    self.list_errors.append(items + 1)
                    self.beam_errors.append(errors[0])
                    self.load_errors.append(errors[1])

                for row, key in enumerate(member_forces.items(), start=1):
                    for col, key in enumerate(d_list[row - 1], start=1):
                        sheet.cell(column=col, row=row, value=d_list[row-1][col-1])
            del wb['Sheet']
            wb.save(output_file_name)
        else:
            with open(output_file_name, 'w', newline=''):
                for items in range(len(member_set)):
                    member_forces, end_index, first_useful_line = \
                        g_mem.ParseFileForData(items, input_file, member_set).get_member_force_list_info()
                    member_forces, errors = emf.GenerateOutputArray(joint, items, member_forces,
                                                            beam_id, load_id).requested_member_force_array()

                    with open(output_file_name, 'a', newline='') as a:
                        csv.writer(a).writerows((list(k) + v for k, v in member_forces.items()))

                    if len(member_forces) == 0:
                        self.member_set_errors.append(items + 1)

                    if errors[0] or errors[1]:
                        self.list_errors.append(items + 1)
                        self.beam_errors.append(errors[0])
                        self.load_errors.append(errors[1])

        if len(self.member_set_errors) or len(self.list_errors) > 0:
            error_set_list = list(set(self.list_errors + self.member_set_errors))
            error_handling.ErrorHandling(self.initial_window).item_not_found(error_set_list, self.beam_errors,
                                                                             self.load_errors)
        else:
            success_window = Toplevel(self.initial_window)
            success_window.geometry('200x120')
            success_window.title('Complete')
            success_window.resizable(False, False)
            success_window.grab_set()
            self.initial_window.eval(f'tk::PlaceWindow {str(success_window)} center')
            Label(success_window, text='Output Saved Successfully').pack()
            Button(success_window, text='OK', command=success_window.destroy).pack()


import config
import error_handling
import extract_member_forces as emf
from parse_file_for_input_data import ParseFileForData
import extract_joint_reactions as ejr
import extract_code_check as ecc
import csv
import openpyxl
from tkinter import *
from tkinter.ttk import *


class RunProgram:

    def __init__(self, tab_name, output_format, output_file_name, result_set_index, initial_window=None):
        self.initial_window = initial_window
        self.output_format = output_format
        self.tab_name = tab_name
        self.output_file_name = output_file_name
        self.result_set_index = result_set_index
        self.result_set_errors = []
        self.list_errors = []
        self.beam_errors = []
        self.load_errors = []
        self.joint_errors = []
        self.name_errors = []
        self.profile_errors = []
        self.ir_errors = []
        if self.output_format == '.xlsx':
            self.generate_xlsx()
        else:
            self.generate_csv()

    def build_output(self, items):
        extracted_result_list, _, _ = ParseFileForData(items, self.tab_name).get_result_list_info()
        if self.tab_name == 'Member Force':
            parsed_results, errors = emf.GenerateOutputArray(self.tab_name, items, extracted_result_list,
                                                             ).requested_member_force_array()
            if errors[0] or errors[1]:
                self.list_errors.append(items + 1)
                self.beam_errors.append(errors[0])
                self.load_errors.append(errors[1])
        elif self.tab_name == 'Joint Reaction':
            parsed_results, errors = ejr.GenerateOutputArray(self.tab_name, items,
                                                             extracted_result_list).requested_joint_reaction_dict()
            if errors[0] or errors[1]:
                self.list_errors.append(items + 1)
                self.joint_errors.append(errors[0])
                self.load_errors.append(errors[1])
        else:
            parsed_results, errors = ecc.GenerateOutputArray(self.tab_name, items,
                                                             extracted_result_list).output_list()
            if errors[0] or errors[1] or errors[2]:
                self.list_errors.append(items + 1)
                self.name_errors.append(errors[0])
                self.profile_errors.append(errors[1])
                self.ir_errors.append(errors[2])
        if len(parsed_results) == 0:
            self.result_set_errors.append(items + 1)
        return parsed_results

    def generate_xlsx(self):
        wb = openpyxl.Workbook()
        for items in range(len(self.result_set_index)):
            parsed_results = self.build_output(items)
            sheet_name = 'Result Set ' + str(items + 1)
            sheet = wb.create_sheet(f'{sheet_name}')
            for col, val in enumerate(config.result_configuration_parameters[self.tab_name]['Headings'], start=1):
                sheet.cell(column=col, row=1, value=val)
            if self.tab_name == 'Code Check':
                for row, key in enumerate(parsed_results, start=2):
                    for col, key in enumerate(parsed_results[row - 2], start=1):
                        sheet.cell(column=col, row=row, value=parsed_results[row - 2][col - 1])
            else:
                d_list = [list(k) + v for k, v in parsed_results.items()]
                for row, key in enumerate(parsed_results.items(), start=2):
                    for col, key in enumerate(d_list[row - 2], start=1):
                        sheet.cell(column=col, row=row, value=d_list[row - 2][col - 1])
        del wb['Sheet']
        wb.save(self.output_file_name)
        self.display_success_or_error()

    def generate_csv(self):
        with open(self.output_file_name, 'w', newline='') as w:
            csv.writer(w).writerow(config.result_configuration_parameters[self.tab_name]['Headings'])
            w.close()
            for items in range(len(self.result_set_index)):
                parsed_results = self.build_output(items)
                print(parsed_results)
                with open(self.output_file_name, 'a', newline='') as a:
                    if self.tab_name == 'Code Check':
                        csv.writer(a).writerows(parsed_results)
                    else:
                        csv.writer(a).writerows((list(k) + v for k, v in parsed_results.items()))
        self.display_success_or_error()

    def display_success_or_error(self):
        if len(self.result_set_errors) or len(self.list_errors) > 0:
            error_set_list = list(set(self.list_errors + self.result_set_errors))
            if self.tab_name == 'Member Force':
                error_handling.ErrorHandling(self.initial_window).item_not_found(error_set_list, self.beam_errors,
                                                                                 self.load_errors, member_force=True)
            elif self.tab_name == 'Joint Reaction':
                error_handling.ErrorHandling(self.initial_window).item_not_found(error_set_list, self.joint_errors,
                                                                                 self.load_errors, joint_reaction=True)
            else:
                error_handling.ErrorHandling(self.initial_window).item_not_found(error_set_list, self.name_errors,
                                                                                 self.profile_errors,
                                                                                 ir_errors=self.ir_errors,
                                                                                 code_check=True)
        else:
            success_window = Toplevel(self.initial_window)
            success_window.geometry('200x60')
            success_window.title('Complete')
            success_window.resizable(False, False)
            success_window.grab_set()
            self.initial_window.eval(f'tk::PlaceWindow {str(success_window)} center')
            Label(success_window, text='Output Saved Successfully').pack()
            Button(success_window, text='OK', command=success_window.destroy).pack()


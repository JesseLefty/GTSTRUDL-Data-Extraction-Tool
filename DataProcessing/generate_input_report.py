"""
This module generates an input file in the form of a .txt file that contains a detailed breakdown of the user
requested results parameters.

"""
import os.path
import datetime
from Tools import shared_stuff
from Tools.result_printing_tools import ProcessResultsPrinting, convert_bool_to_yes_no

MAX_CHAR = 80
SEP_LINE = f'*' * MAX_CHAR


class GenerateInputReport:

    def __init__(self, tab_name):
        self.tab_name = tab_name
        self.results_parameters = shared_stuff.data_store
        self.results_parameters.tab_name = tab_name
        self.input_report_name = f'{self.results_parameters.directory}/{self.tab_name}-INPUT REPORT.txt'
        self.num_sets = len(self.results_parameters.results_parameters['Set Name'])
        self.report_info = ProcessResultsPrinting(self.tab_name)

    def generate_header(self) -> list[str]:
        """
        builds input report header

        :return: list of header rows
        """
        line1 = f'{" "* 23}Data Extraction Tool Input Report'
        line2 = f'Input Report "{os.path.basename(self.input_report_name)}" Generated {datetime.datetime.today()}'
        line3 = f'This input report was generated using the results of output file ' \
                f'{os.path.basename(self.results_parameters.input_file)}'
        return [SEP_LINE, line1, line2, line3, SEP_LINE]

    def format_result_parameter(self) -> list[list[str]]:
        """
        generats a list of formatted result parameters that are more human readable

        :return: nested list of strings corresponding to input report rows
        """
        input_result_parameters = []
        formatted_input_result_parameters = []
        set_name = []
        load_spec = []
        name_spec = []
        joint_spec = []
        profile_spec = []
        sort_spec = []
        sort_criteria_print = []
        ir_range = []

        for items in range(self.num_sets):
            name_option, name_choices = self.report_info.get_name_spec(items)
            set_name.append(f'GTSTRUDL Input Command: {self.report_info.get_set_name(items)}')
            name_spec.append(f'Name Criteria: {" "* (24-16)} {name_option} {name_choices}')
            if self.tab_name == 'Member Force':
                load_option, load_choices = self.report_info.get_load_spec(items)
                joint_spec.append(f'Joint Criteria: {" "* (24-17)} {self.report_info.get_joint_sepc(items)}')
                load_spec.append(f'Load Case Criteria: {" "* (24-21)} {load_option} {load_choices}')
                input_result_parameters = [set_name, load_spec, name_spec, joint_spec]
            elif self.tab_name == 'Joint Reaction':
                load_option, load_choices = self.report_info.get_load_spec(items)
                load_spec.append(f'Load Case Criteria: {" "* (24-21)} {load_option} {load_choices}')
                input_result_parameters = [set_name, load_spec, name_spec]
            else:
                ir_val = self.report_info.get_ir_spec(items)
                profile_option, profile_choices = self.report_info.get_profile_spec(items)
                sort_criteria = self.report_info.get_sort_criteria(items)
                sort_direction = self.report_info.get_sort_direction(items)
                profile_spec.append(f'Profile Criteria: {" "* (24-19)} {profile_option} {profile_choices}')
                sort_spec.append(f'Sort Select: {" "* (24-14)} {convert_bool_to_yes_no(self.results_parameters.sort[items])}')
                ir_range.append(f'IR Range Criteria: {" "* (24-20)} {ir_val}')
                sort_criteria_print.append(f'Sort Criteria Selection: {list(zip(sort_criteria, sort_direction))}')
                input_result_parameters = [set_name, name_spec, profile_spec, ir_range, sort_spec, sort_criteria_print]
        flattened_input_parameters = [item for items in input_result_parameters for item in items]

        for set in range(self.num_sets):
            formatted_input_result_parameters.append([SEP_LINE])
            formatted_input_result_parameters.append([f'{" "* 27} Result Set # {set + 1}'])
            formatted_input_result_parameters.append(flattened_input_parameters[set::self.num_sets])
            formatted_input_result_parameters.append([SEP_LINE])
        return formatted_input_result_parameters

    def print_input_file(self, output_file_path):
        """
        combines the header and formatted input results into a single list and prints the list to a text file

        :param output_file_path: working directory and output file base name
        """
        header = self.generate_header()
        formatted_input = self.format_result_parameter()
        final_output = header
        for result in formatted_input:
            for line in result:
                final_output.append(line)
        with open(self.input_report_name, 'w') as file:
            file.writelines('\n'.join(final_output))
            file.write('\n')
            file.write(f'This input report corresponds to processed results in {os.path.basename(output_file_path)}')


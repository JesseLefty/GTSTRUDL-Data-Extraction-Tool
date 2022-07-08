import os.path
import datetime
from Tools import shared_stuff

MAX_CHAR = 80
SEP_LINE = f'*' * MAX_CHAR
"""
This module generates an input file in the form of a .txt file that contains a detailed breakdown of the user
requested results parameters.

"""


class GenerateInputReport:

    def __init__(self, tab_name):
        self.tab_name = tab_name
        self.results_parameters = shared_stuff.data_store
        self.results_parameters.tab_name = tab_name
        self.input_report_name = f'{self.results_parameters.directory}/{self.tab_name}-INPUT REPORT.txt'
        print(self.input_report_name)

    def generate_header(self) -> list[str]:
        line1 = f'Data Extraction Tool Input Report'
        line2 = f'Input Report "{os.path.basename(self.input_report_name)}" Generated {datetime.date.today()}'
        line3 = f'This input report was generated using the results of output file {os.path.basename(self.results_parameters.input_file)}'
        return [SEP_LINE, line1, line2, line3, SEP_LINE]

    def format_result_parameter(self) -> list[list[str]]:
        input_result_parameters = []
        num_sets = len(self.results_parameters.results_parameters['Set Name'])
        formatted_input_result_parameters = []
        for k, v in self.results_parameters.results_parameters.items():
            for item in v:
                input_result_parameters.append([f'{k}: {item}'])
        for set in range(num_sets):
            formatted_input_result_parameters.append([[SEP_LINE]])
            formatted_input_result_parameters.append(input_result_parameters[set::num_sets])
            formatted_input_result_parameters.append([[SEP_LINE]])
        return [item for items in formatted_input_result_parameters for item in items]

    def print_input_file(self, output_file_path):
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


import numpy as np


class ReadInputFile:

    def __init__(self, input_file):
        self.input_file = input_file

    def file_list(self):
        with open(self.input_file, 'r') as f:
            file_as_list = []
            for lines in f:
                file_as_list.append(lines.rstrip())
        return file_as_list


class GenerateDisplayData:

    def __init__(self, input_file):
        self.input_file = input_file
        pass

    def get_force_display(self):
        file_list = ReadInputFile(self.input_file).file_list()
        trigger_string = 'LIST FOR'
        result = [v for v in file_list if trigger_string in v]
        result = [v[v.find(trigger_string):] for v in result]
        return result, file_list

    def get_reactions_display(self):
        pass

    def get_IRs_display(self):
        pass

    def get_section_cuts_display(self):
        pass


class ParseFileForData:

    def __init__(self, num_mem_set, input_file, member_set):
        self.num_mem_set = num_mem_set
        self.input_file = input_file
        self.member_set = member_set
        pass

    def get_force_positions(self):
        """
        Searches the input file for trigger. Returns a list of lines in input file which contain the strings
        and a list of the index (line number) for each of the lines containing the trigger.
                Parameters:
                    self

                Returns:
                    index_list (int): the index position of the specific member set being requested
                    result list(str): list of GTSTRUDL input lines for 'LIST FOR'

                Triggers:
                    'LIST FOR': Obtains line which lists member forces
                    'OTHER TRIGGERS': Reserved for future triggers / expansion (i.e, displacements, reactions, etc.)
        """
        file_list = ReadInputFile(self.input_file).file_list()
        trigger_string = 'LIST FOR'
        result = [v for v in file_list if trigger_string in v]
        index_list = [file_list.index(result[i]) for i in range(len(result))]
        result = [v[v.find(trigger_string):] for v in result]
        return index_list[self.member_set[self.num_mem_set]], result

    def get_member_force_list_info(self, file_list):
        """
        Determines the index (line number) of first useful line and last useful line of the input file which contains
        the block of requested data. Uses the size of the block to calculate the number of blank lines
        (spaces between subsets of data), the number of members in the requested data set, whether the data set contains
        truss type members (or any members that do not have moments), and the number of load combinations for each
        subset of the data.

            Parameters:
                self
                file_list

            Returns:
                 member_results (array):    a 1d array of the member results
                 lc_count (int):            the number of load combinations
                 truss_member (bool):      truss member type (True or False)
                 mem_num (int):             the number of members in the data block
                 first_useful_line (int):   index of start of requested data block
                 end_index (int):           index of end of requested data block
        """
        index_for_mem_set, ph_1 = self.get_force_positions()
        first_useful_line = index_for_mem_set + 24
        end_index = 0
        next_line = 0
        for i, line in enumerate(file_list):
            if not file_list[first_useful_line + next_line].startswith('1'):
                next_line += 1
            else:
                end_index = first_useful_line + next_line
                break
        blanks = file_list[first_useful_line:end_index].count("")
        mem_num = blanks + 1
        member_forces = list(filter(None, file_list[first_useful_line:end_index]))
        truss_member = False
        if not any('MOMENT' in st for st in file_list[index_for_mem_set:first_useful_line - 2]):
            lc_count = int((end_index - first_useful_line - blanks) / mem_num)
            truss_member = True
        else:
            lc_count = int((end_index - first_useful_line - blanks) / (mem_num * 2))
        return np.array(member_forces), lc_count, truss_member, mem_num, end_index, first_useful_line

"""
This module generates a default list of code check result from the .gto file, parses the default list based on
user input requirements, and provides a final list containing only the subset of items matching the user requirements.
This module works for one code check result at a time.
"""
from operator import itemgetter
from natsort import natsorted
from Tools import shared_stuff
from Tools.config import codes


class GenerateOutputArray:
    """
    Formats the code check list and compiles a list of results which meet the user requirements.

    :param  tab_name (str):         name of active tab
    :param  code_set_index (int):   index of the user generated result set for which the data is requested
    :param  code_check (list):      flattened list of all lines in requested data block
    """

    def __init__(self, tab_name, code_set_index, code_check):
        self.results = shared_stuff.data_store
        self.results.tab_name = tab_name
        self.code_set_index = code_set_index
        self.name_id = self.results.name[self.code_set_index]
        self.profile_id = self.results.profile[self.code_set_index]
        self.ir_range = self.results.ir_range[self.code_set_index]
        self.fail_id = self.results.fail[self.code_set_index]
        for index, line in enumerate(code_check):
            if '/---------/' in line:
                self.code_check = code_check[index:]
                break
            else:
                self.code_check = code_check

    def code_check_array(self):
        """
        Generates a formatted list of code check results with all elements in list.

        :return     nested list with each inner list having 10 items corresponding to the code check results
        """
        col_idx = []
        code_check_list = []
        header_line = self.code_check[0]
        code_check = self.code_check[1:]
        for idx, char in enumerate(header_line):
            if char == '/':
                col_idx.append(idx)
        for line in code_check:
            column_1 = line[0: col_idx[1]].strip()
            column_2 = line[col_idx[1]: col_idx[2] + 1].strip()
            column_3 = line[col_idx[2]: col_idx[3] + 1].strip()
            column_4 = line[col_idx[3]: col_idx[4] + 1].strip()
            column_5 = line[col_idx[4]: col_idx[5] + 1].strip()
            column_6 = line[col_idx[5]: col_idx[6] + 1].strip()
            column_7 = line[col_idx[6]: col_idx[7] + 1].strip()
            column_8 = line[col_idx[7]: col_idx[8] + 1].strip()
            column_9 = line[col_idx[8]: col_idx[9] + 1].strip()
            column_10 = line[col_idx[9]:].strip()
            if column_1 and not (column_1.startswith("****")):
                code_check_list.append([column_1] + [column_2] + [column_3] + [column_4] + [column_5] + [column_6] +
                                       [column_7] + [column_8] + [column_9] + [column_10])
        code_check_list.pop()
        code_check_list = [x + y for x, y in zip(code_check_list[0::2], code_check_list[1::2])]
        return code_check_list

    def parse_names(self, code_check_list):
        """
        Parses the code check list for names which match the user requested names

        :param code_check_list: nested list with each inner list having 10 items corresponding to the code
                                         check results
        :return: list of names in code_check_list which meet the user criteria
        """
        user_names = []
        name = []
        for row in code_check_list:
            name.append(row[0])
        if self.name_id[0] == 2:
            name_starts_with = self.name_id[1]
            user_names = [n for n in name if n.startswith(name_starts_with)]
        elif self.name_id[0] == 3:
            name_ends_with = self.name_id[1]
            user_names = [n for n in name if n.endswith(name_ends_with)]
        elif self.name_id[0] == 4:
            name_contains = self.name_id[1]
            user_names = [n for n in name if name_contains in n]
        elif self.name_id[0] == 5:
            name_list = self.name_id[1].upper()
            name_list = "".join(name_list).replace(" ", "").split(',')
            for names in name_list:
                if names in name:
                    user_names.append(names)
                else:
                    pass
        else:
            user_names = name
        user_names = list(set(user_names))
        return user_names

    def parse_profile(self, code_check_list):
        """
        Parses the code check list for profiles which match the user requested profiles

        :param code_check_list: nested list with each inner list having 10 items corresponding to the code
                                         check results
        :return: list of profiles in code_check_list which meet the user criteria
        """
        user_profiles = []
        profile = []
        for row in code_check_list:
            profile.append(row[11])
        if self.profile_id[0] == 2:
            profile_starts_with = self.profile_id[1]
            user_profiles = [p for p in profile if p.startswith(profile_starts_with)]
        elif self.profile_id[0] == 3:
            profile_ends_with = self.profile_id[1]
            user_profiles = [p for p in profile if p.endswith(profile_ends_with)]
        elif self.profile_id[0] == 4:
            profile_contains = self.profile_id[1]
            user_profiles = [p for p in profile if profile_contains in p]
        elif self.profile_id[0] == 5:
            profile_list = self.profile_id[1].upper()
            profile_list = "".join(profile_list).replace(" ", "").split(',')
            for profiles in profile_list:
                if profiles in profile:
                    user_profiles.append(profiles)
                else:
                    pass
        else:
            user_profiles = profile
        user_profiles = list(set(user_profiles))
        return user_profiles

    def parse_ir_range(self, code_check_list):
        """
        Parses the code check list for IR results which match the user requested IR criteria

        :param code_check_list: nested list with each inner list having 10 items corresponding to the code check results
        :return: list of IRs in code_check_list which meet the user criteria
        """
        ir = []
        for row in code_check_list:
            ir.append(row[5])
        if self.ir_range[0] == 2:
            ir_less_than = float(self.ir_range[1][1])
            user_ir = [p for p in ir if float(p) < ir_less_than]
        elif self.ir_range[0] == 3:
            ir_greater_than = float(self.ir_range[1][0])
            user_ir = [p for p in ir if float(p) > ir_greater_than]
        elif self.ir_range[0] == 4:
            lower_ir = float(self.ir_range[1][0])
            upper_ir = float(self.ir_range[1][1])
            user_ir = [p for p in ir if lower_ir < float(p) < upper_ir]
        else:
            user_ir = ir
        user_ir = list(set(user_ir))
        return user_ir

    def build_parsed_list(self):
        """
        Builds a nested list of code check results for all rows wich match the user name, profile, and IR criteria
        :return: nested list of code check results which meet the user name, profile, and IR criteria
        """
        code_check_list = self.code_check_array()
        code_dict = {}
        fail_parse = {}
        name_parse = {}
        profile_parse = {}
        parsed_dict = {}
        for row in code_check_list:
            code_dict[row[0]] = row[1:]
        if not self.fail_id and self.name_id[0] == 1 and self.profile_id[0] == 1 and self.ir_range[0] == 1:
            parsed_dict = code_dict
        else:
            user_names = self.parse_names(code_check_list)
            user_profiles = self.parse_profile(code_check_list)
            user_ir = self.parse_ir_range(code_check_list)
            if self.fail_id:
                for key, values in code_dict.items():
                    if 'FAILED' in values[18]:
                        fail_parse[key] = code_dict[key]
                    else:
                        pass
            else:
                fail_parse = code_dict
            if len(fail_parse) == 0:
                parsed_dict = {}
            else:
                for names in fail_parse.keys():
                    if names in user_names:
                        name_parse[names] = fail_parse[names]
                for key, values in name_parse.items():
                    if values[10] in user_profiles:
                        profile_parse[key] = name_parse[key]
                for key, values in profile_parse.items():
                    if values[4] in user_ir:
                        parsed_dict[key] = profile_parse[key]
        if len(parsed_dict) == 0:
            print("No matching results")
        parsed_list = [[k] + v for k, v in parsed_dict.items()]
        for row in parsed_list:
            del row[12:14]
        parsed_list = list(zip(*parsed_list))
        col_new = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 6, 7, 8, 14, 15, 16, 9, 17]
        col_map = dict(enumerate(col_new))
        parsed_list = [parsed_list[col_map[i]] for i in range(len(parsed_list))]
        parsed_list = list(zip(*parsed_list))
        return parsed_list

    def sorted_list(self, sort_order, reverse):
        """
        Sorts parsed list if the user requests the data to be sorted

        :param sort_order: tuple of True/False and column index of item to be sorted
        :param reverse: True/False for whether the data should be sorted ascending or descending
        :return: sorted list matching the user criteria
        """
        parsed_list = self.build_parsed_list()
        reverse_idx = len(reverse[self.code_set_index]) - 1
        sorted_list = parsed_list
        for key, flag in reversed(sort_order[self.code_set_index]):
            if flag:
                sorted_list = natsorted(sorted_list, key=itemgetter(key),
                                        reverse=reverse[self.code_set_index][reverse_idx])
            else:
                pass
            reverse_idx -= 1
        return sorted_list

    def output_list(self):
        """
        Function with compiles the final list matching all user input criteria

        :return: list of items matching user input criteria
        """
        sort_request = self.results.sort
        sort_order = self.results.sort_order
        reverse = self.results.reverse
        if sort_request[self.code_set_index]:
            output_list = self.sorted_list(sort_order, reverse)
        else:
            output_list = self.build_parsed_list()
        return output_list

"""
This module generates a default list of code check result from the .gto file, parses the default list based on
user input requirements, and provides a final list containing only the subset of items matching the user requirements.
This module works for one code check result at a time.
"""
from operator import itemgetter
from natsort import natsorted
from Tools.available_result_tools import valid_names, UserSelectionOption
from Tools import shared_stuff


def get_items_in_col(list_of_items: list, col_num: int):
    item_list = []
    for row in list_of_items:
        item_list.append(row[col_num])
    return item_list


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
        for idx, char in enumerate(self.code_check[0]):
            if char == '/':
                col_idx.append(idx)
        for line in self.code_check[1:-1]:
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
        code_check_list = [x + y for x, y in zip(code_check_list[0::2], code_check_list[1::2])]
        return code_check_list

    def parse_ir_range(self, code_check_list):
        """
        Parses the code check list for IR results which match the user requested IR criteria

        :param code_check_list: nested list with each inner list having 10 items corresponding to the code check results
        :return: list of IRs in code_check_list which meet the user criteria
        """
        ir = get_items_in_col(code_check_list, 5)
        lower_ir = self.ir_range[1][0]
        upper_ir = self.ir_range[1][1]
        if self.ir_range[0] == UserSelectionOption.LESS_THAN:
            user_ir = [p for p in ir if float(p) < float(upper_ir)]
        elif self.ir_range[0] == UserSelectionOption.GREATER_THAN:
            user_ir = [p for p in ir if float(p) > float(lower_ir)]
        elif self.ir_range[0] == UserSelectionOption.BETWEEN:
            user_ir = [p for p in ir if float(lower_ir) < float(p) < float(upper_ir)]
        else:
            user_ir = ir
        user_ir = list(set(user_ir))
        return user_ir

    def build_parsed_list(self):
        """
        Builds a nested list of code check results for all rows which match the user name, profile, and IR criteria
        :return: nested list of code check results which meet the user name, profile, and IR criteria
        """
        code_check_list = self.code_check_array()
        code_dict = {}
        fail_parse = {}
        name_parse = {}
        profile_parse = {}
        parsed_dict = {}
        user_names = valid_names(get_items_in_col(code_check_list, 0), self.results.name, self.code_set_index)
        user_profiles = valid_names(get_items_in_col(code_check_list, 11), self.results.profile, self.code_set_index)
        user_ir = self.parse_ir_range(code_check_list)
        for row in code_check_list:
            code_dict[row[0]] = row[1:]
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
            for name in fail_parse.keys():
                if name in user_names:
                    name_parse[name] = fail_parse[name]
            for key, values in name_parse.items():
                if values[10] in user_profiles:
                    profile_parse[key] = name_parse[key]
            for key, values in profile_parse.items():
                if values[4] in user_ir:
                    parsed_dict[key] = profile_parse[key]
        if len(parsed_dict) == 0:
            print("No matching results")
        parsed_list = [[k] + v for k, v in parsed_dict.items()]
        print(parsed_list)
        for row in parsed_list:
            del row[12:14]
        parsed_list = list(zip(*parsed_list))
        col_new = [0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 6, 7, 8, 14, 15, 16, 9, 17]
        col_map = dict(enumerate(col_new))
        parsed_list = [parsed_list[col_map[i]] for i in range(len(parsed_list))]
        parsed_list = list(zip(*parsed_list))
        return parsed_list

    def sorted_list(self, list_to_sort):
        """
        Sorts parsed list if the user requests the data to be sorted

        :param list_to_sort: list of code results to sort

        :return: sorted list matching the user criteria
        """
        reverse_idx = len(self.results.reverse[self.code_set_index]) - 1
        sorted_list = list_to_sort
        for key, flag in reversed(self.results.sort_order[self.code_set_index]):
            sorted_list = natsorted(sorted_list, key=itemgetter(key),
                                    reverse=self.results.reverse[self.code_set_index][reverse_idx])
            reverse_idx -= 1
        return sorted_list

    def output_list(self):
        """
        Function with compiles the final list matching all user input criteria

        :return: list of items matching user input criteria
        """
        output_list = self.build_parsed_list()
        if self.results.sort[self.code_set_index]:
            return self.sorted_list(output_list)
        return output_list

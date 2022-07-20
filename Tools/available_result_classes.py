import re
from Tools.available_result_tools import column_contents


class OutputResult:

    def __init__(self, output_result, type = '<unknown>'):
        self.output_result = output_result
        self.type = type
        self.header = self._get_header()
        self.set_name = self._get_set_name()
        self.number_of_columns = len(self.header)

    def get_number_of_blocks(self, column_start, column_end):
        block_count = 0
        for line in self.output_result:
            column_contents = line[column_start:column_end].strip()
            if column_contents and not column_contents.startswith(('1', '****')):
                block_count += 1

        return block_count

    def _get_set_name(self):
        return 'set name'

    def _get_header(self):
        return [item for item in re.split(r'\s{2,}', self.output_result[0]) if item != ""]


class MemberForceBlock(OutputResult):
    def __init__(self, output_result, column_index):
        super().__init__(output_result)
        self.column_index = column_index
        self.member_names = column_contents(self.column_index[0], self.column_index[1], self.output_result)
        self.block_index_dictionary = self._block_dictionary()

    def _get_block_start_end(self):
        block_start_indices = []
        column_1 = []
        last_index = len(self.output_result)
        for line in self.output_result:
            column_1.append(line[self.column_index[0]: self.column_index[1]].strip())
        for item in self.member_names:
            block_start_indices.append(column_1.index(item))
        block_start_indices.append(last_index)

        return block_start_indices

    def _block_dictionary(self):
        block_name_and_indices = {}
        block_start_indices = self._get_block_start_end()
        for index, item in enumerate(self.member_names):
            block_name_and_indices[item] = (block_start_indices[index], block_start_indices[index+1])
        return block_name_and_indices

    def get_block(self, member_name):
        block_start = self.block_index_dictionary[member_name][0]
        block_end = self.block_index_dictionary[member_name][1]
        block = [item for item in self.output_result[block_start:block_end] if "****" not in item]
        return block

    def get_joint_names(self, block):
        return column_contents(self.column_index[2], self.column_index[3], block)

    def get_load_names(self, block):
        return column_contents(self.column_index[1], self.column_index[2], block)


class JointReactionBlock(OutputResult):
    def __init__(self, output_result, column_index):
        super().__init__(output_result)
        self.column_index = column_index
        self.joint_names = column_contents(self.column_index[0], self.column_index[1], self.output_result)
        self.block_index_dictionary = self._block_dictionary()

    def _get_block_start_end(self):
        block_start_indices = []
        column_1 = []
        last_index = len(self.output_result)
        for line in self.output_result:
            column_1.append(line[self.column_index[0]: self.column_index[1]].strip())
        for item in self.joint_names:
            block_start_indices.append(column_1.index(item))
        block_start_indices.append(last_index)

        return block_start_indices

    def _block_dictionary(self):
        block_name_and_indices = {}
        block_start_indices = self._get_block_start_end()
        for index, item in enumerate(self.joint_names):
            block_name_and_indices[item] = (block_start_indices[index], block_start_indices[index+1])
        return block_name_and_indices

    def get_block(self, member_name):
        block_start = self.block_index_dictionary[member_name][0]
        block_end = self.block_index_dictionary[member_name][1]
        block = [item for item in self.output_result[block_start:block_end] if "****" not in item]
        return block

    def get_joint_names(self, block):
        return column_contents(self.column_index[1], self.column_index[2], block)

    def get_load_names(self, block):
        return column_contents(self.column_index[2], self.column_index[3], block)

import utilities
import re
import shared_stuff


class GenerateOutputArray:
    """
            Formats the member force list and compiles a dictionary of requested joint, load combinations, members
            and the corresponding results.

            Parameters:
                tab_name (str):             name of tab from which the user clicked 'generate'
                mem_set_index (int):        index of the user generated result set for which the data is requested
                member_forces (list):       flattened list of all lines in requested data block
            """
    def __init__(self, tab_name, mem_set_index, member_forces):
        self.mem_set_index = mem_set_index
        self.results = shared_stuff.data_store
        self.results.tab_name = tab_name
        self.joint = self.results.joint[self.mem_set_index]
        self.member_forces = member_forces
        self.beam_id = self.results.name
        self.load_id = self.results.load

    def member_force_array(self):
        """
        Generates a formatted list of member forces with all elements in list containing beam, load, joint,
        and 6 results. Subdivides each result set into 'blocks'. The size of each block is the number of rows for a
        given member.

            Parameters:
                self

            Returns:
                 full_d (dictionary):               dictionary of all member, load, joint (key) and results (values)
                 beam_names (list):                 list all beam names in the results set
                 load_names (list):                 list all load names in teh results set
        """
        beam_names = []
        beam_index = []
        header_line = self.member_forces[0]
        headers = re.split(r'\s{2,}', header_line)[1:]
        member_forces = self.member_forces[1:]
        complete_column_start_idx = [0, 10, 19, 28, 44, 60, 76, 92, 108]
        line_end = [124]
        #TODO: Get rid of these magic numbers
        column_start = complete_column_start_idx[0:len(headers) + 3] + line_end
        value_columns = complete_column_start_idx[4: 4 + len(headers)] + line_end
        full_d = {}
        full_d = utilities.TupleDict(full_d)
        load_cases = []
        for row_num, line in enumerate(member_forces):
            column_1 = line[column_start[0]: column_start[1]].strip()
            if (column_1 or column_1.startswith('1')) and not column_1.startswith("****"):
                beam_names.append([column_1])
                beam_index.append(row_num)
        beam_names.pop()
        for block_id, beam in enumerate(beam_names):
            block_load = []
            block_start = beam_index[block_id: block_id + 2][0]
            block_end = beam_index[block_id: block_id + 2][1]
            block = member_forces[block_start:block_end]
            for row_id, row in enumerate(block):
                numbers = []
                column_2 = row[column_start[1]: column_start[2]].strip()
                formatted_array = "".join(block[row_id]).split()
                if '****' in formatted_array[0]:
                    pass
                else:
                    if row_id > 0:
                        formatted_array.insert(0, beam[0])
                    if column_2:
                        load = row[column_start[1]: column_start[2]].strip()
                        block_load.append(load)
                    if column_2 == "":
                        formatted_array.insert(1, load)
                for ih, col_id in enumerate(value_columns):
                    if col_id > len(row) + 1:
                        numbers.append(False)
                    elif "." in row[column_start[ih + 3]:col_id]:
                        numbers.append(True)
                    else:
                        numbers.append(False)
                for number_id, value in enumerate(numbers):
                    if value:
                        pass
                    else:
                        formatted_array.insert(3 + number_id, " ")
                k = tuple(formatted_array[0:3])
                full_d[k] = formatted_array[3:]
            load_cases.append(block_load)
        return full_d, beam_names, load_cases

    def user_input_sorting(self, beam_names, load_names):
        """
        Takes the full list of beam and load names and generates a sub list based on the user specified beam_id
        requirements. The returned values are nested lists in which the index of the nested list is the same for
        each beam and load in the block.

            Parameters:
                beam_names:         full list of beam names for each block
                load_names:         full list of load names for each block

            Returns:
                 user_beam (list):       list of lists of beam names which meet the user criteria
                 user_loads (list):      list of lists of load names which meet the user criteria
        """
        beam_choice = self.beam_id[self.mem_set_index][0]
        load_choice = self.load_id[self.mem_set_index][0]
        user_loads = []
        user_beams = []
        load = []
        if beam_choice == 2:
            beam_starts_with = self.beam_id[self.mem_set_index][1]
            for b_idx, beams in enumerate(beam_names):
                if beams[0].startswith(beam_starts_with):
                    user_beams.append(beams)
                    load.append(load_names[b_idx])
                else:
                    pass
        elif beam_choice == 3:
            beam_ends_with = self.beam_id[self.mem_set_index][1]
            for b_idx, beams in enumerate(beam_names):
                if beams[0].endswith(beam_ends_with):
                    user_beams.append(beams)
                    load.append(load_names[b_idx])
                else:
                    pass
        elif beam_choice == 4:
            beam_contains = self.beam_id[self.mem_set_index][1]
            for b_idx, beams in enumerate(beam_names):
                if beam_contains in beams[0]:
                    user_beams.append(beams)
                    load.append(load_names[b_idx])
                else:
                    pass
        elif beam_choice == 5:
            beam_text = self.beam_id[self.mem_set_index][1].upper()
            beam_list = "".join(beam_text).replace(" ", "").split(',')
            for item in beam_list:
                b_idx = beam_names.index([item])
                user_beams.append([item])
                load.append(load_names[b_idx])
        else:
            user_beams = beam_names
            load = load_names
        if load:
            if load_choice == 2:
                load_starts_with = self.load_id[self.mem_set_index][1]
                for l_idx, loads in enumerate(load):
                    matching_loads = [l for l in loads if l.startswith(load_starts_with)]
                    user_loads.append(matching_loads)
            elif load_choice == 3:
                load_ends_with = self.load_id[self.mem_set_index][1]
                for l_idx, loads in enumerate(load):
                    matching_loads = [l for l in loads if l.endswith(load_ends_with)]
                    user_loads.append(matching_loads)
            elif load_choice == 4:
                load_contains = self.load_id[self.mem_set_index][1]
                for l_idx, loads in enumerate(load):
                    matching_loads = [l for l in loads if load_contains in l]
                    user_loads.append(matching_loads)
            elif load_choice == 5:
                load_text = self.load_id[self.mem_set_index][1].upper()
                load_list = "".join(load_text).replace(" ", "").split(',')
                for l_idx, loads in enumerate(load):
                    beam_loads = [l for l in load_list if l in loads]
                    user_loads.append(beam_loads)
            else:
                user_loads = load
        else:
            pass
        if user_beams:
            if user_loads:
                for b_idx, beams in enumerate(user_beams):
                    if not user_loads[b_idx]:
                        del user_beams[b_idx]
                        del user_loads[b_idx]
            else:
                user_beams.clear()
        else:
            user_loads.clear()
        return user_beams, user_loads

    def requested_member_force_array(self):
        """
        Builds a dictionary key / value pairs which match the joint, load, and beam criteria requested by the user.
            Parameters:
                self

            Returns:
                 output (dict):     dictionary of key / value pairs which match all joint, load, and beam criteria
                                    specified by the user
                 errors (list):     list of beam and load errors (items requested by user not in result set)
        """
        d, all_beams, all_loads = self.member_force_array()
        user_beams, user_loads = self.user_input_sorting(all_beams, all_loads)
        d_joints = {}
        output = {}
        for key, value in d.items():
            if (key[0] in d_joints) and (key[2] not in d_joints[key[0]]):
                key_list = d_joints[key[0]]
                key_list.append(key[2])
                d_joints[key[0]] = key_list
            else:
                d_joints[key[0]] = [key[2]]
        if not user_beams or not user_loads:
            pass
        else:
            for b_idx, beams in enumerate(user_beams):
                current_beam = beams[0]
                indices = [0] if self.joint == 'START' else [1] if self.joint == 'END' else \
                    range(len(d_joints[current_beam]))
                for l_idx, loads in enumerate(user_loads[b_idx]):
                    current_load = loads
                    for index in indices:
                        t = (current_beam, current_load, d_joints[current_beam][index])
                        output[t] = d[t]
        return output

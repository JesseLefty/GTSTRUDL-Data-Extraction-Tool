from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import error_handling
import json
import os
import save_output
import utilities_GUI


class MemberForceFrame:

    def __init__(self, member_force_frame, initial_window, directory, input_file_path, modify=False):
        self.jt_rb = StringVar()
        self.load_rb = IntVar()
        self.beam_rb = IntVar()
        self.replace = modify
        self.member_force_frame = member_force_frame
        self.initial_window = initial_window
        self.directory = directory
        self.input_file_path = input_file_path

    window_open = False
    delete = False
    file_types = [('*.prop - properties file', '*.prop')]
    sel_rlist = "none"
    joint = []
    load_id = []
    member_set = []
    beam_id = []
    key = [1, 2, 3, 4, 5]
    value = ['', 'Starts With: ', 'Ends With: ', 'Contains: ', 'List: ']
    d_tree = {}
    for row, item in enumerate(key):
        d_tree[key[row]] = value[row]

    def main_tab(self):
        self.joint.clear()
        self.load_id.clear()
        self.beam_id.clear()
        self.member_set.clear()
        member_force_list, input_index = utilities_GUI.GenerateDisplayData(self.input_file_path).get_display('Member Force')
        result_tree_headings = ['Set #', 'Set Name', 'Joint Spec.', 'Load Spec.', 'Beam Spec.']
        available_results_headings = ['Set #', 'Set Name', 'Input line #']
        if member_force_list:
            not_valid_list = False
        else:
            available_results_list = 'No Member Forces Found in Output'
            not_valid_list = True

        def on_list_select(event):
            if not_valid_list:
                new_mem_result_set['state'] = 'disabled'
            else:
                new_mem_result_set['state'] = 'enabled'
                modify_force_result['state'] = 'disabled'
                delete_force_result['state'] = 'disabled'

        def on_tree_select(event):
            modify_force_result['state'] = 'enabled'
            delete_force_result['state'] = 'enabled'
            new_mem_result_set['state'] = 'disabled'
            if len(results_tree.selection()) > 1:
                modify_force_result['state'] = 'disabled'
            elif not results_tree.get_children():
                delete_force_result['state'] = 'disabled'
                modify_force_result['state'] = 'disabled'

        def list_select():
            selection_index = int(available_results_tree.selection()[0]) - 1
            display_index = int(available_results_tree.selection()[0])
            stored_value = available_results_tree.item(display_index, "text")
            return selection_index, stored_value

        def tree_select():
            if modify_force_result['state'] == 'enabled':
                tree_selection_index = int(results_tree.selection()[0])
            else:
                tree_selection_index = 0
            return tree_selection_index

        temp_header = Label(self.member_force_frame, text="Member Force Extraction")
        result_set_frame = LabelFrame(self.member_force_frame, text='Available Member Results', height=160, width=420)
        display_result_set_frame = LabelFrame(self.member_force_frame, text='Requested Results', height=135, width=580)
        button_frame = Frame(self.member_force_frame, height=160, width=150)
        continue_frame = Frame(self.member_force_frame, height=30, width=580)

        temp_header.grid(row=0, column=0, columnspan=1, padx=10, pady=(5, 0))
        result_set_frame.grid(row=1, column=1, padx=(0, 10), pady=(5, 0), sticky='nw')
        display_result_set_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=(5, 0), sticky='nsew')
        button_frame.grid(row=1, column=0, padx=10, pady=(5, 0))
        continue_frame.grid(row=3, column=0, columnspan=3, pady=(5, 10), padx=(0, 10), sticky='se')

        result_set_frame.grid_propagate(0)
        display_result_set_frame.grid_propagate(0)
        button_frame.grid_propagate(0)

        available_results_tree = Treeview(result_set_frame, columns=available_results_headings, show='headings', height=5)

        for idx, col in enumerate(available_results_headings):
            available_results_tree.heading(col, text=col.title())
            tree_width = [40, 275, 75]
            tree_anchor = [CENTER, W, CENTER]
            available_results_tree.column(col, width=tree_width[idx], minwidth=tree_width[idx], anchor=tree_anchor[idx])
        for idx, value in enumerate(member_force_list, start=1):
            if not_valid_list:
                available_results_tree.insert(parent='', index='end', iid=idx, text=available_results_list,
                                              values=(idx, available_results_list))
            else:
                available_results_tree.insert(parent='', index='end', iid=idx, text=value,
                                              values=(idx, value, input_index[idx - 1]))

        available_results_tree.bind('<<TreeviewSelect>>', on_list_select)

        list_yscroll = Scrollbar(result_set_frame)
        list_xscroll = Scrollbar(result_set_frame)
        list_xscroll.configure(command=available_results_tree.xview, orient=HORIZONTAL)
        list_yscroll.configure(command=available_results_tree.yview, orient=VERTICAL)

        list_yscroll.pack(side=RIGHT, fill=Y)
        list_xscroll.pack(side=BOTTOM, fill=X)
        available_results_tree.pack(side=LEFT, expand=True)

        results_tree = Treeview(display_result_set_frame, columns=result_tree_headings, show='headings', height=3)
        tree_scrollx = Scrollbar(display_result_set_frame)
        tree_scrolly = Scrollbar(display_result_set_frame)
        tree_scrollx.configure(command=results_tree.xview, orient=HORIZONTAL)
        tree_scrolly.configure(command=results_tree.yview)
        results_tree.configure(xscrollcommand=tree_scrollx.set, yscrollcommand=tree_scrolly.set)
        tree_scrolly.pack(side=RIGHT, fill=Y)
        tree_scrollx.pack(side=BOTTOM, fill=X)
        results_tree.pack(side=LEFT, fill=X, expand=True)
        tree_index = 0
        for col in result_tree_headings:
            results_tree.heading(col, text=col.title())
            tree_width = [40, 200, 100, 100, 100]
            tree_anchor = [CENTER, W, CENTER, W, W]
            results_tree.column(col, width=tree_width[tree_index], minwidth=tree_width[tree_index],
                                anchor=tree_anchor[tree_index])
            tree_index += 1
        results_tree.bind('<<TreeviewSelect>>', on_tree_select)

        Label(button_frame, text='Member Result Set Options').grid(column=0, row=0)
        new_mem_result_set = Button(button_frame, text="Create New",
                                    command=lambda: NewResultsWindow(self.jt_rb, self.load_rb, self.beam_rb,
                                                                     self.initial_window, self.member_force_frame,
                                                                     self.directory,
                                                                     self.input_file_path).new_mem_result_set(
                                        list_select(), results_tree, tree_select(), False))
        load_exist_mem_result_set = Button(button_frame, text="Load Existing",
                                           command=lambda: self.load_existing_mem_result_set(results_tree))
        modify_force_result = Button(button_frame, text='Modify Result',
                                     command=lambda: self.modify_force_result(results_tree,
                                                                              tree_select()))
        delete_force_result = Button(button_frame, text='Delete Result',
                                     command=lambda: self.delete_force_result(results_tree))

        new_mem_result_set.grid(row=2, column=0, padx=15, pady=5, sticky='ew')
        load_exist_mem_result_set.grid(row=3, column=0, padx=15, pady=5, sticky='ew')
        modify_force_result.grid(row=4, column=0, padx=15, pady=5, sticky='ew')
        delete_force_result.grid(row=5, column=0, padx=15, pady=5, sticky='ew')

        generate_button = Button(continue_frame, text="Generate",
                                 command=lambda: self.run_member_forces(self.joint))

        store_mem_results_prop = Button(continue_frame, text='Store Input',
                                        command=lambda: self.store_inputs(results_tree))

        store_mem_results_prop.grid(row=0, column=0, padx=(10, 405), pady=5)
        generate_button.grid(row=0, column=3, padx=5, pady=5)

        new_mem_result_set['state'] = 'disabled'
        delete_force_result['state'] = 'disabled'
        modify_force_result['state'] = 'disabled'

    def store_member_force_info(self, force_select_window, joint, beam_id_tpl, load_id_tpl, selection_index,
                                results_tree, tree_select):
        force_select_window.destroy()
        selection_index, stored_value = selection_index
        if tree_select == 0:
            tree_selection = 0
        else:
            tree_selection = int(results_tree.selection()[0])

        if self.replace:
            set_name = results_tree.set(tree_selection, column=1)
            set_num_index = int(results_tree.set(tree_selection, column=0)) - 1
            self.joint[set_num_index] = joint
            self.load_id[set_num_index] = load_id_tpl
            self.beam_id[set_num_index] = beam_id_tpl
            results_tree.item(tree_selection, values=(tree_selection, set_name, joint,
                                                      f'{self.d_tree[load_id_tpl[0]]} {load_id_tpl[1]}',
                                                      f'{self.d_tree[beam_id_tpl[0]]} {beam_id_tpl[1]}'))
        else:
            self.load_id.append(load_id_tpl)
            self.joint.append(joint)
            self.beam_id.append(beam_id_tpl)
            self.member_set.append(selection_index)
            try:
                next_avail_idd = max([int(x) for x in results_tree.get_children()]) + 1
            except ValueError:
                next_avail_idd = 1
            results_tree.insert(parent='', index='end', iid=next_avail_idd, text=stored_value,
                                values=(next_avail_idd, stored_value, joint,
                                        f'{self.d_tree[load_id_tpl[0]]} {load_id_tpl[1]}',
                                        f'{self.d_tree[beam_id_tpl[0]]} {beam_id_tpl[1]}'))

        for row, item in enumerate(results_tree.get_children()):
            results_tree.set(item, column=0, value=row + 1)

        print(f'joint = {self.joint}')
        print(f'load = {self.load_id}')
        print(f'beam = {self.beam_id}')
        print(f'member set = {self.member_set}')

    def store_inputs(self, results_tree):
        d_data = {}
        set_name = []
        if not results_tree.get_children():
            error_handling.ErrorHandling(self.initial_window).no_result_set()
        else:
            prop_file_name = filedialog.asksaveasfilename(filetypes=self.file_types, defaultextension='*.prop')
            for rows, count in enumerate(results_tree.get_children()):
                set_name.append(results_tree.set(count, column=1))
                d_data[rows + 1] = {'set name': set_name[rows],
                                    'joint spec': self.joint[rows],
                                    'load spec': self.load_id[rows],
                                    'beam spec': self.beam_id[rows],
                                    'member set': self.member_set[rows]}
            d_force_results = {'Member Force Results': d_data}

            try:
                with open(prop_file_name, 'w') as f:
                    json.dump(d_force_results, f, indent=4)
            except FileNotFoundError:
                pass

    def load_existing_mem_result_set(self, results_tree):
        load_existing_file_path = filedialog.askopenfilename(initialdir=self.directory, title="select file",
                                                             filetypes=self.file_types)
        try:
            with open(load_existing_file_path) as json_file:
                data = json.load(json_file)

            for rows in range(len(data['Member Force Results'].keys())):
                if results_tree.get_children():
                    next_avail_idd = max([int(x) for x in results_tree.get_children()]) + 1
                else:
                    next_avail_idd = 1
                key_num = str(rows + 1)
                self.joint.append(data['Member Force Results'][key_num]['joint spec'])
                self.load_id.append(data['Member Force Results'][key_num]['load spec'])
                self.beam_id.append(data['Member Force Results'][key_num]['beam spec'])
                self.member_set.append(data['Member Force Results'][key_num]['member set'])
                set_name = data['Member Force Results'][key_num]['set name']
                results_tree.insert(parent='', index='end', iid=next_avail_idd, text=set_name,
                                    values=(next_avail_idd, set_name, self.joint[-1],
                                            f'{self.d_tree[self.load_id[-1][0]]} {self.load_id[-1][1]}',
                                            f'{self.d_tree[self.beam_id[-1][0]]} {self.beam_id[-1][1]}'))
                for row, item in enumerate(results_tree.get_children()):
                    results_tree.set(item, column=0, value=row + 1)

        except KeyError:
            error_handling.ErrorHandling(self.initial_window).wrong_properties_file('member force results')
        except FileNotFoundError:
            print('file not found')
            pass
        except UnboundLocalError:
            pass

    def modify_force_result(self, results_tree, tree_select):
        if tree_select == 0:
            tree_selection = 0
        else:
            tree_selection = int(results_tree.selection()[0])
        set_num_index = int(results_tree.set(tree_selection, column=0)) - 1
        self.jt_rb.set(self.joint[set_num_index])
        self.load_rb.set(self.load_id[set_num_index][0])
        self.beam_rb.set(self.beam_id[set_num_index][0])
        beam_text = self.beam_id[set_num_index][1]
        load_text = self.load_id[set_num_index][1]
        NewResultsWindow(self.jt_rb, self.load_rb, self.beam_rb, self.member_force_frame, self.initial_window,
                         self.directory, self.input_file_path, beam_text=beam_text, load_text=load_text).\
            new_mem_result_set((0, 0), results_tree, tree_select, True)

    def delete_force_result(self, results_tree):
        for tree_selection in results_tree.selection():
            set_num = int(results_tree.set(tree_selection, column=0)) - 1
            results_tree.delete(tree_selection)
            del self.joint[set_num]
            del self.load_id[set_num]
            del self.beam_id[set_num]
            del self.member_set[set_num]
            for row, item in enumerate(results_tree.get_children()):
                results_tree.set(item, column=0, value=row + 1)
        if results_tree.get_children():
            next_idd = results_tree.get_children()[0]
            results_tree.selection_set(next_idd)
        else:
            pass

    def run_member_forces(self, joint):
        file_types = [('Excel File', '*.xlsx'), ('csv Files', '*.csv')]
        output_file_path = filedialog.asksaveasfilename(filetypes=file_types, defaultextension='xlsx')
        out_format = os.path.splitext(output_file_path)[1]
        save_output.RunProgram(self.initial_window).run_member_forces(output_file_path, joint, self.member_set, out_format,
                                                                      self.input_file_path, self.beam_id,
                                                                      self.load_id)
        print(self.joint)


class NewResultsWindow:

    def __init__(self, jt_rb, load_rb, beam_rb, initial_window, member_force_frame, directory, input_file_path,
                 beam_text='ALL', load_text='ALL'):
        self.jt_rb = jt_rb
        self.load_rb = load_rb
        self.beam_rb = beam_rb
        self.initial_window = initial_window
        self.member_force_frame = member_force_frame
        self.directory = directory
        self.input_file_path = input_file_path
        self.mod_beam_text = beam_text
        self.mod_load_text = load_text

    def new_mem_result_set(self, selection_index, results_tree, tree_selection_index, modify):
        if not modify:
            self.jt_rb.set('ALL')
            self.load_rb.set("1")
            self.beam_rb.set("1")
        else:
            pass
        force_select_window = Toplevel(self.initial_window)
        force_select_window.geometry('400x360')
        utilities_GUI.center(force_select_window, x_offset=-500)
        force_select_window.resizable(False, False)
        force_select_window.grid_propagate(0)
        force_select_window.grab_set()

        def beam_text_get(beam_rb_val):
            if beam_rb_val == 1:
                beam_id = 'ALL'
            else:
                beam_id = beam_text.get('1.0', 'end-1c')
            return beam_rb_val, beam_id

        def load_text_get(load_rb_val):
            if load_rb_val == 1:
                load_id = 'ALL'
            else:
                load_id = load_text.get('1.0', 'end-1c')
            return load_rb_val, load_id

        def text_return():
            return 'break'

        new_result_set_header = Label(force_select_window, text="Member Force Results Parameter Selection")
        joint_select = LabelFrame(force_select_window, text='JOINT', height=50, width=380)
        load_select = LabelFrame(force_select_window, text='LOAD CASE(s)', height=100, width=380)
        beam_select = LabelFrame(force_select_window, text='MEMBER(s)', height=100, width=380)
        continue_frame = Frame(force_select_window, height=60, width=380)

        new_result_set_header.grid(row=0, column=0, columnspan=6, padx=10, pady=(10, 0))
        joint_select.grid(row=1, column=0, padx=10, pady=(10, 0))
        load_select.grid(row=2, column=0, columnspan=5, padx=10, pady=(10, 0))
        beam_select.grid(row=3, column=0, columnspan=5, padx=10, pady=(10, 0))
        continue_frame.grid(row=4, column=0, columnspan=6, pady=(5, 10), padx=(0, 10), sticky='se')

        joint_select.grid_propagate(0)
        load_select.grid_propagate(0)
        beam_select.grid_propagate(0)

        jt_all_rb = Radiobutton(joint_select, text='ALL', variable=self.jt_rb, value='ALL')
        jt_sta_rb = Radiobutton(joint_select, text='START', variable=self.jt_rb, value='START')
        jt_end_rb = Radiobutton(joint_select, text='END', variable=self.jt_rb, value='END')

        jt_all_rb.grid(row=0, column=0)
        jt_sta_rb.grid(row=0, column=1)
        jt_end_rb.grid(row=0, column=2)

        load_all_rb = Radiobutton(load_select, text='ALL', variable=self.load_rb, value=1)
        load_sta_wth_rb = Radiobutton(load_select, text='STARTS WITH', variable=self.load_rb, value=2)
        load_end_wth_rb = Radiobutton(load_select, text='ENDS WITH', variable=self.load_rb, value=3)
        load_contains_rb = Radiobutton(load_select, text='CONTAINS', variable=self.load_rb, value=4)
        load_list_rb = Radiobutton(load_select, text='LIST', variable=self.load_rb, value=5)
        load_text = Text(load_select, height=1, width=50, font=('Arial', 10), wrap=NONE)
        load_scrollx = Scrollbar(load_select)
        load_scrollx.configure(command=load_text.xview, orient=HORIZONTAL)
        utilities_GUI.CreateToolTip(load_text, f'Do not use single or double quotes around text entries.'
                                               f' All list entries must be separated by a comma and space'
                                               f' (example: LC1, LC2, LC3)')

        load_all_rb.grid(row=0, column=0)
        load_sta_wth_rb.grid(row=0, column=1)
        load_end_wth_rb.grid(row=0, column=2)
        load_contains_rb.grid(row=0, column=3)
        load_list_rb.grid(row=0, column=4)
        load_text.grid(row=1, column=0, columnspan=5, sticky='nw', pady=5, padx=5)
        load_scrollx.grid(row=2, column=0, columnspan=5, sticky='ew')

        load_text.configure(xscrollcommand=load_scrollx.set)
        load_text.config(state='normal')
        load_text.insert('1.0', 'ALL')
        load_text.bind('<Return>', lambda event, : text_return())

        beam_all_rb = Radiobutton(beam_select, text='ALL', variable=self.beam_rb, value=1)
        beam_sta_wth_rb = Radiobutton(beam_select, text='STARTS WITH', variable=self.beam_rb, value=2)
        beam_end_wth_rb = Radiobutton(beam_select, text='ENDS WITH', variable=self.beam_rb, value=3)
        beam_contains_rb = Radiobutton(beam_select, text='CONTAINS', variable=self.beam_rb, value=4)
        beam_list_rb = Radiobutton(beam_select, text='LIST', variable=self.beam_rb, value=5)
        beam_text = Text(beam_select, height=1, width=50, font=('Arial', 10), wrap=NONE)
        beam_scrollx = Scrollbar(beam_select)
        beam_scrollx.configure(command=beam_text.xview, orient=HORIZONTAL)
        utilities_GUI.CreateToolTip(beam_text, f'Do not use single or double quotes around text entries.'
                                               f' All list entries must be separated by a comma and space'
                                               f' (example: Beam1, Beam2)')

        beam_all_rb.grid(row=0, column=0)
        beam_sta_wth_rb.grid(row=0, column=1)
        beam_end_wth_rb.grid(row=0, column=2)
        beam_contains_rb.grid(row=0, column=3)
        beam_list_rb.grid(row=0, column=4)
        beam_text.grid(row=1, column=0, columnspan=5, sticky='nw', pady=5, padx=5)
        beam_scrollx.grid(row=2, column=0, columnspan=5, sticky='ew')

        beam_text.configure(xscrollcommand=beam_scrollx.set)
        beam_text.config(state='normal')
        beam_text.insert('1.0', 'ALL')
        beam_text.bind('<Return>', lambda event, : text_return())

        if modify:
            beam_text.delete('0.0', END)
            load_text.delete('0.0', END)
            beam_text.insert('1.0', self.mod_beam_text)
            load_text.insert('1.0', self.mod_load_text)

        store_button = Button(continue_frame, text="Store",
                              command=lambda: MemberForceFrame(self.member_force_frame, self.initial_window,
                                                               self.directory, self.input_file_path, modify).
                              store_member_force_info(force_select_window, self.jt_rb.get(),
                                                      beam_text_get(self.beam_rb.get()),
                                                      load_text_get(self.load_rb.get()), selection_index,
                                                      results_tree, tree_selection_index))
        cancel_button = Button(continue_frame, text="Cancel", command=lambda: force_select_window.destroy())

        store_button.grid(row=0, column=2, padx=5, pady=5)
        cancel_button.grid(row=0, column=1, padx=5, pady=5)

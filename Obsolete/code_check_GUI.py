from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import error_handling
import json
import os
import save_output
import utilities_GUI


class CodeCheckFrame:

    def __init__(self, code_check_frame, initial_window, directory, input_file_path, modify=False):

        self.name_rb = IntVar()
        self.profile_rb = IntVar()
        self.ir_range_rb = IntVar()
        self.fail_cb = BooleanVar()
        self.replace = modify
        self.code_check_frame = code_check_frame
        self.initial_window = initial_window
        self.directory = directory
        self.input_file_path = input_file_path
        self.sort_cb = BooleanVar()
        self.sort_order_dict = {'IR Value': 5, 'Name': 0, 'Profile': 8}

    reverse = []
    window_open = False
    delete = False
    file_types = [('*.prop - properties file', '*.prop')]
    sel_rlist = "none"
    name_id = []
    code_set = []
    profile_id = []
    ir_range_id = []
    fail_id = []
    sort_request = []
    sort_order = []
    key = [1, 2, 3, 4, 5]
    value = ['', 'Starts With: ', 'Ends With: ', 'Contains: ', 'List: ']
    d_tree = {}
    d_tree_2 = {}
    for row, item in enumerate(key):
        d_tree[key[row]] = value[row]

    def main_tab(self):
        self.name_id.clear()
        self.profile_id.clear()
        self.ir_range_id.clear()
        self.fail_id.clear()
        self.code_set.clear()
        self.sort_request.clear()
        code_check_list, input_index = utilities_GUI.GenerateDisplayData(self.input_file_path).get_display("Code Check")
        result_tree_headings = ['Set #', 'Set Name', 'Name Spec.', 'Profile Spec.', 'IR Range', 'Sort']
        available_results_headings = ['Set #', 'Set Name', 'Input Line #']
        if code_check_list:
            not_valid_list = False
        else:
            available_results_list = 'No Code Check Found in Output'
            not_valid_list = True

        def on_list_select(event):
            if not_valid_list:
                new_code_result_set['state'] = 'disabled'
            else:
                new_code_result_set['state'] = 'enabled'
                modify_code_result['state'] = 'disabled'
                delete_code_result['state'] = 'disabled'

        def on_tree_select(event):
            modify_code_result['state'] = 'enabled'
            delete_code_result['state'] = 'enabled'
            new_code_result_set['state'] = 'disabled'
            if len(results_tree.selection()) > 1:
                modify_code_result['state'] = 'disabled'
            elif not results_tree.get_children():
                delete_code_result['state'] = 'disabled'
                modify_code_result['state'] = 'disabled'

        def list_select():
            selection_index = int(available_results_tree.selection()[0]) - 1
            display_index = int(available_results_tree.selection()[0])
            stored_value = available_results_tree.item(display_index, "text")
            return selection_index, stored_value

        def tree_select():
            if modify_code_result['state'] == 'enabled':
                tree_selection_index = int(results_tree.selection()[0])
            else:
                tree_selection_index = 0
            return tree_selection_index

        temp_header = Label(self.code_check_frame, text="Code Check Extraction")
        result_set_frame = LabelFrame(self.code_check_frame, text='Available Code Check Results', height=160, width=420)
        display_result_set_frame = LabelFrame(self.code_check_frame, text='Requested Results', height=135, width=580)
        button_frame = Frame(self.code_check_frame, height=160, width=150)
        continue_frame = Frame(self.code_check_frame, height=30, width=580)

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
        for idx, value in enumerate(code_check_list, start=1):
            display_text = f'{value} ({idx})'
            if not_valid_list:
                available_results_tree.insert(parent='', index='end', iid=idx, text=available_results_list,
                                              values=(idx, available_results_list))
            else:
                available_results_tree.insert(parent='', index='end', iid=idx, text=display_text,
                                              values=(idx, display_text, input_index[idx - 1]))

        available_results_tree.bind('<<TreeviewSelect>>', on_list_select)

        list_yscroll = Scrollbar(result_set_frame)
        list_xscroll = Scrollbar(result_set_frame)
        list_xscroll.configure(command=available_results_tree.xview, orient=HORIZONTAL)
        list_yscroll.configure(command=available_results_tree.yview, orient=VERTICAL)
        available_results_tree.configure(xscrollcommand=list_xscroll.set, yscrollcommand=list_yscroll.set)

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
            tree_width = [40, 150, 50, 50, 50, 50]
            tree_anchor = [CENTER, W, CENTER, CENTER, CENTER, CENTER]
            results_tree.column(col, width=tree_width[tree_index], minwidth=tree_width[tree_index],
                                anchor=tree_anchor[tree_index])
            tree_index += 1
        results_tree.bind('<<TreeviewSelect>>', on_tree_select)

        Label(button_frame, text='Code Check Set Options').grid(column=0, row=0)
        new_code_result_set = Button(button_frame, text="Create New",
                                    command=lambda: NewResultsWindow(self.name_rb, self.profile_rb, self.ir_range_rb,
                                                                     self.fail_cb, self.sort_cb, self.sort_order,
                                                                     self.initial_window, self.code_check_frame,
                                                                     self.directory,
                                                                     self.input_file_path).new_code_result_set(
                                        list_select(), results_tree, tree_select(), self.replace))
        load_exist_code_result_set = Button(button_frame, text="Load Existing",
                                            command=lambda: self.load_existing_code_result_set(results_tree))
        modify_code_result = Button(button_frame, text='Modify Result',
                                     command=lambda: self.modify_code_result(results_tree,
                                                                             tree_select()))
        delete_code_result = Button(button_frame, text='Delete Result',
                                    command=lambda: self.delete_code_result(results_tree))

        new_code_result_set.grid(row=2, column=0, padx=15, pady=5, sticky='ew')
        load_exist_code_result_set.grid(row=3, column=0, padx=15, pady=5, sticky='ew')
        modify_code_result.grid(row=4, column=0, padx=15, pady=5, sticky='ew')
        delete_code_result.grid(row=5, column=0, padx=15, pady=5, sticky='ew')

        generate_button = Button(continue_frame, text="Generate",
                                 command=lambda: self.run_code_check())

        store_code_results_prop = Button(continue_frame, text='Store Input',
                                        command=lambda: self.store_inputs(results_tree))

        store_code_results_prop.grid(row=0, column=0, padx=(10, 405), pady=5)
        generate_button.grid(row=0, column=3, padx=5, pady=5)

        new_code_result_set['state'] = 'disabled'
        delete_code_result['state'] = 'disabled'
        modify_code_result['state'] = 'disabled'

    def store_code_check_info(self, code_select_window, profile_id_tpl, name_id_tpl, selection_index,
                              results_tree, tree_select, ir_range_id_tpl, fail_id, sort_request, sort_order, reverse):
        code_select_window.destroy()
        selection_index, stored_value = selection_index
        if tree_select == 0:
            tree_selection = 0
        else:
            tree_selection = int(results_tree.selection()[0])
        specific_sort = []
        reverse_order = []
        for item in sort_order:
            specific_sort.append((self.sort_order_dict[item], True))
            reverse_order.append(reverse)
            print(reverse_order)
        if self.replace:
            set_name = results_tree.set(tree_selection, column=1)
            set_num_index = int(results_tree.set(tree_selection, column=0)) - 1
            self.name_id[set_num_index] = name_id_tpl
            self.profile_id[set_num_index] = profile_id_tpl
            self.ir_range_id[set_num_index] = ir_range_id_tpl
            self.fail_id[set_num_index] = fail_id
            self.sort_request[set_num_index] = sort_request
            self.sort_order[set_num_index] = specific_sort
            self.reverse[set_num_index] = reverse_order
            results_tree.item(tree_selection, values=(tree_selection, set_name,
                                                      f'{self.d_tree[name_id_tpl[0]]} {name_id_tpl[1]}',
                                                      f'{self.d_tree[profile_id_tpl[0]]} {profile_id_tpl[1]}',
                                                      f'{ir_range_id_tpl[1][0]} - {ir_range_id_tpl[1][1]}',
                                                      f'{sort_request}'))
        else:
            self.name_id.append(name_id_tpl)
            self.profile_id.append(profile_id_tpl)
            self.ir_range_id.append(ir_range_id_tpl)
            self.fail_id.append(fail_id)
            self.sort_request.append(sort_request)
            self.code_set.append(selection_index)
            self.sort_order.append(specific_sort)
            self.reverse.append(reverse_order)
            try:
                next_avail_idd = max([int(x) for x in results_tree.get_children()]) + 1
            except ValueError:
                next_avail_idd = 1
            results_tree.insert(parent='', index='end', iid=next_avail_idd, text=stored_value,
                                values=(next_avail_idd, stored_value,
                                        f'{self.d_tree[name_id_tpl[0]]} {name_id_tpl[1]}',
                                                      f'{self.d_tree[profile_id_tpl[0]]} {profile_id_tpl[1]}',
                                                      f'{ir_range_id_tpl[1][0]} - {ir_range_id_tpl[1][1]}',
                                                      f'{sort_request}'))

        for row, item in enumerate(results_tree.get_children()):
            results_tree.set(item, column=0, value=row + 1)

        print(f'name spec: {self.name_id}')
        print(f'profile spec: {self.profile_id}')
        print(f'IR Range: {self.ir_range_id}')
        print(f'sort spec: {self.sort_request}')
        print(f'fail id: {self.fail_id}')
        print(f'sort order: {self.sort_order}')
        print(f'reverse: {self.reverse}')
        print(f'code set: {self.code_set}')

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
                                    'name spec': self.name_id[rows],
                                    'profile spec': self.profile_id[rows],
                                    'code set': self.code_set[rows],
                                    'ir_spec': self.ir_range_id[rows],
                                    'sort_spec': self.sort_request[rows],
                                    'sort_order': self.sort_order[rows],
                                    'reverse': self.reverse[rows],
                                    'fail': self.fail_id[rows]}
            d_code_results = {'Code Check Results': d_data}

            try:
                with open(prop_file_name, 'w') as f:
                    json.dump(d_code_results, f, indent=4)
            except FileNotFoundError:
                pass

    def load_existing_code_result_set(self, results_tree):
        load_existing_file_path = filedialog.askopenfilename(initialdir=self.directory, title="select file",
                                                             filetypes=self.file_types)
        try:
            with open(load_existing_file_path) as json_file:
                data = json.load(json_file)

            for rows in range(len(data['Code Check Results'].keys())):
                if results_tree.get_children():
                    next_avail_idd = max([int(x) for x in results_tree.get_children()]) + 1
                else:
                    next_avail_idd = 1
                key_num = str(rows + 1)
                self.name_id.append(data['Code Check Results'][key_num]['name spec'])
                self.profile_id.append(data['Code Check Results'][key_num]['profile spec'])
                self.code_set.append(data['Code Check Results'][key_num]['code set'])
                self.ir_range_id.append(data['Code Check Results'][key_num]['ir_spec'])
                self.sort_request.append(data['Code Check Results'][key_num]['sort_spec'])
                self.sort_order.append(data['Code Check Results'][key_num]['sort_order'])
                self.reverse.append(data['Code Check Results'][key_num]['reverse'])
                self.fail_id.append(data['Code Check Results'][key_num]['fail'])
                set_name = data['Code Check Results'][key_num]['set name']
                results_tree.insert(parent='', index='end', iid=next_avail_idd, text=set_name,
                                    values=(next_avail_idd, set_name,
                                            f'{self.d_tree[self.name_id[-1][0]]} {self.name_id[-1][1]}',
                                            f'{self.d_tree[self.profile_id[-1][0]]} {self.profile_id[-1][1]}',
                                            f'{self.ir_range_id[-1][1][0]} - {self.ir_range_id[-1][1][1]}',
                                            f'{self.sort_request[-1]}'))

                print(self.ir_range_id)
                for row, item in enumerate(results_tree.get_children()):
                    results_tree.set(item, column=0, value=row + 1)

        except KeyError as e:
            error_handling.ErrorHandling(self.initial_window).wrong_properties_file('code check')
            print(e)
        except FileNotFoundError:
            print('file not found')
            pass
        except UnboundLocalError:
            pass

    def modify_code_result(self, results_tree, tree_select):
        if tree_select == 0:
            tree_selection = 0
        else:
            tree_selection = int(results_tree.selection()[0])
        set_num_index = int(results_tree.set(tree_selection, column=0)) - 1
        self.name_rb.set(self.name_id[set_num_index][0])
        self.profile_rb.set(self.profile_id[set_num_index][0])
        self.ir_range_rb.set(self.ir_range_id[set_num_index][0])
        self.fail_cb.set(self.fail_id[set_num_index])
        self.sort_cb.set(self.sort_request[set_num_index])
        profile_text = self.profile_id[set_num_index][1]
        name_text = self.name_id[set_num_index][1]
        ir_range_text = self.ir_range_id[set_num_index][1]
        NewResultsWindow(self.name_rb, self.profile_rb, self.ir_range_rb, self.fail_cb, self.sort_cb, self.sort_order, self.initial_window, self.code_check_frame,
                         self.directory, self.input_file_path, profile_text=profile_text, name_text=name_text, ir_range_text=ir_range_text).\
            new_code_result_set((0, 0), results_tree, tree_select, True)


        print(f'name spec: {self.name_id}')
        print(f'profile spec: {self.profile_id}')
        print(f'IR Range: {self.ir_range_id}')
        print(f'sort spec: {self.sort_request}')
        print(f'fail id: {self.fail_id}')
        print(f'sort order: {self.sort_order}')
        print(f'reverse: {self.reverse}')

    def delete_code_result(self, results_tree):
        for tree_selection in results_tree.selection():
            set_num = int(results_tree.set(tree_selection, column=0)) - 1
            results_tree.delete(tree_selection)
            del self.name_id[set_num]
            del self.profile_id[set_num]
            del self.code_set[set_num]
            del self.ir_range_id[set_num]
            del self.fail_id[set_num]
            del self.sort_request[set_num]
            del self.sort_order[set_num]
            del self.reverse[set_num]
            for row, item in enumerate(results_tree.get_children()):
                results_tree.set(item, column=0, value=row + 1)
        if results_tree.get_children():
            next_idd = results_tree.get_children()[0]
            results_tree.selection_set(next_idd)
        else:
            pass

    def run_code_check(self):
        file_types = [('Excel File', '*.xlsx'), ('csv Files', '*.csv')]
        output_file_path = filedialog.asksaveasfilename(filetypes=file_types, defaultextension='xlsx')
        out_format = os.path.splitext(output_file_path)[1]
        save_output.RunProgram(self.initial_window).run_code_check(output_file_path, self.code_set, out_format,
                                                                        self.input_file_path, self.name_id,
                                                                        self.profile_id, self.ir_range_id, self.fail_id,
                                                                   self.sort_request, self.sort_order, self.reverse)


class NewResultsWindow:

    def __init__(self, name_rb, profile_rb, ir_range_rb, fail_rb, sort_rb, sort_order, initial_window, code_check_frame, directory, input_file_path,
                 name_text='ALL', profile_text='ALL', ir_range_text=('MIN', 'MAX')):
        # TODO: add proper labels to sorting window
        self.profile_rb = profile_rb
        self.name_rb = name_rb
        self.initial_window = initial_window
        self.code_check_frame = code_check_frame
        self.directory = directory
        self.input_file_path = input_file_path
        self.mod_name_text = name_text
        self.mod_profile_text = profile_text
        self.mod_ir_range_text = ir_range_text
        self.ir_range_rb = ir_range_rb
        self.fail_cb = fail_rb
        self.sort_cb = sort_rb
        self.sort_order = sort_order
        self.sort_box_items = StringVar()
        self.default_box_items = StringVar()
        self.order_rb = BooleanVar()
        self.code_select_window = Toplevel(self.initial_window)
        self.sort_frame = LabelFrame(self.code_select_window, text='Sort Criteria', height=160, width=380)
        self.option_window_default = Listbox(self.sort_frame, height=5, width=15, font=('Arial', 10),
                                        listvariable=self.default_box_items)
        self.option_window_sort = Listbox(self.sort_frame, height=5, width=15, font=('Arial', 10),
                                     listvariable=self.sort_box_items)
        self.sort_button_window = Frame(self.sort_frame, width=120, height=140)
        self.asc_rb = Radiobutton(self.sort_button_window, text="Asc.", variable=self.order_rb, value=False)
        self.dec_rb = Radiobutton(self.sort_button_window, text="Dec.", variable=self.order_rb, value=True)

    def new_code_result_set(self, selection_index, results_tree, tree_selection_index, modify):
        pady = (5, 5)
        padx = (5, 5)
        self.code_select_window.geometry('400x430')
        utilities_GUI.center(self.code_select_window, x_offset=-500)
        self.code_select_window.resizable(False, False)
        self.code_select_window.grid_propagate(0)
        self.code_select_window.grab_set()
        self.default_box_items.set(('IR Value', 'Profile', 'Name'))
        if not modify:
            self.profile_rb.set("1")
            self.name_rb.set("1")
            self.ir_range_rb.set("1")
            self.sort_cb.set(False)
            self.fail_cb.set(False)
        else:
            pass

        def name_text_get(name_rb_val):
            if name_rb_val == 1:
                name_id = 'ALL'
            else:
                name_id = name_text.get('1.0', 'end-1c')
            return name_rb_val, name_id

        def profile_text_get(profile_rb_val):
            if profile_rb_val == 1:
                profile_id = 'ALL'
            else:
                profile_id = profile_text.get('1.0', 'end-1c')
            return profile_rb_val, profile_id

        def ir_text_get(ir_range_rb_val):
            if ir_range_rb_val == 1:
                ir_range_id = ('MIN', 'MAX')
            else:
                ir_range_id = (ir_range_text_min.get('1.0', 'end-1c'), ir_range_text_max.get('1.0', 'end-1c'))
            return ir_range_rb_val, ir_range_id

        def ir_range_disable(ir_range_rb_val):
            if ir_range_rb_val == 2:
                ir_range_text_min.delete('0.0', END)
                ir_range_text_min.insert('1.0', 'MIN')
                ir_range_text_min['state'] = 'disabled'
                ir_range_text_max['state'] = 'normal'
            elif ir_range_rb_val == 3:
                ir_range_text_max.delete('0.0', END)
                ir_range_text_max.insert('1.0', 'MAX')
                ir_range_text_max['state'] = 'disabled'
                ir_range_text_min['state'] = 'normal'
            else:
                ir_range_text_min['state'] = 'normal'
                ir_range_text_max['state'] = 'normal'

        def sort_window(sort_flag):
            add_button = Button(self.sort_button_window, text='Add >>', command=lambda: add_sort())
            remove_button = Button(self.sort_button_window, text='<< Remove', command=lambda: remove_sort())
            add_button['state'] = 'disabled'
            remove_button['state'] = 'disabled'

            if sort_flag.get():
                self.code_select_window.geometry('400x600')
                self.sort_frame.grid(row=6, column=0, columnspan=5, padx=padx, pady=pady)
                self.option_window_default.grid(row=0, column=0, padx=padx, pady=pady, sticky='n')
                self.option_window_sort.grid(row=0, column=4, padx=padx, pady=pady, sticky='n')
                self.sort_button_window.grid(row=0, column=1, columnspan=3, padx=padx, pady=pady, sticky='nsew')
                self.sort_frame.grid_propagate(0)
                self.sort_button_window.grid_propagate(0)
                continue_frame.grid_configure(row=7)

                add_button.grid(row=0, column=0, columnspan=2, padx=padx, pady=pady)
                remove_button.grid(row=1, column=0, columnspan=2, padx=padx, pady=pady)

                self.dec_rb.grid(row=2, column=0, padx=padx, pady=pady)
                self.asc_rb.grid(row=2, column=1, padx=padx, pady=pady)

                self.option_window_sort.bind('<<ListboxSelect>>', lambda event: on_sort_select(event, 'sort'))
                self.option_window_default.bind('<<ListboxSelect>>', lambda event: on_sort_select(event, 'default'))

            else:
                self.sort_frame.grid_remove()
                self.code_select_window.geometry('400x430')
                continue_frame.grid_configure(row=6)

            def add_sort():
                if not (self.option_window_sort.curselection() or self.option_window_default.curselection()):
                    pass
                else:
                    sort_select = self.option_window_default.get(self.option_window_default.curselection())
                    self.option_window_sort.insert('end', sort_select)
                    self.option_window_default.delete(self.option_window_default.curselection())

            def remove_sort():
                if not (self.option_window_sort.curselection() or self.option_window_default.curselection()):
                    pass
                else:
                    sort_select = self.option_window_sort.get(self.option_window_sort.curselection())
                    self.option_window_default.insert('end', sort_select)
                    self.option_window_sort.delete(self.option_window_sort.curselection())

            def on_sort_select(event, name):
                print(name)
                print(event.widget.curselection())
                if name == 'sort' and event.widget.curselection():
                    add_button['state'] = 'disabled'
                    remove_button['state'] = 'enabled'
                elif name == 'default' and event.widget.curselection():
                    add_button['state'] = 'enabled'
                    remove_button['state'] = 'disabled'
                else:
                    print('something else')

        def text_return():
            return 'break'

        new_result_set_header = Label(self.code_select_window, text="Code Check Results Parameter Selection")
        profile_select = LabelFrame(self.code_select_window, text='PROFILE(s)', height=90, width=380)
        name_select = LabelFrame(self.code_select_window, text='BEAMS(s)', height=90, width=380)
        ir_range = LabelFrame(self.code_select_window, text='IR Range', height=90, width=380)
        misc_frame = LabelFrame(self.code_select_window, text='Misc Options', height=50, width=380)
        continue_frame = Frame(self.code_select_window, height=50, width=380)

        new_result_set_header.grid(row=0, column=0, columnspan=6, padx=padx, pady=pady)
        profile_select.grid(row=2, column=0, columnspan=5, padx=padx, pady=pady)
        name_select.grid(row=3, column=0, columnspan=5, padx=padx, pady=pady)
        ir_range.grid(row=4, column=0, columnspan=5, padx=padx, pady=pady)
        misc_frame.grid(row=5, column=0, columnspan=5, padx=padx, pady=pady)
        continue_frame.grid(row=6, column=0, columnspan=6, pady=pady, padx=padx, sticky='se')

        profile_select.grid_propagate(0)
        name_select.grid_propagate(0)
        ir_range.grid_propagate(0)
        misc_frame.grid_propagate(0)

        fail_cb = Checkbutton(misc_frame, text='Only Failed Members', variable=self.fail_cb)
        sort_cb = Checkbutton(misc_frame, text='Sort (Y/N)?', variable=self.sort_cb, onvalue=True, offvalue=False)
        sort_cb.configure(command=lambda: sort_window(self.sort_cb))

        fail_cb.grid(row=0, column=0)
        sort_cb.grid(row=0, column=1)

        profile_all_rb = Radiobutton(profile_select, text='ALL', variable=self.profile_rb, value=1)
        profile_sta_wth_rb = Radiobutton(profile_select, text='STARTS WITH', variable=self.profile_rb, value=2)
        profile_end_wth_rb = Radiobutton(profile_select, text='ENDS WITH', variable=self.profile_rb, value=3)
        profile_contains_rb = Radiobutton(profile_select, text='CONTAINS', variable=self.profile_rb, value=4)
        profile_list_rb = Radiobutton(profile_select, text='LIST', variable=self.profile_rb, value=5)
        profile_text = Text(profile_select, height=1, width=50, font=('Arial', 10), wrap=NONE)
        profile_scrollx = Scrollbar(profile_select)
        profile_scrollx.configure(command=profile_text.xview, orient=HORIZONTAL)
        utilities_GUI.CreateToolTip(profile_text, f'Do not use single or double quotes around text entries.'
                                               f' All list entries must be separated by a comma and space'
                                               f' (example: W10x45, W8x17, W24x45)')

        profile_all_rb.grid(row=0, column=0)
        profile_sta_wth_rb.grid(row=0, column=1)
        profile_end_wth_rb.grid(row=0, column=2)
        profile_contains_rb.grid(row=0, column=3)
        profile_list_rb.grid(row=0, column=4)
        profile_text.grid(row=1, column=0, columnspan=5, sticky='nw', pady=5, padx=5)
        profile_scrollx.grid(row=2, column=0, columnspan=5, sticky='ew')

        profile_text.configure(xscrollcommand=profile_scrollx.set)
        profile_text.config(state='normal')
        profile_text.insert('1.0', 'ALL')
        profile_text.bind('<Return>', lambda event, : text_return())

        name_all_rb = Radiobutton(name_select, text='ALL', variable=self.name_rb, value=1)
        name_sta_wth_rb = Radiobutton(name_select, text='STARTS WITH', variable=self.name_rb, value=2)
        name_end_wth_rb = Radiobutton(name_select, text='ENDS WITH', variable=self.name_rb, value=3)
        name_contains_rb = Radiobutton(name_select, text='CONTAINS', variable=self.name_rb, value=4)
        name_list_rb = Radiobutton(name_select, text='LIST', variable=self.name_rb, value=5)
        name_text = Text(name_select, height=1, width=50, font=('Arial', 10), wrap=NONE)
        name_scrollx = Scrollbar(name_select)
        name_scrollx.configure(command=name_text.xview, orient=HORIZONTAL)
        utilities_GUI.CreateToolTip(name_text, f'Do not use single or double quotes around text entries.'
                                               f' All list entries must be separated by a comma and space'
                                               f' (example: Beam1, Beam2)')

        name_all_rb.grid(row=0, column=0)
        name_sta_wth_rb.grid(row=0, column=1)
        name_end_wth_rb.grid(row=0, column=2)
        name_contains_rb.grid(row=0, column=3)
        name_list_rb.grid(row=0, column=4)
        name_text.grid(row=1, column=0, columnspan=5, sticky='nw', pady=5, padx=5)
        name_scrollx.grid(row=2, column=0, columnspan=5, sticky='ew')

        name_text.configure(xscrollcommand=name_scrollx.set)
        name_text.config(state='normal')
        name_text.insert('1.0', 'ALL')
        name_text.bind('<Return>', lambda event, : text_return())

        ir_all_rb = Radiobutton(ir_range, text='ALL', variable=self.ir_range_rb, value=1)
        ir_less_than_rb = Radiobutton(ir_range, text='LESS THAN', variable=self.ir_range_rb, value=2)
        ir_greater_than_rb = Radiobutton(ir_range, text='GREATER THAN', variable=self.ir_range_rb, value=3)
        ir_between_rb = Radiobutton(ir_range, text='BETWEEN', variable=self.ir_range_rb, value=4)

        ir_all_rb.configure(command=lambda: ir_range_disable(self.ir_range_rb.get()))
        ir_less_than_rb.configure(command=lambda: ir_range_disable(self.ir_range_rb.get()))
        ir_greater_than_rb.configure(command=lambda: ir_range_disable(self.ir_range_rb.get()))
        ir_between_rb.configure(command=lambda: ir_range_disable(self.ir_range_rb.get()))

        ir_all_rb.grid(row=0, column=0)
        ir_less_than_rb.grid(row=0, column=1)
        ir_greater_than_rb.grid(row=0, column=2)
        ir_between_rb.grid(row=0, column=3)

        ir_range_text_min = Text(ir_range, height=1, width=10, font=('Arial', 10), wrap=NONE)
        ir_range_text_max = Text(ir_range, height=1, width=10, font=('Arial', 10), wrap=NONE)
        ir_range_text_min.grid(row=1, column=1, columnspan=5, sticky='nw', pady=5, padx=5)
        ir_range_text_max.grid(row=1, column=3, columnspan=5, sticky='nw', pady=5, padx=5)

        Label(ir_range, text='Min:').grid(row=1, column=0, pady=5, padx=5)
        Label(ir_range, text='Max:').grid(row=1, column=2, pady=5, padx=5)

        ir_range_text_min.config(state='normal')
        ir_range_text_min.insert('1.0', 'MIN')
        ir_range_text_min.bind('<Return>', lambda event,: text_return())

        ir_range_text_max.config(state='normal')
        ir_range_text_max.insert('1.0', 'MAX')
        ir_range_text_max.bind('<Return>', lambda event,: text_return())

        if modify:
            name_text.delete('0.0', END)
            profile_text.delete('0.0', END)
            ir_range_text_max.delete('0.0', END)
            ir_range_text_min.delete('0.0', END)
            name_text.insert('1.0', self.mod_name_text)
            profile_text.insert('1.0', self.mod_profile_text)
            ir_range_text_min.insert('1.0', self.mod_ir_range_text[0])
            ir_range_text_max.insert('1.0', self.mod_ir_range_text[1])
            sort_window(self.sort_cb)

        store_button = Button(continue_frame, text="Store",
                              command=lambda: CodeCheckFrame(self.code_check_frame, self.initial_window,
                                                             self.directory, self.input_file_path, modify).
                              store_code_check_info(self.code_select_window,
                                                    profile_text_get(self.profile_rb.get()), name_text_get(self.name_rb.get())
                                                    , selection_index,
                                                    results_tree, tree_selection_index, ir_text_get(self.ir_range_rb.get()), self.fail_cb.get(), self.sort_cb.get(), self.option_window_sort.get('0', END), self.order_rb.get()))
        cancel_button = Button(continue_frame, text="Cancel", command=lambda: self.code_select_window.destroy())

        store_button.grid(row=0, column=2, padx=5, pady=5)
        cancel_button.grid(row=0, column=1, padx=5, pady=5)

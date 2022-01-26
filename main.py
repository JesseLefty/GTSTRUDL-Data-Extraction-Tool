from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import os
import generate_mem_array_info
import save_output


def help():
    # open some help documentation
    pass


class FirstWindow:

    def __init__(self):
        pass

    def select_dir(self, show_dir):
        global directory
        directory = filedialog.askdirectory()
        show_dir.config(state='normal')
        show_dir.insert(END, directory)
        show_dir.config(state='disabled')

    def select_file(self, show_file):
        global input_file
        file_types = [('*.gto - GTSTRUDL Output', '*.gto'), ('*.txt - Text Files', '*.txt'),
                      ('*.csv - Comma Separated Values', '*.csv'), ('*.* - All types', '*.*')]
        input_file = filedialog.askopenfilename(initialdir=directory, title="select file", filetypes=file_types)
        input_file = os.path.basename(input_file)
        show_file.config(state='normal')
        show_file.insert(END, input_file)
        show_file.config(state='disabled')

    def landing_window_display(self, root):
        root.title("GTstrudl Extractor")
        root.geometry('600x400')
        program_description_frame = Frame(root, height=380, width=180)
        program_title = Label(program_description_frame, text='GTstrudl Extractor', font=('Helvetica', 12))
        program_description = Label(program_description_frame, text='GTstrudl Extractor was developed\n'
                                                                    'to facilitate parsing analysis\n'
                                                                    'results from a GTStrudl analysis\n'
                                                                    'using the .gto file. This program\n'
                                                                    'allows the selection of specific\n'
                                                                    'requested data contained within\n'
                                                                    'the .gto file to be exported to\n'
                                                                    'a .csv file or .xlsx file which\n'
                                                                    'can be easily used to develop\n'
                                                                    'calculations or reports.')
        program_version = Label(program_description_frame, text='Version: 0.0.2')
        program_developer = Label(program_description_frame, text='Developed by Jesse Wagoner')
        program_dev_date = Label(program_description_frame, text='12/11/2021')
        program_description_frame.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky='nsew')
        program_description_frame.grid_propagate(0)
        program_title.grid(row=0, column=0)
        program_version.grid(row=1, column=0)
        program_developer.grid(row=2, column=0)
        program_dev_date.grid(row=3, column=0)
        program_description.grid(row=4, column=0)

        banner = Frame(root, height=110, width=390)
        banner.grid(row=0, column=1, pady=(10, 5), padx=(0, 10), sticky='n')
        banner_text = Label(banner, text='Future Banner Of Some Sort')
        banner_text.grid(row=0, column=0, sticky='n')
        banner.grid_propagate(0)

        set_directory_frame = LabelFrame(root, text='Select Directory & File', height=190, width=390)
        set_directory_frame.grid(row=1, column=1, pady=(5, 5), padx=(0, 10), sticky='n')
        dir_label = Label(set_directory_frame, text='Select working directory.\n'
                                                    '(default save location for all files)')
        dir_label.grid(row=0, column=0, columnspan=1, pady=5, padx=5, sticky='nw')
        set_directory_frame.grid_propagate(0)
        show_dir = Text(set_directory_frame, height=1, width=50, font=('Arial', 10), xscrollcommand=True)
        show_dir.grid(row=1, column=0, columnspan=2, sticky='nw')
        show_dir.config(state='disabled')

        show_file = Text(set_directory_frame, height=1, width=50, font=('Arial', 10), xscrollcommand=True)
        show_file.grid(row=3, column=0, columnspan=2, sticky='nw')
        show_file.config(state='disabled')

        select_file = Label(set_directory_frame, text='Select .gto file to parse')
        select_file.grid(row=2, column=0, pady=10, sticky='nw')

        continue_frame = Frame(root, height=60, width=390)
        continue_frame.grid(row=2, column=1, pady=(5, 10), padx=(0, 10), sticky='se')

        exit_button = Button(continue_frame, text="Exit", command=root.quit)
        exit_button.grid(row=0, column=1, padx=5, pady=5)
        help_button = Button(continue_frame, text='Help (?)', command=help)
        help_button.grid(row=0, column=0, padx=5, pady=5)
        dir_open = Button(set_directory_frame, text="Select New", command=lambda: FirstWindow().select_dir(show_dir))
        dir_open.grid(row=0, column=1, pady=5, padx=0, sticky='ne')
        dir_open = Button(set_directory_frame, text="Select File", command=lambda: FirstWindow().select_file(show_file))
        dir_open.grid(row=2, column=1, pady=10, padx=0, sticky='ne')
        continue_button = Button(continue_frame, text='Continue', command=SecondWindow().open_second_window)
        continue_button.grid(row=0, column=2, padx=5, pady=5)


class SecondWindow:

    def __init__(self):
        pass

    window_open = False
    replace = False
    delete = False
    sel_rlist = "none"
    joint = []
    load_id = []
    member_set = []
    beam_id = []

    def open_second_window(self):
        self.joint.clear()
        self.load_id.clear()
        self.beam_id.clear()
        self.member_set.clear()
        member_force_list, file_as_list = generate_mem_array_info.GenerateDisplayData(input_file).get_force_display()
        available_results_list = StringVar(value=member_force_list)
        result_tree_headings = ['Set #', 'Set Name', 'Joint Spec.', 'Load Spec.', 'Beam Spec.']
        out_format_rb = BooleanVar()

        initial_window.withdraw()
        member_force_window = Toplevel(initial_window)
        member_force_window.geometry('600x400')
        member_force_window.grid_propagate(0)

        def on_list_select(event):
            new_mem_result_set['state'] = 'enabled'
            modify_force_result['state'] = 'disabled'
            delete_force_result['state'] = 'disabled'

        def on_tree_select(event):
            modify_force_result['state'] = 'enabled'
            delete_force_result['state'] = 'enabled'
            new_mem_result_set['state'] = 'disabled'

        def list_select():
            selection_index = int(available_result_box.curselection()[0])
            stored_value = available_result_box.get(selection_index)

            return selection_index, stored_value

        def tree_select():
            if modify_force_result['state'] == 'enabled':
                tree_selection_index = results_tree.selection()[0]
            else:
                tree_selection_index = 0
            return int(tree_selection_index)

        temp_header = Label(member_force_window, text="Member Force Extraction")
        result_set_frame = LabelFrame(member_force_window, text='Available Member Results', height=160, width=420)
        display_result_set_frame = LabelFrame(member_force_window, text='Requested Results', height=135, width=580)
        button_frame = Frame(member_force_window, height=160, width=150)
        output_format_frame = LabelFrame(member_force_window, text='Output Format', height=30, width=100)
        continue_frame = Frame(member_force_window, height=30, width=280)

        temp_header.grid(row=0, column=0, columnspan=1, padx=10, pady=(5, 0))
        result_set_frame.grid(row=1, column=1, padx=(0, 10), pady=(5, 0), sticky='nw')
        display_result_set_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=(5, 0), sticky='nsew')
        button_frame.grid(row=1, column=0, padx=10, pady=(5, 0))
        output_format_frame.grid(row=3, column=0, pady=(5, 10), padx=(10, 0), sticky='nw')
        continue_frame.grid(row=3, column=0, columnspan=3, pady=(5, 10), padx=(0, 10), sticky='se')

        result_set_frame.grid_propagate(0)
        display_result_set_frame.grid_propagate(0)
        button_frame.grid_propagate(0)

        available_result_box = Listbox(result_set_frame, listvariable=available_results_list, height=8, width=65)
        list_yscroll = Scrollbar(result_set_frame)
        list_xscroll = Scrollbar(result_set_frame)
        list_xscroll.configure(command=available_result_box.xview, orient=HORIZONTAL)
        list_yscroll.configure(command=available_result_box.yview, orient=VERTICAL)
        available_result_box.configure(xscrollcommand=list_xscroll.set, yscrollcommand=list_yscroll.set)
        list_yscroll.pack(side=RIGHT, fill=Y)
        list_xscroll.pack(side=BOTTOM, fill=X)
        available_result_box.pack(side=LEFT, expand=True)
        available_result_box.bind('<<ListboxSelect>>', on_list_select)

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
                                    command=lambda: self.new_mem_result_set(list_select(), results_tree, tree_select()))
        load_exist_mem_result_set = Button(button_frame, text="Load Existing",
                                           command=lambda: self.load_existing_mem_result_set())
        modify_force_result = Button(button_frame, text='Modify Result',
                                     command=lambda: self.modify_force_result(list_select(), results_tree,
                                                                              tree_select()))
        delete_force_result = Button(button_frame, text='Delete Result',
                                     command=lambda: self.delete_force_result(results_tree))

        new_mem_result_set.grid(row=2, column=0, padx=5, pady=5)
        load_exist_mem_result_set.grid(row=3, column=0, padx=5, pady=5)
        modify_force_result.grid(row=4, column=0, padx=5, pady=5)
        delete_force_result.grid(row=5, column=0, padx=5, pady=5)

        new_mem_result_set['state'] = 'disabled'
        modify_force_result['state'] = 'disabled'
        delete_force_result['state'] = 'disabled'

        csv_rb = Radiobutton(output_format_frame, text='.csv', variable=out_format_rb, value=False)
        xlsx_rb = Radiobutton(output_format_frame, text='.xlsx', variable=out_format_rb, value=True)

        csv_rb.grid(row=0, column=0, padx=10, pady=5)
        xlsx_rb.grid(row=0, column=1, padx=10, pady=5)

        generate_button = Button(continue_frame, text="Generate",
                                 command=lambda: SecondWindow().run_member_forces(file_as_list, self.joint,
                                                                                  out_format_rb.get()))
        back_button = Button(continue_frame, text="Back", command=lambda: [initial_window.deiconify(),
                                                                           member_force_window.destroy()])
        help_button = Button(continue_frame, text='Help (?)', command=help)

        generate_button.grid(row=0, column=2, padx=5, pady=5)
        back_button.grid(row=0, column=1, padx=5, pady=5)
        help_button.grid(row=0, column=0, padx=5, pady=5)

    def new_mem_result_set(self, selection_index, results_tree, tree_selection_index):
        jt_rb = StringVar()
        load_rb = IntVar()
        beam_rb = IntVar()
        jt_rb.set('ALL')
        load_rb.set("1")
        beam_rb.set("1")

        force_select_window = Toplevel(initial_window)
        force_select_window.geometry('400x400')
        force_select_window.grid_propagate(0)

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

        jt_all_rb = Radiobutton(joint_select, text='ALL', variable=jt_rb, value='ALL')
        jt_sta_rb = Radiobutton(joint_select, text='START', variable=jt_rb, value='START')
        jt_end_rb = Radiobutton(joint_select, text='END', variable=jt_rb, value='END')

        jt_all_rb.grid(row=0, column=0)
        jt_sta_rb.grid(row=0, column=1)
        jt_end_rb.grid(row=0, column=2)

        load_all_rb = Radiobutton(load_select, text='ALL', variable=load_rb, value=1)
        load_sta_wth_rb = Radiobutton(load_select, text='STARTS WITH', variable=load_rb, value=2)
        load_end_wth_rb = Radiobutton(load_select, text='ENDS WITH', variable=load_rb, value=3)
        load_contains_rb = Radiobutton(load_select, text='CONTAINS', variable=load_rb, value=4)
        load_list_rb = Radiobutton(load_select, text='LIST', variable=load_rb, value=5)
        load_text = Text(load_select, height=1, width=50, font=('Arial', 10))

        load_all_rb.grid(row=0, column=0)
        load_sta_wth_rb.grid(row=0, column=1)
        load_end_wth_rb.grid(row=0, column=2)
        load_contains_rb.grid(row=0, column=3)
        load_list_rb.grid(row=0, column=4)
        load_text.grid(row=1, column=0, columnspan=5, sticky='nw', pady=5, padx=5)
        load_text.config(state='normal')

        beam_all_rb = Radiobutton(beam_select, text='ALL', variable=beam_rb, value=1)
        beam_sta_wth_rb = Radiobutton(beam_select, text='STARTS WITH', variable=beam_rb, value=2)
        beam_end_wth_rb = Radiobutton(beam_select, text='ENDS WITH', variable=beam_rb, value=3)
        beam_contains_rb = Radiobutton(beam_select, text='CONTAINS', variable=beam_rb, value=4)
        beam_list_rb = Radiobutton(beam_select, text='LIST', variable=beam_rb, value=5)
        beam_text = Text(beam_select, height=1, width=50, font=('Arial', 10))

        beam_all_rb.grid(row=0, column=0)
        beam_sta_wth_rb.grid(row=0, column=1)
        beam_end_wth_rb.grid(row=0, column=2)
        beam_contains_rb.grid(row=0, column=3)
        beam_list_rb.grid(row=0, column=4)
        beam_text.grid(row=1, column=0, columnspan=5, sticky='nw', pady=5, padx=5)
        beam_text.config(state='normal')

        store_button = Button(continue_frame, text="Store",
                              command=lambda: self.store_member_force_info(force_select_window, jt_rb.get(),
                                                                           beam_text_get(beam_rb.get()),
                                                                           load_text_get(load_rb.get()),
                                                                           selection_index[0], selection_index[1],
                                                                           results_tree, tree_selection_index))
        cancel_button = Button(continue_frame, text="Cancel", command=lambda: force_select_window.destroy())
        help_button = Button(continue_frame, text='Help (?)', command=help)

        store_button.grid(row=0, column=2, padx=5, pady=5)
        cancel_button.grid(row=0, column=1, padx=5, pady=5)
        help_button.grid(row=0, column=0, padx=5, pady=5)

    def store_member_force_info(self, force_select_window, joint, beam_id_tpl, load_id_tpl, selection_index,
                                stored_value, results_tree, tree_select):
        force_select_window.destroy()
        key = [1, 2, 3, 4, 5]
        value = ['', 'Starts With: ', 'Ends With: ', 'Contains: ', 'List: ']
        d_tree = {}

        for row, item in enumerate(key):
            d_tree[key[row]] = value[row]

        if tree_select == 0:
            tree_selection = 0
        else:
            tree_selection = int(results_tree.selection()[0])

        if self.replace:
            set_name = results_tree.set(tree_selection, column=1)
            set_num_index = results_tree.set(tree_selection, column=0) - 1
            self.replace = False
            self.joint[set_num_index] = joint
            self.load_id[set_num_index] = load_id_tpl
            self.beam_id[set_num_index] = beam_id_tpl
            results_tree.item(tree_selection, values=(tree_selection, set_name, joint,
                                                      f'{d_tree[load_id_tpl[0]]} {load_id_tpl[1]}',
                                                      f'{d_tree[beam_id_tpl[0]]} {beam_id_tpl[1]}'))
        else:
            self.load_id.append(load_id_tpl)
            self.joint.append(joint)
            self.beam_id.append(beam_id_tpl)
            self.member_set.append(selection_index)
            tree_length = len(results_tree.get_children()) + 1

            if not results_tree.exists(tree_length):
                results_tree.insert(parent='', index='end', iid=tree_length, text=stored_value,
                                    values=(tree_length, stored_value, joint,
                                            f'{d_tree[load_id_tpl[0]]} {load_id_tpl[1]}',
                                            f'{d_tree[beam_id_tpl[0]]} {beam_id_tpl[1]}'))
            else:
                results_tree.insert(parent='', index=tree_length + 1, iid=tree_length + 1, text=stored_value,
                                    values=(tree_length, stored_value, joint,
                                            f'{d_tree[load_id_tpl[0]]} {load_id_tpl[1]}',
                                            f'{d_tree[beam_id_tpl[0]]} {beam_id_tpl[1]}'))

        for row, item in enumerate(results_tree.get_children()):
            results_tree.set(item, column=0, value=row + 1)

    def load_existing_mem_result_set(self):
        # need to generate a config file of all requested data which will be read into the program though this
        # function
        pass

    def modify_force_result(self, selection_index, results_tree, tree_select):
        self.new_mem_result_set(selection_index, results_tree, tree_select)
        self.replace = True

    def delete_force_result(self, results_tree):
        tree_selection = int(results_tree.selection()[0]) - 1
        del self.joint[tree_selection]
        del self.load_id[tree_selection]
        del self.beam_id[tree_selection]
        del self.member_set[tree_selection]
        results_tree.delete(tree_selection + 1)
        for row, item in enumerate(results_tree.get_children()):
            results_tree.set(item, column=0, value=row + 1)

    def run_member_forces(self, file_as_list, joint, out_format):
        output_file_name = 'member_forces'
        save_output.run_program(output_file_name, joint, self.member_set, out_format, input_file, file_as_list,
                                self.beam_id, self.load_id)


if __name__ == '__main__':
    initial_window = Tk()
    FirstWindow().landing_window_display(initial_window)
    initial_window.mainloop()

from tkinter import *
from tkinter.ttk import *
import error_handling
import utilities_GUI
import config
from data_storage import ResultsParameters
from process_data import ProcessData


class ResultsSelectionWindow:

    def __init__(self, tab_name, initial_window, modify=False, selection_idd=0, selected_result=(0, 'None'),
                 selected_results_tree=None):
        self.tab_name = tab_name
        self.initial_window = initial_window
        self.modify = modify
        self.selection_idd = selection_idd
        self.selected_result = selected_result
        self.set_num_selected = selected_result[0]
        self.set_name_selected = selected_result[1]
        self.selected_results_tree = selected_results_tree
        self.results = ResultsParameters(self.tab_name)
        self.jt_rb = StringVar(value='ALL')
        self.first_rb = IntVar(value=1)
        self.second_rb = IntVar(value=1)
        self.sort_box_items = StringVar()
        self.default_box_items = StringVar()
        self.order_rb = BooleanVar(value=False)
        self.sort_cb = BooleanVar(value=False)
        self.fail_cb = BooleanVar(value=False)
        self.ir_range_rb = IntVar(value=1)
        self.sort_order_dict = {'IR Value': 5, 'Name': 0, 'Profile': 8}
        self.set_num = self.results.results_parameters['Set Index']
        self.set_name = self.results.results_parameters['Set Name']
        if self.modify:
            self.first_rb.set(self.results.results_parameters['Name'][self.selection_idd][0])
            self.mod_first_text = self.results.results_parameters['Name'][self.selection_idd][1]
            if self.tab_name == 'Member Force':
                self.jt_rb.set(self.results.results_parameters['Joint'][self.selection_idd])
                self.second_rb.set(self.results.results_parameters['Load'][self.selection_idd][0])
                self.mod_second_text = self.results.results_parameters['Load'][self.selection_idd][1]
            elif self.tab_name == 'Joint Reaction':
                self.second_rb.set(self.results.results_parameters['Load'][self.selection_idd][0])
                self.mod_second_text = self.results.results_parameters['Load'][self.selection_idd][1]
            else:
                self.second_rb.set(self.results.results_parameters['Profile'][self.selection_idd][0])
                self.mod_second_text = self.results.results_parameters['Profile'][self.selection_idd][1]
                self.mod_ir_range_text = self.results.results_parameters['IR Range'][self.selection_idd][1]
                self.ir_range_rb.set(self.results.results_parameters['IR Range'][self.selection_idd][0])
                self.fail_cb.set(self.results.results_parameters['Fail'][self.selection_idd])
                self.sort_cb.set(self.results.results_parameters['Sort'][self.selection_idd])
                self.sort_order = self.results.results_parameters['Sort Order'][self.selection_idd]
                self.reverse = self.results.results_parameters['Reverse'][self.selection_idd]
        else:
            self.selection_idd = len(self.selected_results_tree.get_children())

        if self.tab_name == 'Member Force':
            self.joint = self.results.results_parameters['Joint']
            self.name = self.results.results_parameters['Name']
            self.load = self.results.results_parameters['Load']
        elif self.tab_name == 'Joint Reaction':
            self.name = self.results.results_parameters['Name']
            self.load = self.results.results_parameters['Load']
        else:
            self.name = self.results.results_parameters['Name']

        self.padx, self.pady = (5, 5), (5, 5)
        text_labels = config.requested_results_headings[self.tab_name]
        rb_text = ['ALL', 'STARTS WITH', 'ENDS WITH', 'CONTAINS', 'LIST']
        self.selection_window = Toplevel(self.initial_window)
        self.selection_window.geometry('400x360')
        utilities_GUI.center(self.selection_window, x_offset=-500)
        self.selection_window.resizable(False, False)
        self.selection_window.grid_propagate(0)
        self.selection_window.grab_set()
        new_result_set_header = Label(self.selection_window, text=f'{self.tab_name} Results Parameter Selection')
        first_select = LabelFrame(self.selection_window, text=text_labels['text label'][0], height=100, width=380)
        second_select = LabelFrame(self.selection_window, text=text_labels['text label'][1], height=100, width=380)
        self.continue_frame = Frame(self.selection_window, height=60, width=380)

        new_result_set_header.grid(row=0, column=0, columnspan=6, padx=self.padx, pady=self.pady)
        first_select.grid(row=1, column=0, columnspan=5, padx=self.padx, pady=self.pady)
        second_select.grid(row=2, column=0, columnspan=5, padx=self.padx, pady=self.pady)
        self.continue_frame.grid(row=4, column=0, columnspan=6, pady=self.pady, padx=self.padx, sticky='se')

        first_select.grid_propagate(0)
        second_select.grid_propagate(0)

        for val, text in enumerate(rb_text, start=1):
            first_rb = Radiobutton(first_select, text=text, variable=self.first_rb, value=val)
            first_rb.grid(row=0, column=val - 1)
            second_rb = Radiobutton(second_select, text=text, variable=self.second_rb, value=val)
            second_rb.grid(row=0, column=val - 1)

        self.first_text = Text(first_select, height=1, width=50, font=('Arial', 10), wrap=NONE)
        first_scrollx = Scrollbar(first_select)
        first_scrollx.configure(command=self.first_text.xview, orient=HORIZONTAL)
        utilities_GUI.CreateToolTip(self.first_text, 'List entries must be separated by comma (item1, item2, item3)')
        self.first_text.grid(row=1, column=0, columnspan=5, sticky='nw', pady=5, padx=5)
        first_scrollx.grid(row=2, column=0, columnspan=5, sticky='ew')
        self.first_text.configure(xscrollcommand=first_scrollx.set)
        self.first_text.config(state='normal')

        self.second_text = Text(second_select, height=1, width=50, font=('Arial', 10), wrap=NONE)
        second_scrollx = Scrollbar(second_select)
        second_scrollx.configure(command=self.second_text.xview, orient=HORIZONTAL)
        utilities_GUI.CreateToolTip(self.second_text, 'List entries must be separated by comma (item1, item2, item3)')

        self.second_text.grid(row=1, column=0, columnspan=5, sticky='nw', pady=5, padx=5)
        second_scrollx.grid(row=2, column=0, columnspan=5, sticky='ew')

        self.second_text.configure(xscrollcommand=second_scrollx.set)
        self.second_text.config(state='normal')

        self.store_button = Button(self.continue_frame, text="Store")

        cancel_button = Button(self.continue_frame, text="Cancel", command=lambda: self.selection_window.destroy())

        self.store_button.grid(row=0, column=2, padx=5, pady=5)
        cancel_button.grid(row=0, column=1, padx=5, pady=5)

        if self.modify:
            self.first_text.insert('1.0', self.mod_first_text)
            self.second_text.insert('1.0', self.mod_second_text)
        else:
            self.first_text.insert('1.0', 'ALL')
            self.second_text.insert('1.0', 'ALL')

        if self.tab_name == "Member Force":
            self.mem_force_window()

        elif self.tab_name == 'Joint Reaction':
            self.joint_reaction_window()

        else:
            self.code_check_window()

    def get_text(self, rb_val, text_val):
        if rb_val == 1:
            beam_id = 'ALL'
        else:
            beam_id = text_val.get('1.0', 'end-1c')
        return rb_val, beam_id

    def mem_force_window(self):
        joint_select = LabelFrame(self.selection_window, text='JOINT', height=50, width=380)
        joint_select.grid(row=3, column=0, padx=self.padx, pady=self.pady)
        joint_select.grid_propagate(0)
        joint_rb_text = ['ALL', 'START', 'END']
        for val, text in enumerate(joint_rb_text):
            jt_all_rb = Radiobutton(joint_select, text=text, variable=self.jt_rb, value=text)
            jt_all_rb.grid(row=0, column=val)

        self.store_button.configure(command=lambda: (
            ProcessData(self.tab_name, self.selection_idd, modify=self.modify,
                        selected_results_tree=self.selected_results_tree).store_results(
                self.get_text(self.first_rb.get(), self.first_text),
                self.get_text(self.second_rb.get(), self.second_text),
                self.jt_rb.get(), selected_result=self.selected_result),
            self.selection_window.destroy()))

    def joint_reaction_window(self):
        self.selection_window.geometry('400x300')
        self.store_button.configure(command=lambda: (
            ProcessData(self.tab_name, self.selection_idd, modify=self.modify,
                        selected_results_tree=self.selected_results_tree).store_results(
                self.get_text(self.first_rb.get(), self.first_text),
                self.get_text(self.second_rb.get(), self.second_text),
                self.jt_rb.get(), selected_result=self.selected_result),
            self.selection_window.destroy()))

    def code_check_window(self):
        self.selection_window.geometry('400x460')
        self.continue_frame.grid(row=6)
        self.default_box_items.set(('IR Value', 'Profile', 'Name'))
        ir_range = LabelFrame(self.selection_window, text='IR Range', height=90, width=380)
        misc_frame = LabelFrame(self.selection_window, text='Misc Options', height=50, width=380)

        ir_range.grid(row=4, column=0, columnspan=5, padx=self.padx, pady=self.pady)
        misc_frame.grid(row=5, column=0, columnspan=5, padx=self.padx, pady=self.pady)

        ir_range.grid_propagate(0)
        misc_frame.grid_propagate(0)

        fail_cb = Checkbutton(misc_frame, text='Only Failed Members', variable=self.fail_cb)
        sort_cb = Checkbutton(misc_frame, text='Sort (Y/N)?', variable=self.sort_cb, onvalue=True, offvalue=False)
        sort_cb.configure(command=lambda: sort_window(self.sort_cb))

        fail_cb.grid(row=0, column=0)
        sort_cb.grid(row=0, column=1)

        sort_frame = LabelFrame(self.selection_window, text='Sort Criteria', height=160, width=380)
        option_window_default = Listbox(sort_frame, height=5, width=15, font=('Arial', 10),
                                        listvariable=self.default_box_items)
        option_window_sort = Listbox(sort_frame, height=5, width=15, font=('Arial', 10),
                                     listvariable=self.sort_box_items)
        sort_button_window = Frame(sort_frame, width=120, height=140)
        asc_rb = Radiobutton(sort_button_window, text="Asc.", variable=self.order_rb, value=False)
        dec_rb = Radiobutton(sort_button_window, text="Dec.", variable=self.order_rb, value=True)

        ir_range_text = ['ALL', 'LESS THAN', 'GREATER THAN', 'BETWEEN']
        for val, text in enumerate(ir_range_text, start=1):
            ir_all_rb = Radiobutton(ir_range, text=text, variable=self.ir_range_rb, value=val)
            ir_all_rb.configure(command=lambda: ir_range_disable(self.ir_range_rb.get()))
            ir_all_rb.grid(row=0, column=val - 1)

        ir_range_text_min = Text(ir_range, height=1, width=10, font=('Arial', 10), wrap=NONE)
        ir_range_text_max = Text(ir_range, height=1, width=10, font=('Arial', 10), wrap=NONE)
        ir_range_text_min.grid(row=1, column=1, columnspan=5, sticky='nw', pady=5, padx=5)
        ir_range_text_max.grid(row=1, column=3, columnspan=5, sticky='nw', pady=5, padx=5)

        Label(ir_range, text='Min:').grid(row=1, column=0, pady=5, padx=5)
        Label(ir_range, text='Max:').grid(row=1, column=2, pady=5, padx=5)

        ir_range_text_min.config(state='normal')
        ir_range_text_min.insert('1.0', 'MIN')

        ir_range_text_max.config(state='normal')
        ir_range_text_max.insert('1.0', 'MAX')

        self.store_button.configure(command=lambda: (sort_window_get(),
                                                     ProcessData(self.tab_name, self.selection_idd,
                                                                 modify=self.modify, selected_results_tree=self.selected_results_tree).store_results(
                                                         self.get_text(self.first_rb.get(), self.first_text),
                                                         self.get_text(self.second_rb.get(), self.second_text),
                                                         selected_result=self.selected_result,
                                                         ir_range=ir_text_get(self.ir_range_rb.get()),
                                                         sort=self.sort_cb.get(), fail=self.fail_cb.get(),
                                                         sort_order=self.sort_order, reverse=self.reverse),
                                                     self.selection_window.destroy()))

        def sort_window(sort_flag):
            add_button = Button(sort_button_window, text='Add >>', command=lambda: add_sort())
            remove_button = Button(sort_button_window, text='<< Remove', command=lambda: remove_sort())
            add_button['state'] = 'disabled'
            remove_button['state'] = 'disabled'

            if sort_flag.get():
                self.selection_window.geometry('400x630')
                sort_frame.grid(row=6, column=0, columnspan=5, padx=self.padx, pady=self.pady)
                option_window_default.grid(row=0, column=0, padx=self.padx, pady=self.pady, sticky='n')
                option_window_sort.grid(row=0, column=4, padx=self.padx, pady=self.pady, sticky='n')
                sort_button_window.grid(row=0, column=1, columnspan=3, padx=self.padx, pady=self.pady, sticky='nsew')
                sort_frame.grid_propagate(0)
                sort_button_window.grid_propagate(0)
                self.continue_frame.grid_configure(row=7)

                add_button.grid(row=0, column=0, columnspan=2, padx=self.padx, pady=self.pady)
                remove_button.grid(row=1, column=0, columnspan=2, padx=self.padx, pady=self.pady)

                dec_rb.grid(row=2, column=0, padx=self.padx, pady=self.pady)
                asc_rb.grid(row=2, column=1, padx=self.padx, pady=self.pady)

                option_window_sort.bind('<<ListboxSelect>>', lambda event: on_sort_select(event, 'sort'))
                option_window_default.bind('<<ListboxSelect>>', lambda event: on_sort_select(event, 'default'))

            else:
                sort_frame.grid_remove()
                self.selection_window.geometry('400x460')
                self.continue_frame.grid_configure(row=6)

            def add_sort():
                if not (option_window_sort.curselection() or option_window_default.curselection()):
                    pass
                else:
                    sort_select = option_window_default.get(option_window_default.curselection())
                    option_window_sort.insert('end', sort_select)
                    option_window_default.delete(option_window_default.curselection())

            def remove_sort():
                if not (option_window_sort.curselection() or option_window_default.curselection()):
                    pass
                else:
                    sort_select = option_window_sort.get(option_window_sort.curselection())
                    option_window_default.insert('end', sort_select)
                    option_window_sort.delete(option_window_sort.curselection())

            def on_sort_select(event, name):
                if name == 'sort' and event.widget.curselection():
                    add_button['state'] = 'disabled'
                    remove_button['state'] = 'enabled'
                elif name == 'default' and event.widget.curselection():
                    add_button['state'] = 'enabled'
                    remove_button['state'] = 'disabled'
                else:
                    pass

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

        def sort_window_get():
            sort_order = option_window_sort.get('0', END)
            specific_sort = []
            reverse_order = []
            for item in sort_order:
                specific_sort.append((self.sort_order_dict[item], True))
                reverse_order.append(self.order_rb.get())
            self.sort_order = specific_sort
            self.reverse = reverse_order

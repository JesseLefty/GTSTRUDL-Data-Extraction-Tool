"""
Generates the results selection window when user wants to add new result or modify existing result
"""
from tkinter import *
from tkinter.ttk import *
from Tools.utilities import center, CreateToolTip
from Tools.config import requested_results_headings, text_box_color_disable, text_box_color_enable, sort_order_dict
from DataProcessing.process_data import ProcessData
from Tools import shared_stuff


def disable_text_box(rb_value, textbox):
    """
    enables or disables a text box based on a radio button value

    :param rb_value: value of radio button associated with text box
    :param textbox: Tkinter textbox object being enabled or disabled
    """
    if rb_value == 1:
        textbox.delete('0.0', END)
        textbox.configure(state='disabled', background=text_box_color_disable)

    else:
        textbox.configure(state='normal', background=text_box_color_enable)


def get_text(rb_val, text_val):
    """
    gets the text in a text box based on radio button value
    :param rb_val: value of radio button associated with text box
    :param text_val: text object containing the value
    """
    if rb_val == 1:
        beam_id = 'ALL'
    else:
        beam_id = text_val.get('1.0', 'end-1c')
    return rb_val, beam_id.upper()


class ResultsSelectionWindow:
    """
    Generates window for the user to input the criteria for which they would like to parse the .gto file.

    :param tab_name: active tab name
    :param initial_window: active window
    :param modify: True/False depending on if 'modify' button is pressed
    :param selection_idd: index of the selected result if result is selected
    :param selected_result: set number and set name of selected result
    :param selected_results_tree: Tkinter textbox object containing evaluable results
    """

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
        self.results = shared_stuff.data_store
        self.results.tab_name = self.tab_name
        self.jt_rb = StringVar(value='ALL')
        self.first_rb = IntVar(value=1)
        self.second_rb = IntVar(value=1)
        self.sort_box_items = StringVar()
        self.default_box_items = StringVar()
        self.order_rb = BooleanVar(value=False)
        self.sort_cb = BooleanVar(value=False)
        self.fail_cb = BooleanVar(value=False)
        self.ir_range_rb = IntVar(value=1)
        self.set_num = self.results.set_index
        self.set_name = self.results.set_name
        if self.modify:
            self.first_rb.set(self.results.name[self.selection_idd][0])
            self.mod_first_text = self.results.name[self.selection_idd][1]
            if self.tab_name == 'Member Force':
                self.jt_rb.set(self.results.joint[self.selection_idd])
                self.second_rb.set(self.results.load[self.selection_idd][0])
                self.mod_second_text = self.results.load[self.selection_idd][1]
            elif self.tab_name == 'Joint Reaction':
                self.second_rb.set(self.results.load[self.selection_idd][0])
                self.mod_second_text = self.results.load[self.selection_idd][1]
            else:
                self.second_rb.set(self.results.profile[self.selection_idd][0])
                self.mod_second_text = self.results.profile[self.selection_idd][1]
                self.mod_ir_range_text = self.results.ir_range[self.selection_idd][1]
                self.ir_range_rb.set(self.results.ir_range[self.selection_idd][0])
                self.fail_cb.set(self.results.fail[self.selection_idd])
                self.sort_cb.set(self.results.sort[self.selection_idd])
                self.sort_order = self.results.sort_order[self.selection_idd]
                self.reverse = self.results.reverse[self.selection_idd]
        else:
            self.selection_idd = len(self.selected_results_tree.get_children())

        if self.tab_name == 'Member Force':
            self.joint = self.results.joint
            self.name = self.results.name
            self.load = self.results.load
        elif self.tab_name == 'Joint Reaction':
            self.name = self.results.name
            self.load = self.results.load
        else:
            self.name = self.results.name

        self.padx, self.pady = (5, 5), (5, 5)
        text_labels = requested_results_headings[self.tab_name]
        rb_text = ['ALL', 'STARTS WITH', 'ENDS WITH', 'CONTAINS', 'LIST']
        self.selection_window = Toplevel(self.initial_window)
        self.selection_window.geometry('400x360')
        center(self.selection_window, x_offset=-500)
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
            first_rb.configure(command=lambda: disable_text_box(self.first_rb.get(), self.first_text))
            second_rb = Radiobutton(second_select, text=text, variable=self.second_rb, value=val)
            second_rb.grid(row=0, column=val - 1)
            second_rb.configure(command=lambda: disable_text_box(self.second_rb.get(), self.second_text))

        self.first_text = Text(first_select, height=1, width=50, font=('Arial', 10), wrap=NONE)
        first_scrollx = Scrollbar(first_select)
        first_scrollx.configure(command=self.first_text.xview, orient=HORIZONTAL)
        CreateToolTip(self.first_text, 'List entries must be separated by comma (item1, item2, item3)')
        self.first_text.grid(row=1, column=0, columnspan=5, sticky='nw', pady=5, padx=5)
        first_scrollx.grid(row=2, column=0, columnspan=5, sticky='ew')
        self.first_text.configure(xscrollcommand=first_scrollx.set)
        self.first_text.config(state='disabled', background=text_box_color_disable)

        self.second_text = Text(second_select, height=1, width=50, font=('Arial', 10), wrap=NONE)
        second_scrollx = Scrollbar(second_select)
        second_scrollx.configure(command=self.second_text.xview, orient=HORIZONTAL)
        CreateToolTip(self.second_text, 'List entries must be separated by comma (item1, item2, item3)')

        self.second_text.grid(row=1, column=0, columnspan=5, sticky='nw', pady=5, padx=5)
        second_scrollx.grid(row=2, column=0, columnspan=5, sticky='ew')

        self.second_text.configure(xscrollcommand=second_scrollx.set)
        self.second_text.config(state='disabled', background=text_box_color_disable)

        self.store_button = Button(self.continue_frame, text="Store")

        cancel_button = Button(self.continue_frame, text="Cancel", command=lambda: self.selection_window.destroy())

        self.store_button.grid(row=0, column=2, padx=5, pady=5)
        cancel_button.grid(row=0, column=1, padx=5, pady=5)

        if self.modify:
            disable_text_box(self.first_rb.get(), self.first_text)
            disable_text_box(self.second_rb.get(), self.second_text)
            self.first_text.insert('1.0', self.mod_first_text)
            self.second_text.insert('1.0', self.mod_second_text)
        else:
            pass

        if self.tab_name == "Member Force":
            self.mem_force_window()

        elif self.tab_name == 'Joint Reaction':
            self.joint_reaction_window()

        else:
            self.code_check_window()

    def mem_force_window(self):
        """
        opens the results selection window specific to member force results
        """
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
                get_text(self.first_rb.get(), self.first_text),
                get_text(self.second_rb.get(), self.second_text),
                self.jt_rb.get(), selected_result=self.selected_result),
            self.selection_window.destroy()))

    def joint_reaction_window(self):
        """
        opens the results selection window specific to the joint reaction results
        """
        self.selection_window.geometry('400x300')
        self.store_button.configure(command=lambda: (
            ProcessData(self.tab_name, self.selection_idd, modify=self.modify,
                        selected_results_tree=self.selected_results_tree).store_results(
                get_text(self.first_rb.get(), self.first_text),
                get_text(self.second_rb.get(), self.second_text),
                self.jt_rb.get(), selected_result=self.selected_result),
            self.selection_window.destroy()))

    def code_check_window(self):
        """
        opens the results selection window specific to the code check results
        """
        style = Style()
        style.configure('mystyle.Treeview.Heading', font=('futura', 10, 'bold'))
        self.selection_window.geometry('400x460')
        self.continue_frame.grid(row=6)
        self.default_box_items.set(('IR Value', 'Profile', 'Name'))
        ir_range = LabelFrame(self.selection_window, text='IR RANGE', height=90, width=380)
        misc_frame = LabelFrame(self.selection_window, text='MISC OPTIONS', height=50, width=380)

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
        option_window_default = Treeview(sort_frame, columns=['Sort Options'],
                                         show='headings',
                                         height=4, style='mystyle.Treeview')
        option_window_sort = Treeview(sort_frame, columns=['Sort Selection', 'Order'],
                                      show='headings',
                                      height=4, style='mystyle.Treeview')
        sort_button_window = Frame(sort_frame, width=100, height=120)
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

        self.store_button.configure(command=lambda: (sort_window_get(),
                                                     ProcessData(self.tab_name, self.selection_idd,
                                                                 modify=self.modify,
                                                                 selected_results_tree=self.selected_results_tree).store_results(
                                                         get_text(self.first_rb.get(), self.first_text),
                                                         get_text(self.second_rb.get(), self.second_text),
                                                         selected_result=self.selected_result,
                                                         ir_range=ir_text_get(self.ir_range_rb.get()),
                                                         sort=self.sort_cb.get(), fail=self.fail_cb.get(),
                                                         sort_order=self.sort_order, reverse=self.reverse),
                                                     self.selection_window.destroy()))

        if self.modify:
            if self.results.ir_range[self.selection_idd][0] == 2:
                ir_range_text_max.insert('1.0', self.mod_ir_range_text[1])
                ir_range_text_min.config(state='disabled')
                ir_range_text_min.configure(background=text_box_color_disable)
            elif self.results.ir_range[self.selection_idd][0] == 3:
                ir_range_text_min.insert('1.0', self.mod_ir_range_text[0])
                ir_range_text_max.config(state='disabled')
                ir_range_text_max.configure(background=text_box_color_disable)
            elif self.results.ir_range[self.selection_idd][0] == 4:
                ir_range_text_min.insert('1.0', self.mod_ir_range_text[0])
                ir_range_text_max.insert('1.0', self.mod_ir_range_text[1])
            else:
                ir_range_text_min.config(state='disabled')
                ir_range_text_max.config(state='disabled')
                ir_range_text_max.configure(background=text_box_color_disable)
                ir_range_text_min.configure(background=text_box_color_disable)
        else:
            ir_range_text_min.config(state='disabled')
            ir_range_text_max.config(state='disabled')
            ir_range_text_max.configure(background=text_box_color_disable)
            ir_range_text_min.configure(background=text_box_color_disable)

        def sort_window(sort_flag):
            """
            expands the results selection window to allow user to select code check result sorting options

            :param sort_flag: radio button associated with sorting selection
            """
            add_button = Button(sort_button_window, text='Add >>', command=lambda: add_sort())
            remove_button = Button(sort_button_window, text='<< Remove', command=lambda: remove_sort())
            add_button['state'] = 'disabled'
            remove_button['state'] = 'disabled'

            if sort_flag.get():
                self.selection_window.geometry('400x630')
                sort_frame.grid(row=6, column=0, columnspan=5, padx=self.padx, pady=self.pady)
                option_window_default.grid(row=0, column=0, padx=(5, 0), pady=self.pady, sticky='n')
                option_window_sort.grid(row=0, column=4, padx=(0, 5), pady=self.pady, sticky='n')
                sort_button_window.grid(row=0, column=1, columnspan=3, padx=self.padx, pady=self.pady, sticky='nsew')
                sort_frame.grid_propagate(0)
                sort_button_window.grid_propagate(0)
                self.continue_frame.grid_configure(row=7)
                for index, col in enumerate(['Sort Selection', 'Order']):
                    option_window_sort.heading(col, text=col.title())
                    width = [100, 50]
                    anchor = [W, CENTER]
                    option_window_sort.column(col, width=width[index], minwidth=25, anchor=anchor[index])
                option_window_default.heading('Sort Options', text='Sort Options'.title())
                option_window_default.column('Sort Options', width=90, minwidth=25, anchor=W)
                for idx, value in enumerate(['IR', 'Profile', 'Name'], start=1):
                    option_window_default.insert(parent='', index='end', value=value)

                add_button.grid(row=0, column=0, columnspan=2, padx=self.padx, pady=self.pady)
                remove_button.grid(row=1, column=0, columnspan=2, padx=self.padx, pady=self.pady)

                dec_rb.grid(row=2, column=0, padx=(0, 5), pady=self.pady)
                asc_rb.grid(row=2, column=1, padx=(5, 0), pady=self.pady)

                option_window_sort.bind('<<TreeviewSelect>>', lambda event: on_sort_select(event, 'sort'))
                option_window_default.bind('<<TreeviewSelect>>', lambda event: on_sort_select(event, 'default'))

            else:
                sort_frame.grid_remove()
                self.selection_window.geometry('400x460')
                self.continue_frame.grid_configure(row=6)

            def add_sort():
                """
                adds a selected sorting parameter to the selected sorting list box and removes it from the option
                window
                """
                if not (option_window_sort.selection() or option_window_default.selection()):
                    pass
                else:
                    sort_select = option_window_default.item(option_window_default.focus())
                    if self.order_rb.get():
                        order = 'Dec.'
                    else:
                        order = 'Asc.'
                    option_window_sort.insert(parent='', index='end', values=(sort_select["values"], order))
                    option_window_default.delete(option_window_default.selection())

            def remove_sort():
                """
                removes a selected sorting parameter from the selected sorting list box and moves it to the option
                window
                """
                if not (option_window_sort.selection() or option_window_default.selection()):
                    pass
                else:
                    sort_select = option_window_sort.item(option_window_sort.focus())
                    option_window_default.insert(parent='', index='end', values=sort_select['values'][0])
                    option_window_sort.delete(option_window_sort.selection())

            def on_sort_select(event, name):
                """
                enables or disables the add and remove button based on what the user is selection.

                :param event: click event
                :param name: name of window that was clicked
                """
                if name == 'sort' and event.widget.selection():
                    add_button['state'] = 'disabled'
                    remove_button['state'] = 'enabled'
                elif name == 'default' and event.widget.selection():
                    add_button['state'] = 'enabled'
                    remove_button['state'] = 'disabled'
                else:
                    pass

        def ir_text_get(ir_range_rb_val):
            """
            gets the text contained in the IR criteria text boxes

            :param ir_range_rb_val: value of IR range radio button
            """
            if ir_range_rb_val == 1:
                ir_range_id = ('', '')
            else:
                ir_range_id = (ir_range_text_min.get('1.0', 'end-1c'), ir_range_text_max.get('1.0', 'end-1c'))
            return ir_range_rb_val, ir_range_id

        def ir_range_disable(ir_range_rb_val):
            """
            enables or disables the IR range text boxes based on the radio button value

            :param ir_range_rb_val: value of radio button associated with IR range text boxes
            """
            if ir_range_rb_val == 2:
                ir_range_text_min.delete('0.0', END)
                ir_range_text_min['state'] = 'disabled'
                ir_range_text_min.configure(background=text_box_color_disable)
                ir_range_text_max['state'] = 'normal'
                ir_range_text_max.configure(background=text_box_color_enable)
            elif ir_range_rb_val == 3:
                ir_range_text_max.delete('0.0', END)
                ir_range_text_max['state'] = 'disabled'
                ir_range_text_max.configure(background=text_box_color_disable)
                ir_range_text_min['state'] = 'normal'
                ir_range_text_min.configure(background=text_box_color_enable)
            elif ir_range_rb_val == 1:
                ir_range_text_max.delete('0.0', END)
                ir_range_text_min.delete('0.0', END)
                ir_range_text_max.configure(background=text_box_color_disable)
                ir_range_text_min.configure(background=text_box_color_disable)
                ir_range_text_max['state'] = 'disabled'
                ir_range_text_min['state'] = 'disabled'
            else:
                ir_range_text_min['state'] = 'normal'
                ir_range_text_max['state'] = 'normal'
                ir_range_text_min.configure(background=text_box_color_enable)
                ir_range_text_max.configure(background=text_box_color_enable)

        def sort_window_get():
            """
            sets the sort order and reverse variables based on the content in the sorting window
            """
            sort_order = option_window_sort.get_children()
            specific_sort = []
            reverse_order = []
            if sort_order:
                for item in sort_order:
                    sort_criteria, order = option_window_sort.item(item)['values']
                    specific_sort.append((sort_order_dict[sort_criteria], True))
                    if order == 'Asc.':
                        reverse = False
                    else:
                        reverse = True
                    reverse_order.append(reverse)
            else:
                pass
            self.sort_order = specific_sort
            self.reverse = reverse_order

        if self.sort_cb.get():
            sort_window(self.sort_cb)

from tkinter import *
from tkinter.ttk import *
import error_handling
import utilities_GUI
import config
from results_selection_window import ResultsSelectionWindow
from process_data import ProcessData
from data_storage import ResultsParameters


class GenerateTab:

    def __init__(self, frame, tab_name, initial_window, directory=False, input_file_path=False):

        self.frame = frame
        self.tab_name = tab_name
        self.initial_window = initial_window
        self.input_file_path = input_file_path
        self.modify = False
        padx, pady = (5, 5), (5, 0)
        self.btn_width = 15
        header = Label(self.frame, text=self.tab_name)
        self.available_result_set_frame = LabelFrame(self.frame, text=f'Available {self.tab_name} Results', height=160,
                                                     width=420)
        self.selected_result_set_frame = LabelFrame(self.frame, text='Requested Results', height=135, width=580)
        button_frame = LabelFrame(self.frame, text='Result Set Options', height=160, width=150)
        bottom_bar_frame = Frame(self.frame, height=30, width=580)

        header.grid(row=0, column=0, columnspan=1, padx=padx, pady=pady)
        self.available_result_set_frame.grid(row=1, column=1, padx=padx, pady=pady, sticky='nw')
        self.selected_result_set_frame.grid(row=2, column=0, columnspan=3, padx=padx, pady=pady, sticky='nsew')
        button_frame.grid(row=1, column=0, padx=padx, pady=pady)
        bottom_bar_frame.grid(row=3, column=0, columnspan=3, pady=pady, padx=padx, sticky='se')

        self.available_result_set_frame.grid_propagate(0)
        self.selected_result_set_frame.grid_propagate(0)
        button_frame.grid_propagate(0)

        available_results, input_index = utilities_GUI.GenerateDisplayData(self.input_file_path).get_display(
            self.tab_name)
        self.available_results_tree = Treeview(self.available_result_set_frame,
                                               columns=config.available_results_headings,
                                               show='headings',
                                               height=5)

        if available_results:
            self.not_valid_list = False
        else:
            available_results_list = 'No Member Forces Found in Output'
            self.not_valid_list = True

        list_yscroll = Scrollbar(self.available_result_set_frame)
        list_xscroll = Scrollbar(self.available_result_set_frame)
        list_xscroll.configure(command=self.available_results_tree.xview, orient=HORIZONTAL)
        list_yscroll.configure(command=self.available_results_tree.yview, orient=VERTICAL)

        list_yscroll.pack(side=RIGHT, fill=Y)
        list_xscroll.pack(side=BOTTOM, fill=X)
        self.available_results_tree.pack(side=LEFT, expand=True)

        for idx, col in enumerate(config.available_results_headings):
            self.available_results_tree.heading(col, text=col.title())
            tree_width = [40, 275, 75]
            tree_anchor = [CENTER, W, CENTER]
            self.available_results_tree.column(col, width=tree_width[idx], minwidth=tree_width[idx],
                                               anchor=tree_anchor[idx])

        for idx, value in enumerate(available_results, start=1):
            if self.not_valid_list:
                self.available_results_tree.insert(parent='', index='end', iid=idx, text=available_results_list,
                                                   values=(idx, available_results_list))
            else:
                self.available_results_tree.insert(parent='', index='end', iid=idx, text=value,
                                                   values=(idx, value, input_index[idx - 1]))

        self.selected_results_tree = Treeview(self.selected_result_set_frame,
                                              columns=config.requested_results_headings[self.tab_name]['headings'],
                                              show='headings',
                                              height=3)
        tree_scrollx = Scrollbar(self.selected_result_set_frame)
        tree_scrolly = Scrollbar(self.selected_result_set_frame)
        tree_scrollx.configure(command=self.selected_results_tree.xview, orient=HORIZONTAL)
        tree_scrolly.configure(command=self.selected_results_tree.yview)
        self.selected_results_tree.configure(xscrollcommand=tree_scrollx.set, yscrollcommand=tree_scrolly.set)
        tree_scrolly.pack(side=RIGHT, fill=Y)
        tree_scrollx.pack(side=BOTTOM, fill=X)
        self.selected_results_tree.pack(side=LEFT, fill=X, expand=True)

        for idx, col in enumerate(config.requested_results_headings[self.tab_name]['headings'], start=0):
            print(idx, col)
            self.selected_results_tree.heading(col, text=col.title())
            tree_width = config.requested_results_headings[self.tab_name]['column width']
            tree_anchor = config.requested_results_headings[self.tab_name]['text location']
            self.selected_results_tree.column(col, width=tree_width[idx], minwidth=tree_width[idx],
                                              anchor=tree_anchor[idx])

        self.selected_results_tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.available_results_tree.bind('<<TreeviewSelect>>', self.on_list_select)

        self.new_result_set = Button(button_frame, text="Create New",
                                     command=lambda: ResultsSelectionWindow(self.frame, self.tab_name,
                                                                            self.initial_window,
                                                                            selection_idd=self.tree_select(),
                                                                            selected_result=self.list_select(),
                                                                            selected_results_tree=self.selected_results_tree))

        self.load_exist_result_set = Button(button_frame, text="Load Existing",
                                            command=lambda: ProcessData(self.tab_name.load_existing_result_set()))
        self.modify_result = Button(button_frame, text='Modify Result',
                                    command=lambda: (self.modify_pressed(), ResultsSelectionWindow(self.frame, self.tab_name,
                                                                           self.initial_window,
                                                                           self.modify,
                                                                           selection_idd=self.tree_select(),
                                                                           selected_results_tree=self.selected_results_tree)))
        self.delete_result = Button(button_frame, text='Delete Result',
                                    command=lambda: self.delete_result)  # add selection_idd as item in tree selected

        for num, button in enumerate(filter(lambda w: isinstance(w, Button), button_frame.children.values())):
            button.configure(width=self.btn_width)
            button.grid(row=num + 2, column=0, padx=22, pady=5, sticky='nsew')

        generate_button = Button(bottom_bar_frame, text="Generate",
                                 command=lambda: ProcessData(self.tab_name.generate_results()))

        store_mem_results_prop = Button(bottom_bar_frame, text='Store Input',
                                        command=lambda: ProcessData(self.tab_name).store_results())

        store_mem_results_prop.grid(row=0, column=0, padx=(10, 405), pady=5)
        generate_button.grid(row=0, column=3, padx=5, pady=5)

        self.new_result_set['state'] = 'disabled'
        self.delete_result['state'] = 'disabled'
        self.modify_result['state'] = 'disabled'

    def on_list_select(self, event):
        if self.not_valid_list:
            self.new_result_set['state'] = 'disabled'
        else:
            self.new_result_set['state'] = 'enabled'
            self.modify_result['state'] = 'disabled'
            self.delete_result['state'] = 'disabled'

    def on_tree_select(self, event):
        self.modify_result['state'] = 'enabled'
        self.delete_result['state'] = 'enabled'
        self.new_result_set['state'] = 'disabled'
        if len(self.selected_results_tree.selection()) > 1:
            self.modify_result['state'] = 'disabled'
        elif not self.selected_results_tree.get_children():
            self.delete_result['state'] = 'disabled'
            self.modify_result['state'] = 'disabled'

    def list_select(self):
        selection_index = int(self.available_results_tree.selection()[0]) - 1
        display_index = int(self.available_results_tree.selection()[0])
        stored_value = self.available_results_tree.item(display_index, "text")
        return selection_index, stored_value

    def tree_select(self):
        if self.modify_result['state'] == 'enabled':
            tree_selection_index = int(self.selected_results_tree.selection()[0]) - 1
        else:
            tree_selection_index = 0

        return tree_selection_index

    def modify_pressed(self):
        self.modify = True



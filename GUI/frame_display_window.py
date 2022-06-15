"""
This module generates the content in each tab. This includes all buttons, text, and Treeview objects.
"""
from tkinter import *
from tkinter.ttk import *
import error_handling
from Tools.utilities import GenerateDisplayData
from Tools import config
from GUI.results_selection_window import ResultsSelectionWindow
from DataProcessing.process_data import ProcessData


class GenerateTab:
    """
    Generates the buttons, text, text boxes, and results treeview object for each tab.

    :param frame: Tkinter Frame object
    :param tab_name: name of active tab
    :param initial_window: Tkinter active window object
    :param input_file_path: file path of user selected .gto file
    """

    def __init__(self, frame, tab_name, initial_window, input_file_path=False):

        self.frame = frame
        self.tab_name = tab_name
        self.initial_window = initial_window
        self.input_file_path = input_file_path
        self.modify = False
        style = Style()
        style.configure('mystyle.Treeview.Heading', font=('futura', 10, 'bold'))
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

        available_results, input_index = GenerateDisplayData(self.input_file_path).get_display(self.tab_name)
        self.available_results_tree = Treeview(self.available_result_set_frame,
                                               columns=config.available_results_headings,
                                               show='headings',
                                               height=5, style='mystyle.Treeview')
        if available_results:
            self.not_valid_list = False
        else:
            available_results_list = f'No {self.tab_name} Results found in output'
            self.not_valid_list = True
        list_yscroll = Scrollbar(self.available_result_set_frame)
        list_xscroll = Scrollbar(self.available_result_set_frame)
        list_xscroll.configure(command=self.available_results_tree.xview, orient=HORIZONTAL)
        list_yscroll.configure(command=self.available_results_tree.yview, orient=VERTICAL)
        list_yscroll.pack(side=RIGHT, fill=Y)
        list_xscroll.pack(side=BOTTOM, fill=X)
        self.available_results_tree.pack(side=LEFT, expand=True)
        self.available_results_tree.configure(xscrollcommand=list_xscroll.set, yscrollcommand=list_yscroll.set)

        for idx, col in enumerate(config.available_results_headings):
            self.available_results_tree.heading(col, text=col.title())
            tree_width = [40, 260, 100]
            tree_anchor = [CENTER, W, CENTER]
            self.available_results_tree.column(col, width=tree_width[idx], minwidth=tree_width[idx],
                                               anchor=tree_anchor[idx], stretch=False)

        if self.not_valid_list:
            self.available_results_tree.insert(parent='', index='end', iid=0, text=available_results_list,
                                               values=("", available_results_list))
        else:
            for idx, value in enumerate(available_results, start=1):
                self.available_results_tree.insert(parent='', index='end', iid=idx, text=value,
                                                   values=(idx, value, input_index[idx - 1]))

        self.selected_results_tree = Treeview(self.selected_result_set_frame,
                                              columns=config.requested_results_headings[self.tab_name]['headings'],
                                              show='headings',
                                              height=3, style='mystyle.Treeview')

        tree_scrollx = Scrollbar(self.selected_result_set_frame)
        tree_scrolly = Scrollbar(self.selected_result_set_frame)
        tree_scrollx.configure(command=self.selected_results_tree.xview, orient=HORIZONTAL)
        tree_scrolly.configure(command=self.selected_results_tree.yview)
        self.selected_results_tree.configure(xscrollcommand=tree_scrollx.set, yscrollcommand=tree_scrolly.set)
        tree_scrolly.pack(side=RIGHT, fill=Y)
        tree_scrollx.pack(side=BOTTOM, fill=X)
        self.selected_results_tree.pack(side=LEFT, fill=X, expand=True)

        for idx, col in enumerate(config.requested_results_headings[self.tab_name]['headings'], start=0):
            self.selected_results_tree.heading(col, text=col)
            tree_width = config.requested_results_headings[self.tab_name]['column width']
            tree_anchor = config.requested_results_headings[self.tab_name]['text location']
            self.selected_results_tree.column(col, width=tree_width[idx], minwidth=tree_width[idx],
                                              anchor=tree_anchor[idx], stretch=False)

        self.selected_results_tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.available_results_tree.bind('<<TreeviewSelect>>', self.on_list_select)
        self.selected_results_tree.bind('<Double-1>', self.on_double_click_selected)
        self.available_results_tree.bind('<Double-1>', self.on_double_click_available)

        self.new_result_set = Button(button_frame, text="Create New",
                                     command=lambda: ResultsSelectionWindow(self.tab_name,
                                                                            self.initial_window,
                                                                            selection_idd=self.tree_select(),
                                                                            selected_result=self.list_select(),
                                                                            selected_results_tree=self.selected_results_tree))

        self.load_exist_result_set = Button(button_frame, text="Load Existing",
                                            command=lambda: ProcessData(self.tab_name,
                                                                        selected_results_tree=self.selected_results_tree).load_existing_result_set())
        self.modify_result = Button(button_frame, text='Modify Result',
                                    command=lambda: (self.modify_pressed(), ResultsSelectionWindow(self.tab_name,
                                                                                                   self.initial_window,
                                                                                                   self.modify,
                                                                                                   selection_idd=self.tree_select(),
                                                                                                   selected_results_tree=self.selected_results_tree)))
        self.delete_result = Button(button_frame, text='Delete Result',
                                    command=lambda: (ProcessData(self.tab_name, selection_idd=self.tree_select(),
                                                                 selected_results_tree=self.selected_results_tree).delete_result()))

        for num, button in enumerate(filter(lambda w: isinstance(w, Button), button_frame.children.values())):
            button.configure(width=self.btn_width)
            button.grid(row=num + 2, column=0, padx=22, pady=5, sticky='nsew')

        generate_button = Button(bottom_bar_frame, text="Generate",
                                 command=lambda: ProcessData(self.tab_name,
                                                             initial_window=self.initial_window).generate_results())

        store_properties = Button(bottom_bar_frame, text='Store Input',
                                  command=lambda: (ProcessData(self.tab_name,
                                                               selected_results_tree=self.selected_results_tree).store_inputs(),
                                                   self.check_for_results()))

        store_properties.grid(row=0, column=0, padx=(10, 405), pady=5)
        generate_button.grid(row=0, column=3, padx=5, pady=5)

        self.new_result_set['state'] = 'disabled'
        self.delete_result['state'] = 'disabled'
        self.modify_result['state'] = 'disabled'

    def on_double_click_selected(self, event):
        """
        resizes tkinter Treeview to original header sizing on double click

        :param event: double click event
        """
        region = self.selected_results_tree.identify("region", event.x, event.y)
        if region == "heading":
            for idx, col in enumerate(config.requested_results_headings[self.tab_name]['headings'], start=0):
                tree_width = config.requested_results_headings[self.tab_name]['column width']
                self.selected_results_tree.column(col, width=tree_width[idx])

    def on_double_click_available(self, event):
        """
        resizes tkinter Treeview to original header sizing on double click

        :param event: double click event
        """
        region = self.available_results_tree.identify("region", event.x, event.y)
        if region == "heading":
            for idx, col in enumerate(config.available_results_headings, start=0):
                tree_width = [40, 260, 100]
                self.available_results_tree.column(col, width=tree_width[idx])

    def on_list_select(self, event):
        """
        Enables or disables selection buttons when user clicks on available results window

        :param event:
        """
        if self.not_valid_list:
            self.new_result_set['state'] = 'disabled'
        else:
            self.new_result_set['state'] = 'enabled'
            self.modify_result['state'] = 'disabled'
            self.delete_result['state'] = 'disabled'

    def on_tree_select(self, event):
        """
        Enables or disables selection buttons when user clicks on requested results Treeview

        :param event:
        """
        self.modify_result['state'] = 'enabled'
        self.delete_result['state'] = 'enabled'
        self.new_result_set['state'] = 'disabled'
        if len(self.selected_results_tree.selection()) > 1:
            self.modify_result['state'] = 'disabled'
        elif not self.selected_results_tree.get_children():
            self.delete_result['state'] = 'disabled'
            self.modify_result['state'] = 'disabled'

    def list_select(self):
        """
        determines the index of the item selected in the available results window as well as the set name

        :return: tuple containing the set number and set name of the selected result
        """
        set_num = int(self.available_results_tree.selection()[0]) - 1
        display_index = int(self.available_results_tree.selection()[0])
        set_name = self.available_results_tree.item(display_index, "text")
        return set_num, set_name

    def tree_select(self):
        """
        determines the index of the item selected in the requested results Treeview

        :return: index of selected result in the tree
        """
        if self.modify_result['state'] == 'enabled':
            tree_selection_index = int(self.selected_results_tree.selection()[0]) - 1
        else:
            tree_selection_index = 0

        return tree_selection_index

    def modify_pressed(self):
        """
        sets modify to True if the modify button is pressed
        """
        self.modify = True

    def check_for_results(self):
        """
        checks for results in the results Treeview. If no results exists, raises an error.
        """
        if not self.selected_results_tree.get_children():
            error_handling.ErrorHandling(self.initial_window).no_result_set()

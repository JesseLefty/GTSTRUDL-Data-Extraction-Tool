"""
This module contains the class for error handling. This class gets called whenever a predefined error has been
encountered and displays the error to the user.
"""
from tkinter import *
from tkinter.ttk import *
import utilities


def is_valid_mem_force(input_file, search_string):
    """
    checks to make sure file contains 'output by member'. If not, produces error preventing user from continuing

    :param input_file: .gto file being parsed
    :param search_string: string to find in file
    :return True true if search string is in file and before results, False otherwise
    """
    display_data = utilities.GenerateDisplayData(input_file)
    first_member_force_result = display_data.get_display('Member Force')
    string_position, result_position = None, None
    if any('OUTPUT BY LOAD' in x for x in display_data.file_list):
        return False
    if first_member_force_result[0]:
        for line, value in enumerate(display_data.file_list):
            if (search_string in value) and ("$" not in value):
                string_position = line
            elif first_member_force_result[1][0] in value:
                result_position = line
            else:
                pass
            if string_position and result_position:
                break
        if string_position and result_position:
            if string_position < result_position:
                return True
            else:
                return False
        else:
            return False
    else:
        return True


def on_double_click(event, tree, header, width):
    """
    resizes tkinter Treeview to original header sizing on double click

    :param event: double click event
    :param tree: tkinter Treeview widget
    :param header: Treeview header
    :param width: Treeview header width
    """
    region = tree.identify("region", event.x, event.y)
    if region == "heading":
        for idx, col in enumerate(header, start=0):
            tree.column(col, width=width[idx])


class ErrorHandling:
    """
    Provides feed back to the user based on the type of error encountered. Generates a template pop-up with slight
    modifications based on the sub function chosen

    :param initial_window: tkinter current active window
    """
    def __init__(self, initial_window):
        self.initial_window = initial_window
        self.error_window = Toplevel(self.initial_window)
        self.error_window.geometry('400x200')
        self.error_window.resizable(False, False)
        utilities.center(self.error_window)
        self.error_window.title("ERROR!")
        self.error_top_frame = Frame(self.error_window, width=300, height=40)
        self.error_top_frame.pack(side='top', fill='x')
        self.error_bottom_frame = Frame(self.error_window, width=300, height=40)
        self.error_bottom_frame.pack(side='bottom', fill='x')
        self.error_mid_frame = Frame(self.error_window, width=300, height=105)
        self.error_mid_frame.pack(fill='both', expand=True)

        mid_style = Style()
        mid_style.configure('mid_frame.TFrame', background='white')

        self.label_style = Style()
        self.label_style.configure('mid.TLabel', background='white')

        self.error_mid_frame.configure(style='mid_frame.TFrame')
        self.error_mid_frame.grid_rowconfigure(0, weight=1)
        exit_button = Button(self.error_bottom_frame, text='OK', command=self.error_window.destroy)
        exit_button.pack(pady=15, side='bottom')

        self.error_top_label = Label(self.error_top_frame, text='!! ERROR !!', justify='center', font='helvetica 20')
        self.error_top_label.pack()
        self.error_window.grab_set()

    def no_result_set(self):
        """
        Used to indicate no result sets have been generated if the user tries to store properties file before generating
        result sets.
        """
        self.error_window.geometry('300x125')
        Label(self.error_mid_frame, text=f'No result sets have been created.\n'
                                         f'Please create result sets before continuing', wraplength=280,
              justify='center', style='mid.TLabel').grid(row=0, column=0, sticky='nsew', padx=(10, 10))

    def no_directory(self):
        """
        Used to indicate no working director has been selected if user tires to select a file prior to selecting a
        directory
        """
        self.error_window.geometry('300x125')
        Label(self.error_mid_frame,
              text='No working directory has been selected.\n Please select directory before selecting file',
              wraplength=280, justify='center',
              style='mid.TLabel').grid(row=0, column=0, sticky='nsew', padx=(10, 10))

    def item_not_found(self, item, box_one, box_two, tab_name, ir_errors=None):
        """
        Used to display which result sets have errors and which user inputs prodiced those errors

        :param item: result set which is checked for errors
        :param box_one: errors in user input box 1
        :param box_two: errors in user input box 2
        :param tab_name: active tab name
        :param ir_errors: errors in user IR selection
        """
        style = Style()
        style.configure('mystyle.Treeview.Heading', font=('futura', 10, 'bold'))
        self.error_window.geometry('400x300')
        tree_width = [40, 165, 165]
        tree_anchor = [CENTER, CENTER, CENTER]
        if tab_name == 'Member Force':
            col_2 = 'Beam" or "Load'
            tree_header = ['Set #', 'Beam', 'Load']
        elif tab_name == 'Joint Reaction':
            col_2 = 'Joint" or "Load'
            tree_header = ['Set #', 'Joint', 'Load']
        else:
            col_2 = 'Name", "Profile", or "IR'
            tree_header = ['Set #', 'Name', 'Profile', 'IR Range']
            tree_width = [40, 110, 110, 110]
            tree_anchor = [CENTER, CENTER, CENTER, CENTER]

        text_label_top = Label(self.error_mid_frame, style='mid.TLabel', wraplength=380, justify='left',
                               text=f'The following result set(s) contain incorrect inputs in the "{col_2}"'
                                    f' spec:')
        text_label_top.pack(side=TOP, padx=(10, 10))
        error_tree = Treeview(self.error_mid_frame, columns=tree_header, show='headings', height=4,
                              style='mystyle.Treeview')
        for idx, col in enumerate(tree_header):
            error_tree.heading(col, text=col)
            error_tree.column(col, width=tree_width[idx], minwidth=tree_width[idx], anchor=tree_anchor[idx],
                              stretch=False)
        tree_scrollx = Scrollbar(self.error_mid_frame)
        tree_scrolly = Scrollbar(self.error_mid_frame)
        tree_scrollx.configure(command=error_tree.xview, orient=HORIZONTAL)
        tree_scrolly.configure(command=error_tree.yview)
        error_tree.configure(xscrollcommand=tree_scrollx.set, yscrollcommand=tree_scrolly.set)
        tree_scrolly.pack(side=RIGHT, fill=Y)
        tree_scrollx.pack(side=BOTTOM, fill=X)
        error_tree.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))
        if tab_name == 'Code Check':
            for index, set_num in enumerate(item):
                if not box_one[index]:
                    box_one[index] = '---'
                if not box_two[index]:
                    box_two[index] = '---'
                if not ir_errors[index]:
                    ir_errors[index] = '---'
                error_tree.insert(parent='', index='end', iid=index, text=set_num, values=(set_num, box_one[index],
                                                                                           box_two[index], ir_errors[index]))
        else:
            for index, set_num in enumerate(item):
                if not box_one[index]:
                    box_one[index] = '---'
                if not box_two[index]:
                    box_two[index] = '---'
                error_tree.insert(parent='', index='end', iid=index, text=set_num, values=(set_num, box_one[index],
                                                                                           box_two[index]))

        error_tree.bind('<Double-1>', lambda event: on_double_click(event, error_tree, tree_header, tree_width))

    def wrong_properties_file(self, result_type):
        """
        Used to indicate the user tried to load in a properties file which does not match the active tab

        :param result_type: active tab name
        """
        self.error_window.geometry('300x160')
        Label(self.error_mid_frame,
              text=f'Selected property file is incorrect for {result_type} results. Please select a file that contains'
                   f' {result_type} results',
              wraplength=280, justify='center',
              style='mid.TLabel').grid(row=0, column=0, sticky='nsew', padx=(10, 10))

    def file_already_open(self, error):
        """
        used to indicate the excel file being generated is already opened somewhere
        :param error: text describing the error
        """
        self.error_window.geometry('300x160')
        Label(self.error_mid_frame,
              text=f'Please close file before saving\n'
                   f'{error}',
              wraplength=280, justify='center',
              style='mid.TLabel').grid(row=0, column=0, sticky='nsew', padx=(10, 10))

    def no_output_by_member(self):
        self.error_window.geometry('300x200')
        Label(self.error_mid_frame,
              text=f'Program cannot continue for one of the following reasons:\n'
                   f'1. "OUTPUT BY LOAD" is specified (currently not supported)\n'
                   f'2. "OUTPUT BY MEMBER" is not specified or that command is specified after "LIST FORCES"',
              wraplength=280, justify='left',
              style='mid.TLabel').grid(row=0, column=0, sticky='nsew', padx=(10, 10))




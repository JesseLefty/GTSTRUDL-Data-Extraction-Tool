from tkinter import *
from tkinter.ttk import *

import utilities


class ErrorHandling:

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
        exit_button = Button(self.error_bottom_frame, text='OK', command=lambda: self.error_window.destroy())
        exit_button.pack(pady=15, side='bottom')

        self.error_top_label = Label(self.error_top_frame, text='!! ERROR !!', justify='center', font='helvetica 20')
        self.error_top_label.pack()
        self.error_window.grab_set()

    def no_result_set(self):
        self.error_window.geometry('300x125')
        Label(self.error_mid_frame, text=f'No result sets have been generated. Please generate results before storing'
                                         f' the inputs', wraplength=280,
              justify='center', style='mid.TLabel').grid(row=0, column=0, sticky='nsew', padx=(10, 10))

    def no_directory(self):
        self.error_window.geometry('300x125')
        Label(self.error_mid_frame,
              text=f'No working directory has been selected. Please select directory before selecting file',
              wraplength=280, justify='center',
              style='mid.TLabel').grid(row=0, column=0, sticky='nsew', padx=(10, 10))

    def item_not_found(self, item, beam_or_joint, load, tab_name, ir_errors=None):
        self.error_window.geometry('400x300')
        tree_width = [20, 60, 60]
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
            tree_width = [20, 40, 40, 40]
            tree_anchor = [CENTER, CENTER, CENTER, CENTER]

        text_label_top = Label(self.error_mid_frame, style='mid.TLabel', wraplength=380, justify='left',
                               text=f'The following result set(s) contain incorrect inputs in the "{col_2}"'
                                    f' spec:')
        text_label_top.pack(side=TOP, padx=(10, 10))
        error_tree = Treeview(self.error_mid_frame, columns=tree_header, show='headings', height=4)
        for idx, col in enumerate(tree_header):
            error_tree.heading(col, text=col)
            error_tree.column(col, width=tree_width[idx], minwidth=tree_width[idx], anchor=tree_anchor[idx])
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
                error_tree.insert(parent='', index='end', iid=index, text=set_num, values=(set_num, beam_or_joint[index],
                                                                                       load[index], ir_errors[index]))
        else:
            for index, set_num in enumerate(item):
                error_tree.insert(parent='', index='end', iid=index, text=set_num, values=(set_num, beam_or_joint[index],
                                                                                       load[index]))

    def wrong_properties_file(self, result_type):
        self.error_window.geometry('300x160')
        Label(self.error_mid_frame,
              text=f'Selected property file is incorrect for {result_type} results. Please select a file that contains'
                   f' {result_type} results',
              wraplength=280, justify='center',
              style='mid.TLabel').grid(row=0, column=0, sticky='nsew', padx=(10, 10))

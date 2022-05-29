"""
This module generates the initial window of the program, the landing window. This window displays the title and
description of the program and prompts the user to select a working directory and .gto file
"""
from tkinter import *
from tkinter.ttk import *
import os
from tkinter import filedialog
import shared_stuff
import frame_display_window
import error_handling
import utilities
from config import load_file_types


def help_doc():
    """
    opens help documentation
    """
    help_pdf = r"Supporting Documents\code_check.csv"
    os.startfile(help_pdf)


class FirstWindow:

    """
    Generates the directory and file selection window and the first window of the program (landing window)

    :param: initial window - Tkinter mainloop root object
    """

    def __init__(self, initial_window):
        self.initial_window = initial_window
        self.results = shared_stuff.data_store

    def win_display(self):
        """
        Generates the landing window
        """
        self.initial_window.title("GTSTRUDL Data Extraction Tool")
        self.initial_window.geometry('600x440')
        self.initial_window.resizable(False, False)
        utilities.center(self.initial_window)
        program_description_frame = Frame(self.initial_window, height=430, width=180)
        program_title = Label(program_description_frame, text='GTSTRUDL Data Extraction Tool',
                              font=('Helvetica', 12, 'bold'), wraplength=160, justify='center')
        program_description = Label(program_description_frame, text=f'GTSTRUDL Data Extraction Tool was developed'
                                                                    f' to provide a means of parsing GTSTRUDL'
                                                                    f' output files (.gto) for analysis results'
                                                                    f' commonly used in structural analysis '
                                                                    f' calculations and reports.\n'
                                                                    f'\n'
                                                                    f'This program allows the user to choose specific'
                                                                    f' criteria for which the .gto file should be parsed'
                                                                    f' and output'
                                                                    f' that data as either a comma separated value file'
                                                                    f' or as an excel workbook with each set of'
                                                                    f' desired data stored in a separate worksheet.',
                                    wraplength=160, justify='center')
        program_version = Label(program_description_frame, text='Version: 0.2.1')
        program_developer = Label(program_description_frame, text='Developed by Jesse Wagoner')
        program_dev_date = Label(program_description_frame, text='3/22/2022')
        program_description_frame.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky='nsew')
        program_description_frame.grid_propagate(0)
        program_title.grid(row=0, column=0)
        program_version.grid(row=1, column=0)
        program_developer.grid(row=2, column=0)
        program_dev_date.grid(row=3, column=0)
        program_description.grid(row=4, column=0)

        banner = Frame(self.initial_window, height=160, width=390)
        banner.picture = PhotoImage(file="Supporting Documents/Banner.png")
        banner.grid(row=0, column=1, pady=(10, 5), padx=(0, 10), sticky='n')
        Label(banner, image=banner.picture).grid(row=0, column=0, sticky='n')
        banner.grid_propagate(0)

        set_directory_frame = LabelFrame(self.initial_window, text='Select Directory & File', height=190, width=390)
        set_directory_frame.grid(row=1, column=1, pady=(5, 5), padx=(0, 10), sticky='n')
        dir_label = Label(set_directory_frame, text='Select working directory.\n'
                                                    '(default save location for all files)')
        dir_label.grid(row=0, column=0, columnspan=1, pady=5, padx=5, sticky='nw')
        set_directory_frame.grid_propagate(0)
        self.show_dir = Text(set_directory_frame, height=1, width=50, font=('Arial', 10), wrap=NONE)
        dir_scrollx = Scrollbar(set_directory_frame)
        dir_scrollx.configure(command=self.show_dir.xview, orient=HORIZONTAL)
        self.show_dir.configure(xscrollcommand=dir_scrollx.set)
        dir_scrollx.grid(row=2, column=0, columnspan=2, sticky='sew')
        self.show_dir.grid(row=1, column=0, columnspan=2, sticky='nw')
        self.show_dir.config(state='disabled')

        self.show_file = Text(set_directory_frame, height=1, width=50, font=('Arial', 10), wrap=NONE)
        self.show_file.grid(row=4, column=0, columnspan=2, sticky='nw')
        self.show_file.config(state='disabled')
        file_scrollx = Scrollbar(set_directory_frame)
        file_scrollx.configure(command=self.show_file.xview, orient=HORIZONTAL)
        self.show_file.configure(xscrollcommand=file_scrollx.set)
        file_scrollx.grid(row=5, column=0, columnspan=2, sticky='sew')

        select_file = Label(set_directory_frame, text='Select .gto file to parse')
        select_file.grid(row=3, column=0, pady=10, sticky='nw')

        continue_frame = Frame(self.initial_window, height=50, width=390)
        continue_frame.grid(row=2, column=1, pady=(5, 10), padx=(0, 10), sticky='se')

        exit_button = Button(continue_frame, text="Exit", command=self.initial_window.quit)
        exit_button.grid(row=0, column=1, padx=5, pady=5)
        help_button = Button(continue_frame, text='Help (?)', command=help_doc)
        help_button.grid(row=0, column=0, padx=5, pady=5)
        dir_open = Button(set_directory_frame, text="Select Dir.", command=lambda: (self.select_dir(),
                                                                                    self.check_continue()))
        dir_open.grid(row=0, column=1, pady=5, padx=0, sticky='ne')
        file_open = Button(set_directory_frame, text="Select File", command=lambda: (self.select_file(),
                                                                                     self.check_continue()))
        file_open.grid(row=3, column=1, pady=10, padx=0, sticky='ne')
        self.continue_button = Button(continue_frame, text='Continue', command=self.tab_window_generate)
        self.continue_button.grid(row=0, column=2, padx=5, pady=5)
        self.continue_button['state'] = 'disabled'

    def select_dir(self):
        """
        prompts the user to select a working directory
        """
        directory = filedialog.askdirectory()
        self.results.directory = directory
        self.show_dir.config(state='normal')
        self.show_dir.delete('1.0', END)
        self.show_dir.insert(END, directory)
        self.show_dir.config(state='disabled')

    def select_file(self):
        """
        prompts user to select .gto file to parse from working directory
        """
        try:
            input_file_path = filedialog.askopenfilename(initialdir=self.results.directory, title="select file",
                                                         filetypes=load_file_types)
            input_file_name = os.path.basename(input_file_path)
            self.results.input_file = input_file_path
            self.show_file.config(state='normal')
            self.show_file.delete('1.0', END)
            self.show_file.insert(END, input_file_name)
            self.show_file.config(state='disabled')
        except NameError:
            error_handling.ErrorHandling(self.initial_window).no_directory()

    def check_continue(self):
        """
        sets the stats of the continue button. Status is enabled if both the directory and .gto file have been selected
        disabled otherwise.
        """
        if self.show_dir.get("1.0", END) != '\n' and self.show_file.get("1.0", END) != '\n':
            self.continue_button['state'] = 'enabled'
            self.initial_window.bind('<Return>', (lambda event, : self.continue_button.invoke()))
        else:
            self.continue_button['state'] = 'disabled'

    def tab_window_generate(self):
        """
        generates the three tab windows corresponding to the type of results which can be parsed through this program
        """
        if not error_handling.is_valid_mem_force(self.results.input_file, 'OUTPUT BY MEMBER'):
            error_handling.ErrorHandling(self.initial_window).no_output_by_member()
        else:
            height = 370
            width = 600
            tab_window = Toplevel(self.initial_window)
            tab_window.geometry('600x440')
            utilities.center(tab_window)
            tab_window.resizable(False, False)

            my_notebook = Notebook(tab_window)
            my_notebook.pack()

            member_force_frame = Frame(my_notebook, width=width, height=height)
            joint_reaction_frame = Frame(my_notebook, width=width, height=height)
            code_check_frame = Frame(my_notebook, width=width, height=height)
            navigate_frame = Frame(tab_window, width=width, height=50)

            member_force_frame.grid(row=0, column=0, sticky='n')
            joint_reaction_frame.grid(row=0, column=0, sticky='n')
            code_check_frame.grid(row=0, column=0, sticky='n')
            navigate_frame.pack(side='right', padx=(0, 10))

            member_force_frame.grid_propagate(0)
            joint_reaction_frame.grid_propagate(0)
            code_check_frame.grid_propagate(0)

            my_notebook.add(member_force_frame, text='Member Forces')
            my_notebook.add(joint_reaction_frame, text='Joint Reactions')
            my_notebook.add(code_check_frame, text='Code Check')

            back_button = Button(navigate_frame, text="Back", command=lambda: (self.initial_window.deiconify(),
                                                                               tab_window.destroy(), self.reset()))
            help_button = Button(navigate_frame, text='Help (?)', command=help_doc)
            exit_button = Button(navigate_frame, text='Exit', command=self.initial_window.quit)

            help_button.grid(row=0, column=0, padx=5, pady=5)
            exit_button.grid(row=0, column=1, padx=5, pady=5)
            back_button.grid(row=0, column=2, padx=5, pady=5)

            self.initial_window.withdraw()

            frame_display_window.GenerateTab(member_force_frame, 'Member Force', self.initial_window,
                                             self.results.input_file)
            frame_display_window.GenerateTab(joint_reaction_frame, 'Joint Reaction', self.initial_window,
                                             self.results.input_file)
            frame_display_window.GenerateTab(code_check_frame, 'Code Check', self.initial_window,
                                             self.results.input_file)

    def reset(self):
        """
        resets the stored results data when the user exits out to the landing window
        """
        self.results.reset()

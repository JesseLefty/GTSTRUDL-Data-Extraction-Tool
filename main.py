from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import os
import member_force_GUI
import joint_reactions_GUI
import error_handling
import utilities_GUI


def help_doc():
    # open some help documentation
    pass


class FirstWindow:

    def __init__(self, initial_window):
        self.initial_window = initial_window

        self.initial_window.title("GTSTRUDL Data Extraction Tool")
        self.initial_window.geometry('600x440')
        self.initial_window.resizable(False, False)
        utilities_GUI.center(self.initial_window)
        program_description_frame = Frame(self.initial_window, height=430, width=180)
        program_title = Label(program_description_frame, text='GTSTRUDL Data Extraction Tool', font=('Helvetica', 12),
                              wraplength=160, justify='center')
        program_description = Label(program_description_frame, text=f'GTSTRUDL Data Extraction Tool was developed'
                                                                    f' to provide a means of parsing a GTSTRUDL Version'
                                                                    f' 2016 output file (.gto) for analysis results'
                                                                    f' commonly used for structural analysis '
                                                                    f' calculations and reports.\n'
                                                                    f'\n'
                                                                    f'This program allows the user to select specific'
                                                                    f' data contained within the .gto file and output'
                                                                    f' that data as either a comma separated value file'
                                                                    f' or as an excel workbook with each set of'
                                                                    f' desired data stored in a separate worksheet.',
                                    wraplength=160, justify='center')
        program_version = Label(program_description_frame, text='Version: 0.1.2')
        program_developer = Label(program_description_frame, text='Developed by Jesse Wagoner')
        program_dev_date = Label(program_description_frame, text='3/04/2022')
        program_description_frame.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky='nsew')
        program_description_frame.grid_propagate(0)
        program_title.grid(row=0, column=0)
        program_version.grid(row=1, column=0)
        program_developer.grid(row=2, column=0)
        program_dev_date.grid(row=3, column=0)
        program_description.grid(row=4, column=0)

        banner = Frame(self.initial_window, height=160, width=390)
        banner.grid(row=0, column=1, pady=(10, 5), padx=(0, 10), sticky='n')
        banner_text = Label(banner, text='Future Banner Of Some Sort')
        banner_text.grid(row=0, column=0, sticky='n')
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
        dir_open = Button(set_directory_frame, text="Select New", command=lambda: self.select_dir())
        dir_open.grid(row=0, column=1, pady=5, padx=0, sticky='ne')
        file_open = Button(set_directory_frame, text="Select File", command=lambda: self.select_file())
        file_open.grid(row=3, column=1, pady=10, padx=0, sticky='ne')
        self.continue_button = Button(continue_frame, text='Continue', command=tab_window_generate)
        self.continue_button.grid(row=0, column=2, padx=5, pady=5)
        self.continue_button['state'] = 'disabled'

        self.show_file.bind('<<Modified>>', lambda event, : self.check_continue())
        self.show_dir.bind('<<Modified>>', lambda event, : self.check_continue())

    def select_dir(self):
        global directory
        directory = filedialog.askdirectory()
        self.show_dir.config(state='normal')
        self.show_dir.delete('1.0', END)
        self.show_dir.insert(END, directory)
        self.show_dir.config(state='disabled')

    def select_file(self):
        global input_file_path
        file_types = [('*.gto - GTSTRUDL Output', '*.gto'), ('*.txt - Text Files', '*.txt')]
        try:
            input_file_path = filedialog.askopenfilename(initialdir=directory, title="select file", filetypes=file_types)
            input_file_name = os.path.basename(input_file_path)
            self.show_file.config(state='normal')
            self.show_file.delete('1.0', END)
            self.show_file.insert(END, input_file_name)
            self.show_file.config(state='disabled')
        except NameError:
            error_handling.ErrorHandling(initial_window).no_directory()

    def check_continue(self):
        if self.show_dir.get("1.0", END) and self.show_file.get("1.0", END) != '\n':
            self.continue_button['state'] = 'enabled'
            self.initial_window.bind('<Return>', (lambda event, : self.continue_button.invoke()))


def tab_window_generate():

    tab_window = Toplevel(initial_window)
    tab_window.geometry('600x440')
    utilities_GUI.center(tab_window)
    tab_window.resizable(False, False)

    my_notebook = Notebook(tab_window)
    my_notebook.pack()

    member_force_frame = Frame(my_notebook, width=600, height=370)
    joint_reaction_frame = Frame(my_notebook, width=600, height=370)
    member_ir_frame = Frame(my_notebook, width=600, height=370)
    joint_disp_frame = Frame(my_notebook, width=600, height=370)
    section_forces_frame = Frame(my_notebook, width=600, height=370)
    navigate_frame = Frame(tab_window, width=600, height=50)

    member_force_frame.grid(row=0, column=0, sticky='n')
    joint_reaction_frame.grid(row=0, column=0, sticky='n')
    member_ir_frame.grid(row=0, column=0, sticky='n')
    joint_disp_frame.grid(row=0, column=0, sticky='n')
    section_forces_frame.grid(row=0, column=0, sticky='n')
    navigate_frame.pack(side='right', padx=(0, 10))

    member_force_frame.grid_propagate(0)
    joint_reaction_frame.grid_propagate(0)
    member_ir_frame.grid_propagate(0)
    joint_disp_frame.grid_propagate(0)
    section_forces_frame.grid_propagate(0)

    my_notebook.add(member_force_frame, text='Member Forces')
    my_notebook.add(joint_reaction_frame, text='Joint Reactions')
    my_notebook.add(member_ir_frame, text='Code Check')
    my_notebook.add(joint_disp_frame, text='Joint Displacements')
    my_notebook.add(section_forces_frame, text='Section Forces')

    back_button = Button(navigate_frame, text="Back", command=lambda: [initial_window.deiconify(),
                                                                       tab_window.destroy()])
    help_button = Button(navigate_frame, text='Help (?)', command=help_doc)
    exit_button = Button(navigate_frame, text='Exit', command=initial_window.quit)

    help_button.grid(row=0, column=0, padx=5, pady=5)
    exit_button.grid(row=0, column=1, padx=5, pady=5)
    back_button.grid(row=0, column=2, padx=5, pady=5)

    initial_window.withdraw()
    member_force_GUI.MemberForceFrame(member_force_frame, initial_window, directory, input_file_path).main_tab()
    joint_reactions_GUI.JointReactionsFrame(joint_reaction_frame, initial_window, directory, input_file_path).main_tab()

if __name__ == '__main__':
    initial_window = Tk()
    FirstWindow(initial_window)
    initial_window.mainloop()

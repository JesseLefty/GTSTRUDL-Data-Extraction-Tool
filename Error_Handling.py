from tkinter import *
from tkinter.ttk import *


class ErrorHandling:

    def __init__(self, initial_window):
        self.initial_window = initial_window
        self.error_window = Toplevel(self.initial_window)
        self.error_window.geometry('300x200')
        self.initial_window.eval(f'tk::PlaceWindow {str(self.error_window)} center')
        self.error_window.minsize(width=300, height=200)
        self.error_window.title("ERROR!")
        self.error_top_frame = Frame(self.error_window, width=300, height=40)
        self.error_top_frame.grid(row=0, column=0, sticky='n')
        self.error_top_frame.grid_propagate(0)
        self.error_bottom_frame = Frame(self.error_window, width=300, height=40)
        self.error_bottom_frame.grid(row=2, column=0, sticky='s')
        self.error_bottom_frame.grid_propagate(0)
        self.error_mid_frame = Frame(self.error_window, width=300, height=105)
        self.error_mid_frame.grid(row=1, column=0, sticky='nesw')
        self.error_mid_frame.grid_propagate(0)

        mid_style = Style()
        mid_style.configure('mid_frame.TFrame', background='white')

        self.label_style = Style()
        self.label_style.configure('mid.TLabel', background='white')

        self.error_mid_frame.configure(style='mid_frame.TFrame')
        exit_button = Button(self.error_bottom_frame, text='OK', command=lambda: self.error_window.destroy())
        exit_button.pack(pady=15)

        error_top_label = Label(self.error_top_frame, text='!! ERROR !!', justify='center', font='helvetica 20')
        error_top_label.pack()

    def no_selection(self, item_type):
        Label(self.error_mid_frame, text=f'No {item_type} is selected. Please select a {item_type}', wraplength=280,
              justify='left', style='mid.Tlabel').pack()

    def item_not_found(self, item):
        text_label_top = Label(self.error_mid_frame, style='mid.TLabel', wraplength=280, justify='left',
                           text=f'The following result set have incorrect inputs:')
        text_label_top.grid(row=0, column=0, sticky='w', padx=(10, 10))
        text_label_bot = Label(self.error_mid_frame, style='mid.TLabel', wraplength=280, justify='left',
                               text=f'This is generally means the requested'
                                    f' beam spec or load spec cannot be found in the file. Please check your inputs'
                                    f' carefully to ensure everything has been entered properly')
        text_label_bot.grid(row=2, column=0, sticky='w', padx=(10, 10))
        list_label = Label(self.error_mid_frame, style='mid.TLabel', text=f'{", ".join(str(e) for e in item)}')
        list_label.grid(row=1, column=0, sticky='n', padx=(10, 10))

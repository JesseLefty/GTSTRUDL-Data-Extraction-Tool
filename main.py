"""
Generates the Tkinter main loop and initializes ResultsParameters
"""
from tkinter import *
from Tools.data_storage import ResultsParameters
from Tools import shared_stuff
from GUI.landing_window import FirstWindow

if __name__ == '__main__':
    shared_stuff.data_store = ResultsParameters()
    initial_window = Tk()
    FirstWindow(initial_window).win_display()
    initial_window.mainloop()

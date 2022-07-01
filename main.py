"""
Generates the Tkinter main loop and initializes ResultsParameters
"""
from tkinter import *
from Tools.data_storage import ResultsParameters
from Tools import shared_stuff
from GUI.landing_window import FirstWindow

import time
try:
    import pyi_splash
    time.sleep(2)
    pyi_splash.update_text('Complete')
    time.sleep(1)
    pyi_splash.close()

except:
    pass

if __name__ == '__main__':
    shared_stuff.data_store = ResultsParameters()
    initial_window = Tk()
    FirstWindow(initial_window).win_display()
    initial_window.mainloop()

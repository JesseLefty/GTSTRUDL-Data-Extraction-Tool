"""
This module contains a collection of utilities commonly used in the program
"""
from tkinter import *
from tkinter.ttk import *


def center(win, x_offset=0, y_offset=0):
    """
    Centers a tkinter window
        Parameters:
            win: the main window or Toplevel window to center
            x_offset: option offset for x coordinate
            y_offset: optional offset for y coordinate
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = (win.winfo_screenwidth() // 2 - win_width // 2) + x_offset
    y = (win.winfo_screenheight() // 2 - win_height // 2) + y_offset
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


class ReadInputFile:
    """
    Reads .gto file and returns each row in file as element in list
        Parameters:
            input_file: .gto file selected to parse
    """
    def __init__(self, input_file):
        self.input_file = input_file

    def file_list(self):
        with open(self.input_file, 'r') as f:
            file_as_list = []
            for lines in f:
                file_as_list.append(lines.rstrip())
        return file_as_list


class CreateToolTip(object):
    """
    create a tooltip for a given widget

    parameters:
        widget:     tkinter widget to which the tool tip is attached
        text:       text to display on tool tip
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength= self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class GenerateDisplayData:
    """
    Generates data to display in the "available results" window
        Parameters:
            input_file: .gto file selected to parse
    """
    def __init__(self, input_file):
        self.input_file = input_file
        self.file_list = ReadInputFile(input_file).file_list()

    def get_display(self, tab_name):
        """
        Generates data to display in the "available results" window
            Parameters:
                self

            Returns:
                result (list): list containing the lines with the trigger string
                index (list):  list containing the GTSTRUDL output line number
        """
        if tab_name == 'Member Force':
            trigger_string = 'LIST FOR'
            result = [row for row in self.file_list if trigger_string in row]
            index = [v[:v.find("}") + 1].lstrip() for v in result]
            result = [v[v.find(trigger_string):] for v in result]

        elif tab_name == 'Joint Reaction':
            trigger_string = 'RESULTANT JOINT LOADS SUPPORTS'
            index_string = 'LIST REA'
            index = [row for row in self.file_list if index_string in row]
            index = [v[:v.find("}") + 1].lstrip() for v in index]
            result = [row for row in self.file_list if trigger_string in row]
            result = [v[v.find(trigger_string):] for v in result]

        else:
            trigger_string = 'DESIGN TRACE OUTPUT'
            result = []
            index = []
            for idx, row in enumerate(self.file_list):
                if trigger_string in row:
                    display_text = self.file_list[idx - 4]
                    text = display_text[display_text.find(">") + 2:]
                    line_num = display_text[:display_text.find("}") + 1].lstrip()
                    index.append(line_num)
                    result.append(text)
                else:
                    pass

        return result, index


class TupleDict(dict):
    """
    Rebuilds a dictionary which allows searching a key of type tuple for any value. If any item in the tuple matches the
    requested value, the entire key is returned.

            Parameters:
                dict:   dictionary which is to be converted to searchable

            Returns:    a dictionary which has a searchable tuple key
    """
    def __contains__(self, key):
        if super(TupleDict, self).__contains__(key):
            return True
        return any(key in k for k in self)

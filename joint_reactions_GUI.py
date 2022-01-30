from tkinter import *
from tkinter.ttk import *


class JointReactionsFrame:

    def __init__(self, joint_reaction_frame, initial_window, directory, input_file_path, modify=False):

        self.replace = modify
        self.joint_reaction_frame = joint_reaction_frame
        self.initial_window = initial_window
        self.directory = directory
        self.input_file_path = input_file_path

    def main_tab(self):
        Label(self.joint_reaction_frame, text="In Development").pack()

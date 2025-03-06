##############################################################################
# FILE: boggle.py
# EXERCISE: Intro2cs ex12 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash, Samuel Hayat [REDACTED]
# DESCRIPTION: this is the main file for the boggle game
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
##############################################################################

import tkinter
from boggle_controller import Controller


def main():

    root = tkinter.Tk()
    root.resizable(width=False, height=False)

    controller = Controller(root)
    controller.initial_display()

    root.mainloop()

if __name__ == '__main__':
    main()
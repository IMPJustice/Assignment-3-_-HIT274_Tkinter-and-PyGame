"""
    Application: Tic Tac Toe 1v1
    Date: 18th Oct 2024
    Author: Phuong Trinh Vu, Jay Nguyen
    Github Repo: https://github.com/IMPJustice/Assignment-3-_-HIT274_Tkinter-and-PyGame.git
    
"""

import tkinter as tk
from function import MainMenu
from backgr import BlurredBackground

if __name__ == "__main__":
    root = tk.Tk()

    #Initialize the main menu on top of the background
    app = MainMenu(root)

    root.mainloop()

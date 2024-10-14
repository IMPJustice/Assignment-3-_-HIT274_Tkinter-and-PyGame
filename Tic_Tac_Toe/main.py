"""
    Application: Tic Tac Toe 1v1
    Date: 18th Oct 2024
    Author: Phuong Trinh Vu, Jay Nguyen
    Github Repo: https://github.com/IMPJustice/Assignment-3-_-HIT274_Tkinter-and-PyGame.git
    
"""

import tkinter as tk
from function import MainMenu
from backgr import BlurredBackgroundApp

if __name__ == "__main__":
    root = tk.Tk()

    #Set the blurred background image
    backgr_img = "background.png"
    backgr_app = BlurredBackgroundApp(root, backgr_img)
    
    app = MainMenu(root)
    root.mainloop()

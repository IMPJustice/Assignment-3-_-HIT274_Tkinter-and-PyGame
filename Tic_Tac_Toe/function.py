import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self, root, size):
        self.root = root
        self.size = size
        self.root.title(f"Tic Tac Toe {size}x{size}")
        
        #Initialize variables
        self.player_turn = "X"
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        
        #Scaling the game with the window
        for i in range(size):
            #Rows resizable
            self.root.grid_rowconfigure(i, weight=1)
            #Columns resizable
            self.root.grid_columnconfigure(i, weight=1)
        #Create UI for the Tic Tac Toe grid and quit button
        self.create_widgets()

        #Add menu with Quit option
        self.create_menu()

    #Tkinter
    def create_widgets(self):
        #Create grid of buttons dynamically based on the size selected
        for i in range(self.size):
            for j in range(self.size):
                button = tk.Button(self.root, text="", font=('Arial', 20), width=5, height=2,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                #Button fill the grid cell and stretch
                button.grid(row=i, column=j, sticky="nsew")
                self.buttons[i][j] = button
                
    #Window taskbar
    def create_menu(self):
        #Menu bar
        menubar = tk.Menu(self.root)

        #Game menu
        game_menu = tk.Menu(menubar, tearoff=0)
        #Add Quit option
        game_menu.add_command(label="Quit", command=self.root.quit)

        #Add the Game menu to the menu bar
        menubar.add_cascade(label="Game", menu=game_menu)

        #Set the menu bar as the window taskbar
        self.root.config(menu=menubar)

    #Button check
    def on_button_click(self, row, col):
        #Check if the button is already clicked
        if self.buttons[row][col]['text'] == "":
            #Place player's symbol on the button
            self.buttons[row][col]['text'] = self.player_turn

            #Check for a winner after the move
            if self.check_winner():
                messagebox.showinfo("Game Over!", f"Player {self.player_turn} wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Game Over!", "It's a draw!")
                self.reset_board()
            else:
                #Switch turn: "X" irst then "O"
                self.player_turn = "O" if self.player_turn == "X" else "X"

    #Winning condition check
    def check_winner(self):
        #Check rows, columns, and diagonals for winning condition
        for i in range(self.size):
            if all(self.buttons[i][j]['text'] == self.player_turn for j in range(self.size)):
                return True
            if all(self.buttons[j][i]['text'] == self.player_turn for j in range(self.size)):
                return True

        if all(self.buttons[i][i]['text'] == self.player_turn for i in range(self.size)):
            return True
        if all(self.buttons[i][self.size - i - 1]['text'] == self.player_turn for i in range(self.size)):
            return True

        return False

    #Draw check
    def check_draw(self):
        return all(self.buttons[i][j]['text'] != "" for i in range(self.size) for j in range(self.size))

    #Continue playing until choose "Quit" from "Game"
    def reset_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j]['text'] = ""
        self.player_turn = "X"


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe Menu")
        self.root.geometry("400x300")

        self.create_widgets()

    #Create application menu
    def create_widgets(self):
        #Application title
        title_label = tk.Label(self.root, text="Welcome to Tic Tac Toe!", font=('Arial', 18, 'bold'))
        title_label.pack(pady=20)
        
        #Start game option
        start_button = tk.Button(self.root, text="1. Start the Game", font=('Arial', 14), command=self.start_game_menu)
        start_button.pack(pady=10)

        #Rules option
        rules_button = tk.Button(self.root, text="2. Rules", font=('Arial', 14), command=self.show_rules)
        rules_button.pack(pady=10)

        #Exit the application
        quit_button = tk.Button(self.root, text="3. Quit", font=('Arial', 14), command=self.root.quit)
        quit_button.pack(pady=10)

    #Generate game window
    def start_game_menu(self):
        #Destroy the main menu window
        self.root.destroy()

        #Open a new window to choose the game board size
        size_window = tk.Tk()
        size_window.title("Choose Board Size")
        size_window.geometry("400x300")

        tk.Label(size_window, text="Choose board size:", font=('Arial', 14)).pack(pady=10)

        #3x3 Game
        size_3x3_button = tk.Button(size_window, text="3x3", font=('Arial', 14),
                                    command=lambda: self.start_game(size_window, 3))
        size_3x3_button.pack(pady=5)

        #5x5 Game
        size_5x5_button = tk.Button(size_window, text="5x5", font=('Arial', 14),
                                    command=lambda: self.start_game(size_window, 5))
        size_5x5_button.pack(pady=5)

        #7x7 Game
        size_7x7_button = tk.Button(size_window, text="7x7", font=('Arial', 14),
                                    command=lambda: self.start_game(size_window, 7))
        size_7x7_button.pack(pady=5)

    #Close the main menu and start the game
    def start_game(self, size_window, size):
        #Destroy window
        size_window.destroy()

        #Open the Tic Tac Toe game window
        game_window = tk.Tk()
        app = TicTacToe(game_window, size)

    #Rules display
    def show_rules(self):
        rules_message = """
        Tic Tac Toe Rules:
        
        3x3 Game:
        - The player who succeeds in placing three of their marks in a horizontal, vertical, or diagonal row wins.

        5x5 and 7x7 Game:
        - The player who succeeds in placing four of their marks in a horizontal, vertical, or diagonal row wins.

        Enjoy the game!
        """
        messagebox.showinfo("Tic Tac Toe Rules", rules_message)

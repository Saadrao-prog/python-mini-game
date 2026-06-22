import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeComputer:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe (vs Computer) - saad")
        self.human = "X"
        self.computer = "O"
        self.board = [""] * 9
        self.buttons = []
        self.create_board()

    def create_board(self):
        for i in range(9):
            btn = tk.Button(self.root, text="", font=('Arial', 24, 'bold'), width=5, height=2,
                            command=lambda idx=i: self.human_click(idx), bg="#f0f0f0")
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

    def human_click(self, idx):
        # Agar box khali hai aur koi jeeta nahi hai
        if self.board[idx] == "" and not self.check_winner(self.human) and not self.check_winner(self.computer):
            self.make_move(idx, self.human, "#ff4757")
            
            if self.check_game_over():
                return
                
            # Human ki chal ke foran baad Computer khelega
            self.root.after(500, self.computer_move)

    def computer_move(self):
        # Khali dabbas (empty spaces) dhoondo
        empty_squares = [i for i, spot in enumerate(self.board) if spot == ""]
        
        if empty_squares:
            # AI Logic: Pehle check karo agar computer khud jeet raha hai to chal chalay
            for move in empty_squares:
                self.board[move] = self.computer
                if self.check_winner(self.computer):
                    self.make_move(move, self.computer, "#2ed573")
                    self.check_game_over()
                    return
                self.board[move] = ""

            # 2. Check karo agar human jeet raha hai to uski chal block kare
            for move in empty_squares:
                self.board[move] = self.human
                if self.check_winner(self.human):
                    self.board[move] = "" # Undo text simulation
                    self.make_move(move, self.computer, "#2ed573")
                    self.check_game_over()
                    return
                self.board[move] = ""

            # 3. Agar kuch baki nahi to random chal chale
            move = random.choice(empty_squares)
            self.make_move(move, self.computer, "#2ed573")
            self.check_game_over()

    def make_move(self, idx, player, color):
        self.board[idx] = player
        self.buttons[idx].config(text=player, fg=color)

    def check_winner(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]
        return any(all(self.board[i] == player for i in cond) for cond in win_conditions)

    def check_game_over(self):
        if self.check_winner(self.human):
            messagebox.showinfo("Game Over", "Wah! Aap Jeet Gaye! 🎉")
            self.reset_board()
            return True
        elif self.check_winner(self.computer):
            messagebox.showinfo("Game Over", "Computer Jeet Gaya! 🤖")
            self.reset_board()
            return True
        elif "" not in self.board:
            messagebox.showinfo("Game Over", "Match Draw Ho Gaya! 🤝")
            self.reset_board()
            return True
        return False

    def reset_board(self):
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="", bg="#f0f0f0")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeComputer(root)
    root.mainloop()
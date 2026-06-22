import tkinter as tk
from tkinter import messagebox
import chess
import random

class ChessAI_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess vs Computer AI - saad")
        self.board = chess.Board()
        self.selected_square = None
        self.buttons = {}
        self.create_board()
        self.update_board()

    def create_board(self):
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                color = "#eeeed2" if (row + col) % 2 == 0 else "#769656"
                btn = tk.Button(self.root, text="", font=('Arial', 18, 'bold'), width=4, height=2,
                                bg=color, command=lambda s=square: self.square_clicked(s))
                btn.grid(row=row, column=col)
                self.buttons[square] = btn

    def update_board(self):
        unicode_pieces = {
            'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
            'r': '♖', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔', 'p': '♙'
        }
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                self.buttons[square].config(text=unicode_pieces[piece.symbol()])
            else:
                self.buttons[square].config(text="")

    def square_clicked(self, square):
        # Agar game khatam ho chuki hai to click na ho
        if self.board.is_game_over():
            return

        # White (Human) ki turn hai
        if self.board.turn == chess.WHITE:
            if self.selected_square is None:
                if self.board.piece_at(square) and self.board.piece_at(square).color == chess.WHITE:
                    self.selected_square = square
                    self.buttons[square].config(bg="#baca44") # Highlight selected
            else:
                move = chess.Move(self.selected_square, square)
                
                # Check for pawn promotion automatically to Queen
                if chess.Move(self.selected_square, square, chess.QUEEN) in self.board.legal_moves:
                    move = chess.Move(self.selected_square, square, chess.QUEEN)

                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.update_board()
                    
                    # Reset original color of selected square
                    row1, col1 = 7 - chess.square_rank(self.selected_square), chess.square_file(self.selected_square)
                    orig_color = "#eeeed2" if (row1 + col1) % 2 == 0 else "#769656"
                    self.buttons[self.selected_square].config(bg=orig_color)
                    self.selected_square = None

                    if self.check_game_status():
                        return

                    # Human ki move ke baad Computer khelega (0.5 second ke pause ke sath)
                    self.root.after(500, self.make_computer_move)
                else:
                    # Invalid move par highlight reset karein
                    row1, col1 = 7 - chess.square_rank(self.selected_square), chess.square_file(self.selected_square)
                    orig_color = "#eeeed2" if (row1 + col1) % 2 == 0 else "#769656"
                    self.buttons[self.selected_square].config(bg=orig_color)
                    self.selected_square = None

    # AI Evaluation Function (Pieces ko unki power ke hisab se numbers deta hai)
    def evaluate_board(self):
        piece_values = {
            chess.PAWN: 10, chess.KNIGHT: 30, chess.BISHOP: 30,
            chess.ROOK: 50, chess.QUEEN: 90, chess.KING: 9000
        }
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                if piece.color == chess.BLACK:
                    score += value
                else:
                    score -= value
        return score

    # Minimax AI Algorithm with Alpha-Beta Pruning
    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board()

        if maximizing_player:
            max_eval = -99999
            for move in self.board.legal_moves:
                self.board.push(move)
                evaluation = self.minimax(depth - 1, alpha, beta, False)
                self.board.pop()
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = 99999
            for move in self.board.legal_moves:
                self.board.push(move)
                evaluation = self.minimax(depth - 1, alpha, beta, True)
                self.board.pop()
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def make_computer_move(self):
        best_move = None
        best_value = -99999
        alpha = -99999
        beta = 99999

        # Best move dhoondne ke liye loop (Depth = 2 tak check karega fast process ke liye)
        for move in self.board.legal_moves:
            self.board.push(move)
            board_value = self.minimax(2, alpha, beta, False)
            self.board.pop()
            if board_value > best_value:
                best_value = board_value
                best_move = move

        if best_move:
            self.board.push(best_move)
            self.update_board()
            self.check_game_status()

    def check_game_status(self):
        if self.board.is_checkmate():
            if self.board.turn == chess.WHITE:
                messagebox.showinfo("Game Over", "Checkmate! Computer Jeet Gaya. 🤖")
            else:
                messagebox.showinfo("Game Over", "Wah! Checkmate! Aap Jeet Gaye. 🎉")
            return True
        elif self.board.is_game_over():
            messagebox.showinfo("Game Over", "Match Draw Ho Gaya! 🤝")
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = ChessAI_GUI(root)
    root.mainloop()
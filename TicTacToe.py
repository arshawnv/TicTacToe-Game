import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

DEFAULT_PLAYERS = (Player(label = 'X', color = 'blue'),Player(label = 'O',color = 'green'))
BOARD_SIZE = 3

class TicTacToeGame:
    def __init__(self, players = DEFAULT_PLAYERS, board_size = BOARD_SIZE ):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [[Move(row,col) for col in range(self.board_size)] for row in range(self.board_size)]
        self._winning_combos = self._get_winning_combos()
    
    def _get_winning_combos(self):
        rows = [[(move.row,move.col) for move in row]for row in self._current_moves]
        columns = [list(col) for col in zip(*rows)]
        diagonal1 = [row[i] for i,row in enumerate(rows)]
        diagonal2 = [col[j] for j,col in enumerate(reversed(columns))]
        return rows + columns + [diagonal1,diagonal2]

    def is_valid_move(self,move):
        row = move.row
        col = move.col
        if self._current_moves[row][col].label == '' and not self._has_winner:
            return True
        else:
            return False
        
    def process_move(self,move):
        row = move.row
        col = move.col
        self._current_moves[row][col] = move

        for combo in self._winning_combos:
            result = set(self._current_moves[n][m].label for n,m in combo)

            win = len(result) == 1 and '' not in result
            if win:
                self._has_winner = True
                self.winner_combo = combo
                break
    def has_winner(self):
        return self._has_winner
    
    def is_tied(self):
        no_winner = not self.has_winner()
        played_moves = (move.label for row in self._current_moves for move in row)
        if no_winner and all(played_moves):
            return True
        else:
            return False
    
    def toggle_player(self):
        self.current_player = next(self._players)
            

        


class TicTacToeBoard(tk.Tk):

    def __init__(self,game):
        super().__init__()
        self.title('TicTacToe')
        self._cells = {}
        self._game = game
        self.createBoard()
        self.createGrid()

    def createBoard(self):
        display_frame = tk.Frame(master=self, )
        display_frame.pack(fill = 'both')
        self.display = tk.Label(master=display_frame,text= "Ready?" ,font= font.Font(family= 'Helvitca',size= 28, weight = 'bold'))
        self.display.pack()

    def createGrid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row,weight=1, minsize=50)
            self.columnconfigure(row,weight=1, minsize = 50)
            for col in range(self._game.board_size):
                button = tk.Button(master = grid_frame,
                                   width = 3,
                                   height=2,
                                   highlightbackground='lightgreen')
                self._cells[button] = (row,col)
                button.bind('<ButtonPress-1>',self.play)
                button.grid(row=row,column = col, padx = 3,pady = 3, sticky= 'nesw' )
    
    def play(self,event):
        clicked_btn = event.widget
        row,col = self._cells[clicked_btn]
        move = Move(row,col,self._game.current_player.label)

        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg ="Tied Game", color =  'red')
            elif self._game.has_winner():
                self._highlight_cells()
                self._update_display(msg = f'Player {self._game.current_player.label} won')
            else:
                self._game.toggle_player()
                self._update_display(msg = f"Player {self._game.current_player.label}'s turn")

    def _update_button(self, clicked_btn):
        clicked_btn.config(text = self._game.current_player.label)
        clicked_btn.config(fg = self._game.current_player.color)
        
    def _update_display(self,msg,color = 'white'):
        self.display['text'] = msg
        self.display['fg'] = color
        
    def _highlight_cells(self):
        for button,coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground = 'red' )


def main():
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == '__main__':
    main()




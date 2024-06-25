import tkinter as tk
from tkinter import font
from common import Player, Move, Opponent, Cell
from itertools import cycle
import json

ROW = 3
COL = 3

DEFAULT_PLAYERS = (Player(label = "X", color = "blue"), Player(label = "O", color = "green"))

class TicTacToeGame:
    def __init__(self, player = DEFAULT_PLAYERS):
        self._players = cycle(player)
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self) -> None:
        for row in range(ROW):
            moves = []
            for col in range(COL):
                moves.append(Move(row, col))
            self._current_moves.append(moves)
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self) -> list:
        rows = []
        for row in self._current_moves:
            moves = []
            for move in row:
                moves.append((move.row, move.col))
            rows.append(moves)
        columns = []
        for col in zip(*rows):
            columns.append(list(col))
        first_diagonal = []
        for i, row in enumerate(rows):
            first_diagonal.append(row[i])
        second_diagonal = []
        for j, col in enumerate(reversed(columns)):
            second_diagonal.append(col[j])
        return rows + columns + [first_diagonal, second_diagonal]
    
    def is_valid_move(self, move: Move) -> bool:
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played
    
    def process_move(self, move: Move) -> None:
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results_list = []
            for i, j in combo:
                results_list.append(self._current_moves[i][j].label)
            results = set(results_list)
            is_win = (len(results) == 1 and ("" not in results))
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break
    
    def has_winner(self) -> bool:
        return self._has_winner
    
    def is_tied(self) -> bool:
        no_winner = not self._has_winner
        played_moves = []
        for row in self._current_moves:
            for move in row:
                played_moves.append(move.label)
        played_moves = tuple(played_moves)

        return no_winner and all(played_moves)

    def toggle_player(self) -> None:
        self.current_player = next(self._players)
    
    def reset_game(self) -> None:
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

        if self.current_player == DEFAULT_PLAYERS[1]:
            # always start with x
            self.current_player = next(self._players)

    def get_board_state(self) -> tuple:
        state = []

        for row in range(ROW):
            for col in range(COL):
                if self._current_moves[row][col].label == "":
                    state.append(Cell.NO_MOVE.value)
                elif self._current_moves[row][col].label == "X":
                    state.append(Cell.X.value)
                elif self._current_moves[row][col].label == "O":
                    state.append(Cell.O.value)

        state = tuple(state)
        return state

class TicTacToeBoard(tk.Tk):
    def __init__(self, game: TicTacToeGame) -> None:
        super().__init__()
        self.title = "Tic Tac Toe"
        self._cells = {}
        self._game = game
        self._player_label = DEFAULT_PLAYERS[0].label
        self._opponent = Opponent.HUMAN
        self._value_iteration_policy = {}
        self._policy_iteration_policy = {}
        self._vi_policy_loaded = False
        self._pi_policy_loaded = False
        self._load_policy()
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _load_policy(self) -> None:
        vi_policy_path = "policies/valueIteration.json"
        pi_policy_path = "policies/policyIteration.json"

        try:
            with open(vi_policy_path, 'r') as json_file:
                self._value_iteration_policy = json.load(json_file)
            self._vi_policy_loaded  = True
        except:
            self._vi_policy_loaded = False
            print("Failed to load value iteration policy")
        
        try:
            with open(pi_policy_path, 'r') as json_file:
                self._policy_iteration_policy = json.load(json_file)
            self._pi_policy_loaded = True
        except: 
            self._pi_policy_loaded = False
            print("Failed to load policy iteration policy")


    def _create_menu(self):
        menu_bar = tk.Menu(master = self)
        self.config(menu = menu_bar)
        file_menu = tk.Menu(master = menu_bar)
        file_menu.add_command(label = "Play Again", command = self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label = "Exit", command=quit)
        menu_bar.add_cascade(label = "File", menu=file_menu)

        settings_menu = tk.Menu(master = menu_bar)
        settings_menu.add_command(label = "Human", command = lambda: self.change_opponent(Opponent.HUMAN))
        settings_menu.add_command(label = "Value Iteration", command = lambda: self.change_opponent(Opponent.VALUE_ITERATION))
        settings_menu.add_command(label = "Policy Iteration", command = lambda: self.change_opponent(Opponent.POLICY_ITERATION))
        menu_bar.add_cascade(label = "Settings", menu=settings_menu)


        player_menu = tk.Menu(master = menu_bar)
        self._player_var = tk.IntVar()
        player_menu.add_radiobutton(label = "x", variable = self._player_var, value = 1, command = self.select_player)
        player_menu.add_radiobutton(label = "o", variable = self._player_var, value = 2, command = self.select_player)
        menu_bar.add_cascade(label = "Player", menu=player_menu)

    def _create_board_display(self) -> None:
        display_frame = tk.Frame(master = self)
        display_frame.pack(fill = tk.X)
        self.display = tk.Label(master = display_frame, text="Ready", font = font.Font(size = 20, weight = "bold"))
        self.display.pack()

    def _create_board_grid(self) -> None:
        grid_frame = tk.Frame(master = self)
        grid_frame.pack()
        for row in range(ROW):
            self.rowconfigure(row, weight = 1, minsize = 50)
            self.columnconfigure(row, weight = 1, minsize = 75)
            for col in range(COL):
                button = tk.Button(master = grid_frame, text = "", font = font.Font(size = 36, weight = "bold"), fg = "black", width = 3, height = 2, highlightbackground = "lightblue")
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row = row, column = col, padx = 5, pady = 5, sticky = "nsew")    

    def _update_button(self, clicked_btn) -> None:
        clicked_btn.config(text = self._game.current_player.label)
        clicked_btn.config(fg = self._game.current_player.color)

    def _update_grid(self, row: int, col: int) -> None:
        for button, coordinates in self._cells.items():
            if coordinates[0] == row and coordinates[1] == col:
                button.config(text = self._game.current_player.label)
                button.config(fg = self._game.current_player.color)

    def _update_display(self, msg: str, color: str = "black") -> None:
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self) -> None:
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo: 
                button.config(highlightbackground = "red")

    
    def play(self, event):
        clicked_btn = event.widget
        if self._game.current_player.label == self._player_label:
            row, col = self._cells[clicked_btn]
            move = Move(row, col, self._game.current_player.label)

            if self._game.is_valid_move(move):
                self._update_button(clicked_btn)
                self._game.process_move(move)

                if self._game.is_tied():
                    self._update_display(msg = "Tied game!", color = "red")
                elif self._game.has_winner():
                    self._highlight_cells()
                    msg = f'Player "{self._game.current_player.label}" won!'
                    color = self._game.current_player.color
                    self._update_display(msg, color)
                else:
                    self._game.toggle_player()
                    msg = f"{self._game.current_player.label}'s turn"
                    self._update_display(msg)

                    if self._opponent != Opponent.HUMAN:
                        self.play_computer()
                    else:
                        self._player_label = self._game.current_player.label

        elif self._opponent != Opponent.HUMAN:
            self.play_computer()
        else:
            self._player_label = self._game.current_player.label

    def play_computer(self):      
        state = self._game.get_board_state()      
        # if computer is O, invert X and O, policy assumes we are always playing X
        if self._game.current_player.label == "O":
            state = tuple(3-cell_state if cell_state != Cell.NO_MOVE.value else Cell.NO_MOVE.value for cell_state in state)

        if self._opponent == Opponent.VALUE_ITERATION:
            index = self._value_iteration_policy[str(state)]
        elif self._opponent == Opponent.POLICY_ITERATION:
            index = self._policy_iteration_policy[str(state)]

        row = index // ROW
        col = index % COL
        move = Move(row, col, self._game.current_player.label)

        if self._game.is_valid_move(move):
            self._update_grid(row, col)
            self._game.process_move(move)

            if self._game.is_tied():
                self._update_display(msg = "Tied game!", color = "red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)  

    def reset_board(self) -> None:
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

    def change_opponent(self, opponent: Opponent) -> None:
        if opponent == Opponent.HUMAN:
            self._opponent = opponent
        elif opponent == Opponent.VALUE_ITERATION:
            if self._vi_policy_loaded:
                self._opponent = opponent
            else:
                print("Unable to find value iteration policy, opponent switch back to HUMAN")
                self._opponent = Opponent.HUMAN
        elif opponent == Opponent.POLICY_ITERATION:
            if self._policy_iteration_policy:
                self._opponent = opponent
            else:
                print("Unable to find policy iteration policy, opponent switch back to HUMAN")
                self._opponent = Opponent.HUMAN

    def select_player(self) -> None:
        if self._player_var.get() == 1:
            self._player_label = DEFAULT_PLAYERS[0].label
        else:
            self._player_label = DEFAULT_PLAYERS[1].label

def main():
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()
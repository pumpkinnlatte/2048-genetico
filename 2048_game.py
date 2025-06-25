import tkinter as tk
import random

CELL_COLORS = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
    4096: "#3c3a32",
}
FONT = ("Verdana", 24, "bold")
BG_COLOR = "#bbada0"

class Game2048GUI(tk.Frame):
    def __init__(self, master=None, size=4):
        super().__init__(master)
        self.master = master
        self.size = size
        self.grid()
        self.master.title("2048 Game")
        self.master.resizable(False, False)
        self.score = 0

        self.board = [[0] * size for _ in range(size)]
        self.cells = []

        self.init_board()
        self.init_game()
        self.bind_keys()

    def init_board(self):
        bg = tk.Frame(self, bg=BG_COLOR, bd=4, width=400, height=400)
        bg.grid(padx=10, pady=10)
        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell = tk.Frame(bg, bg=CELL_COLORS[0], width=100, height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)
                label = tk.Label(cell, text="", bg=CELL_COLORS[0], justify=tk.CENTER, font=FONT, width=4, height=2)
                label.pack()
                row.append(label)
            self.cells.append(row)

    def init_game(self):
        self.add_tile()
        self.add_tile()
        self.update_board()

    def bind_keys(self):
        self.master.bind("<Up>", lambda e: self.move("up"))
        self.master.bind("<Down>", lambda e: self.move("down"))
        self.master.bind("<Left>", lambda e: self.move("left"))
        self.master.bind("<Right>", lambda e: self.move("right"))
        self.master.bind("r", lambda e: self.restart_game())

    def restart_game(self):
        self.board = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.init_game()

    def add_tile(self):
        empty = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def update_board(self):
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                label = self.cells[i][j]
                label.configure(text=str(value) if value else "", bg=CELL_COLORS.get(value, "#3c3a32"))

    def move(self, direction):
        moved = False
        if direction == "left":
            for i in range(self.size):
                moved |= self.merge_row(i)
        elif direction == "right":
            for i in range(self.size):
                self.board[i].reverse()
                moved |= self.merge_row(i)
                self.board[i].reverse()
        elif direction == "up":
            self.transpose()
            for i in range(self.size):
                moved |= self.merge_row(i)
            self.transpose()
        elif direction == "down":
            self.transpose()
            for i in range(self.size):
                self.board[i].reverse()
                moved |= self.merge_row(i)
                self.board[i].reverse()
            self.transpose()

        if moved:
            self.add_tile()
            self.update_board()
            if not self.can_move():
                self.game_over()

    def merge_row(self, i):
        original = [num for num in self.board[i] if num != 0]
        merged = []
        j = 0
        while j < len(original):
            if j + 1 < len(original) and original[j] == original[j + 1]:
                merged.append(original[j] * 2)
                self.score += original[j] * 2
                j += 2
            else:
                merged.append(original[j])
                j += 1
        merged += [0] * (self.size - len(merged))
        if self.board[i] != merged:
            self.board[i] = merged
            return True
        return False

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def can_move(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return True
                if j + 1 < self.size and self.board[i][j] == self.board[i][j + 1]:
                    return True
                if i + 1 < self.size and self.board[i][j] == self.board[i + 1][j]:
                    return True
        return False

    def game_over(self):
        game_over_win = tk.Toplevel(self)
        game_over_win.title("Game Over")
        tk.Label(game_over_win, text="Game Over!", font=("Verdana", 24)).pack(padx=20, pady=10)
        tk.Button(game_over_win, text="Restart", command=lambda: [game_over_win.destroy(), self.restart_game()]).pack(pady=5)
        tk.Button(game_over_win, text="Quit", command=self.master.destroy).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048GUI(root)
    game.mainloop()

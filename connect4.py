import random
import time
import tkinter as tk
from tkinter import ttk

ROWS = 6
COLS = 7
EMPTY = 0
HUMAN = 1
AI = 2

# Coordinates for center-first move ordering; this helps alpha-beta pruning.
COLUMN_ORDER = sorted(range(COLS), key=lambda c: abs(c - (COLS // 2)))
WIN_SCORE = 1_000_000


def new_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def valid_columns(board):
    return [c for c in COLUMN_ORDER if board[0][c] == EMPTY]


def landing_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return -1


def drop_piece(board, col, piece):
    row = landing_row(board, col)
    if row == -1:
        return -1
    board[row][col] = piece
    return row


def undo_piece(board, row, col):
    board[row][col] = EMPTY


def board_full(board):
    return all(board[0][c] != EMPTY for c in range(COLS))


def winning_cells(board, piece):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != piece:
                continue
            for dr, dc in directions:
                cells = []
                for i in range(4):
                    rr = r + dr * i
                    cc = c + dc * i
                    if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == piece:
                        cells.append((rr, cc))
                    else:
                        cells = []
                        break
                if len(cells) == 4:
                    return cells
    return None


def score_window(window, piece):
    opp = AI if piece == HUMAN else HUMAN
    mine = window.count(piece)
    theirs = window.count(opp)
    empty = window.count(EMPTY)

    if mine == 4:
        return 100
    if mine == 3 and empty == 1:
        return 5
    if mine == 2 and empty == 2:
        return 2
    if theirs == 3 and empty == 1:
        return -4
    return 0


def evaluate(board, piece):
    score = 0
    center_col = COLS // 2
    for r in range(ROWS):
        if board[r][center_col] == piece:
            score += 3

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in directions:
                rr = r + 3 * dr
                cc = c + 3 * dc
                if 0 <= rr < ROWS and 0 <= cc < COLS:
                    window = []
                    for i in range(4):
                        window.append(board[r + i * dr][c + i * dc])
                    score += score_window(window, piece)
    return score


def minimax(board, depth, alpha, beta, maximizing, stats):
    stats["nodes"] += 1

    if winning_cells(board, AI):
        return None, WIN_SCORE + depth
    if winning_cells(board, HUMAN):
        return None, -WIN_SCORE - depth

    moves = valid_columns(board)
    if not moves:
        return None, 0
    if depth == 0:
        return None, evaluate(board, AI)

    best_col = moves[0]
    if maximizing:
        value = -float("inf")
        for col in moves:
            row = drop_piece(board, col, AI)
            score = minimax(board, depth - 1, alpha, beta, False, stats)[1]
            undo_piece(board, row, col)
            if score > value:
                value = score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    value = float("inf")
    for col in moves:
        row = drop_piece(board, col, HUMAN)
        score = minimax(board, depth - 1, alpha, beta, True, stats)[1]
        undo_piece(board, row, col)
        if score < value:
            value = score
            best_col = col
        beta = min(beta, value)
        if alpha >= beta:
            break
    return best_col, value


DIFFICULTY = {
    "Easy": [2, 0.30],
    "Medium": [4, 0.0],
    "Hard": [6, 0.0],
}


def choose_ai_move(board, level):
    depth, blunder = DIFFICULTY[level]
    stats = {"nodes": 0, "time": 0.0, "depth": depth}
    start = time.perf_counter()

    if random.random() < blunder:
        moves = valid_columns(board)
        col = random.choice(moves)
    else:
        col, _ = minimax(board, depth, -float("inf"), float("inf"), True, stats)

    stats["time"] = time.perf_counter() - start
    return col, stats


class ConnectFourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four - AI Mini Project")
        self.root.geometry("520x620")
        self.root.resizable(False, False)

        self.score = {"human": 0, "ai": 0, "draw": 0}
        self.board = new_board()
        self.game_over = False
        self.busy = False
        self.ai_first = tk.BooleanVar(value=False)
        self.level = tk.StringVar(value="Medium")
        self.status = tk.StringVar(value="Your turn")
        self.info = tk.StringVar(value="")
        self.win_cells = []

        self.setup_ui()
        self.new_game()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Connect Four", font=("Arial", 18, "bold")).pack(pady=(0, 4))
        ttk.Label(frame, text="Minimax + Alpha-Beta Pruning", foreground="#5a5a5a").pack(pady=(0, 10))

        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X)

        ttk.Label(controls, text="Difficulty:").pack(side=tk.LEFT, padx=(0, 6))
        difficulty_box = ttk.Combobox(controls, textvariable=self.level, values=["Easy", "Medium", "Hard"], state="readonly", width=10)
        difficulty_box.pack(side=tk.LEFT)

        ttk.Checkbutton(controls, text="AI first", variable=self.ai_first).pack(side=tk.LEFT, padx=(12, 0))
        ttk.Button(controls, text="New Game", command=self.new_game).pack(side=tk.RIGHT)

        ttk.Label(frame, textvariable=self.status, font=("Arial", 12, "bold")).pack(pady=(14, 4))
        ttk.Label(frame, textvariable=self.info, foreground="#555555", font=("Arial", 9)).pack(pady=(0, 8))

        self.score_label = ttk.Label(frame, text="You: 0   Computer: 0   Draw: 0", foreground="#444444")
        self.score_label.pack(pady=(0, 8))

        self.canvas = tk.Canvas(frame, width=490, height=420, bg="#1f5ce6", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def draw_board(self, last_move=None):
        self.canvas.delete("all")
        cell_size = 60
        margin = 18
        radius = 24
        board_x0 = margin
        board_y0 = margin

        for r in range(ROWS):
            for c in range(COLS):
                x1 = board_x0 + c * cell_size
                y1 = board_y0 + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#1f5ce6", outline="#1f5ce6")
                self.canvas.create_oval(x1 + 8, y1 + 8, x2 - 8, y2 - 8, fill="#0a1d52", outline="")

        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                if piece == EMPTY:
                    continue
                x = board_x0 + c * cell_size + cell_size // 2
                y = board_y0 + r * cell_size + cell_size // 2
                color = "#ef3b4a" if piece == HUMAN else "#ffd90e"
                self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline="")

        if self.win_cells:
            for r, c in self.win_cells:
                x = board_x0 + c * cell_size + cell_size // 2
                y = board_y0 + r * cell_size + cell_size // 2
                self.canvas.create_oval(x - radius + 2, y - radius + 2, x + radius - 2, y + radius - 2, outline="#ffffff", width=4)

        if last_move is not None:
            r, c = last_move
            x = board_x0 + c * cell_size + cell_size // 2
            y = board_y0 + r * cell_size + cell_size // 2
            self.canvas.create_oval(x - radius - 10, y - radius - 10, x + radius + 10, y + radius + 10, outline="#ffffff", width=3)

    def update_score(self):
        self.score_label.config(text=f"You: {self.score['human']}   Computer: {self.score['ai']}   Draw: {self.score['draw']}")

    def make_move(self, col, piece, animate=True):
        row = drop_piece(self.board, col, piece)
        if animate:
            self.draw_board(last_move=(row, col))
        else:
            self.draw_board()
        return row

    def check_end(self, piece):
        cells = winning_cells(self.board, piece)
        if cells:
            self.win_cells = cells
            self.game_over = True
            self.busy = False
            self.draw_board()
            if piece == HUMAN:
                self.score["human"] += 1
                self.status.set("You win! 🎉")
            else:
                self.score["ai"] += 1
                self.status.set("Computer wins!")
            self.update_score()
            return True

        if board_full(self.board):
            self.game_over = True
            self.busy = False
            self.score["draw"] += 1
            self.status.set("Draw game!")
            self.update_score()
            return True

        return False

    def on_canvas_click(self, event):
        if self.game_over or self.busy:
            return

        x = event.x
        col = min(max(int(x // 60), 0), COLS - 1)
        if self.board[0][col] != EMPTY:
            return

        self.busy = True
        self.make_move(col, HUMAN)
        if self.check_end(HUMAN):
            return

        self.status.set("Computer thinking...")
        self.root.after(250, self.ai_turn)

    def ai_turn(self):
        if self.game_over:
            return
        col, stats = choose_ai_move(self.board, self.level.get())
        self.info.set(f"AI: depth={stats['depth']}  nodes={stats['nodes']}  time={stats['time']:.2f}s")
        self.make_move(col, AI)
        if self.check_end(AI):
            return
        self.busy = False
        self.status.set("Your turn")

    def new_game(self):
        self.board = new_board()
        self.game_over = False
        self.busy = False
        self.win_cells = []
        self.info.set("")
        self.update_score()
        self.draw_board()

        if self.ai_first.get():
            self.status.set("Computer thinking...")
            self.busy = True
            self.root.after(400, self.ai_turn)
        else:
            self.status.set("Your turn")


def main():
    root = tk.Tk()
    ConnectFourGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

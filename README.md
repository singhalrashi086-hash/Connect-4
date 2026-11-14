# Connect Four with AI (Minimax + Alpha-Beta Pruning)

**College AI Mini Project**

This is a Connect Four game where you play as Red against the computer as Yellow. The computer does not make random moves; it analyzes future possibilities using the Minimax algorithm with Alpha-Beta Pruning.

## How to Run

### Option A: Browser / Mobile (easiest)

Open the `index.html` file in any browser (Chrome, Safari, Firefox, etc.). No installation is required.

This is the JavaScript version of the same game and uses the same AI logic (Minimax + Alpha-Beta Pruning).

**Online play link (GitHub Pages):** after enabling GitHub Pages in the repository settings (`Settings → Pages → Branch: main → Save`), the game can be played directly at:
`https://<username>.github.io/<repo-name>/`

### Option B: Python (desktop)

```bash
python connect4.py
```

- Python 3.8+ is required.
- No additional `pip` packages are needed.
- Windows/macOS: Tkinter is included with Python.
- Linux (Ubuntu/Debian): if you see `No module named tkinter`, run:

```bash
sudo apt install python3-tk
```

## Features

- 3 difficulty levels: Easy, Medium, Hard
- Option to let the AI move first
- Disc drop animation and hover preview
- Winning line highlighting for the 4 connected discs
- Scoreboard (You / Computer / Draw)
- After each AI move, the game displays search depth, explored nodes, and elapsed time

## Project Files

| File | Purpose |
|------|---------|
| `index.html` | Browser/mobile version (HTML + CSS + JavaScript) |
| `connect4.py` | Python desktop version (Tkinter) |
| `ALGORITHM.md` | Full algorithm explanation, pseudocode, and complexity |
| `README.md` | Project overview and instructions |

Both versions consist of three parts:

1. Game Engine: board state, valid moves, win/draw detection
2. AI: heuristic evaluation + Minimax + Alpha-Beta Pruning
3. GUI: user interface and gameplay interaction

The engine and AI logic are separated from the GUI, which makes them testable without the interface.

## How the AI Works

### 1. Minimax

Think of the game as a tree: each node is a board position and each branch is a possible move.

- AI turn (MAX): choose the move with the highest score
- Human turn (MIN): assume the human also plays optimally and chooses the move that minimizes the AI's score
- After examining moves up to a specific depth, the board position is scored and those values are propagated upward through the tree

### 2. Alpha-Beta Pruning

Without pruning, the AI would need to examine every possible branch. Alpha-Beta pruning removes branches that cannot possibly improve the current decision, thereby reducing computation without changing the final result.

Optimization: moves are explored from the center outward because central columns are usually stronger, and this improves pruning efficiency.

### 3. Heuristic Evaluation Function

When the search reaches the depth limit and the game is not yet finished, the position is scored by evaluating each four-cell window (horizontal, vertical, and diagonal):

| Situation | Score |
|-----------|-------|
| AI has 4 in a row | +100 |
| AI has 3 and 1 empty cell | +5 |
| AI has 2 and 2 empty cells | +2 |
| Human has 3 and 1 empty cell | -4 (to force a block) |
| AI piece in the center column | +3 per piece |

A win or loss is scored much higher (`1,000,000`) so the AI prefers quick wins and avoids forced losses.

### 4. Difficulty Levels

| Level | Search depth | Extra |
|-------|--------------|-------|
| Easy | 2 | 30% chance of a random move |
| Medium | 4 | - |
| Hard | 6 | - |

## Testing Results

- If the AI has a winning move, it takes it.
- If the human has a single immediate winning threat, the AI blocks it.
- On a blank board at Hard difficulty, the AI explores around 1,400 nodes in about 0.05 seconds.
- Against a random player, the Medium AI won 20 out of 20 games.

## Possible Viva Questions

1. What is Minimax?
   Two-player zero-sum games use a search strategy where each side assumes the opponent will also play optimally.

2. Why use Alpha-Beta pruning?
   It cuts away useless branches so the AI can search deeper within the same time limit.

3. Why use a heuristic function?
   The full game tree is extremely large, so a complete search is not feasible. We estimate the board value at limited depth.

4. How is difficulty adjusted?
   By changing the search depth. Greater depth means more lookahead and a stronger AI.

5. What is the time complexity?
   Worst case: `O(b^d)`, where `b` is the branching factor (max 7) and `d` is the search depth.

6. How can the AI be improved?
   With a transposition table, iterative deepening, a better heuristic, or Monte Carlo Tree Search.

## Future Improvements

- Add a transposition table to avoid recalculating repeated board positions
- Use iterative deepening with a time limit
- Improve the heuristic with threat analysis and playable-cell evaluation
- Add a human-vs-human mode or online multiplayer
- Compare Minimax with Monte Carlo Tree Search

## Conclusion

This project demonstrates how adversarial search can be applied to a familiar board game. The game engine enforces the rules, while Minimax evaluates future moves and Alpha-Beta pruning reduces unnecessary searches.

This gives a strong AI that remains fast enough for both browser and desktop versions.

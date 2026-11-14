# Connect Four with AI — Project Report

| Field | Details |
| --- | --- |
| Project title | Connect Four with Artificial Intelligence |
| Course | Bachelor of Computer Applications (BCA) |
| Semester | 5 |
| Institution | Lachoo Memorial College of Science and Technology |
| Instructor | Ms. Sakshi |
| Submission date | 14 November 2026 |

## Project Team

| Student name | Roll number |
| --- | --- |
| Rashi Singhal | 243501179 |
| Ritika Prajapati | 243501225 |
| Sanyam Nagori | 243501189 |

## Abstract

This project implements the two-player strategy game Connect Four and an artificial-intelligence opponent. Players take turns dropping discs into a 6-by-7 board; the first to connect four discs horizontally, vertically, or diagonally wins. The computer player uses Minimax search with alpha-beta pruning and a heuristic evaluation function to select moves. The project provides both a browser implementation and a Python desktop implementation, along with adjustable AI difficulty and documentation of the algorithm.

## 1. Introduction

Connect Four is a turn-based, zero-sum game with perfect information: both players can see the entire board, and each player's success depends on anticipating the other's choices. This makes the game a useful example for studying adversarial search. The project combines a working game interface with a search-based AI that evaluates possible future positions rather than selecting every move at random.

## 2. Problem Statement

The objective is to create an interactive Connect Four game in which a human can play against a computer. The game must enforce legal moves, identify wins and draws, and allow the computer to choose strategic moves within practical computation limits.

## 3. Objectives

- Implement the rules of Connect Four on a 6-by-7 board.
- Detect horizontal, vertical, and diagonal four-in-a-row wins.
- Create browser and Python desktop versions of the game.
- Implement Minimax search with alpha-beta pruning.
- Evaluate non-terminal positions using a heuristic function.
- Provide multiple AI difficulty levels and automated tests for key logic.

## 4. Scope and Requirements

### Functional requirements

1. Start a new game with an empty board.
2. Allow the human to choose a non-full column.
3. Drop each disc into the lowest available position in its column.
4. Allow the AI to move either second or first, depending on the selected option.
5. Detect and display a win or draw, then prevent further moves until a new game starts.
6. Track game results and provide Easy, Medium, and Hard AI settings.

### Technical requirements

- Browser version: a modern web browser; no additional packages or build process.
- Desktop version: Python 3.8 or later with Tkinter available.
- No third-party Python packages are required.

## 5. System Design

The game is divided into three logical parts:

1. **Game engine:** stores the board, generates legal columns, applies and undoes moves, and checks for wins or a full board.
2. **AI engine:** orders moves from the center outward, searches future states with Minimax and alpha-beta pruning, and evaluates depth-limited positions.
3. **User interface:** gathers player input, displays the board and game status, and requests an AI move when appropriate.

The browser implementation is in `index.html`. The Python desktop implementation is in `connect4.py`. The detailed algorithm and pseudocode are provided in `ALGORITHM.md`.

## 6. AI Methodology

### 6.1 Minimax

The AI is treated as the maximizing player, while the human is treated as the minimizing player. The algorithm explores possible legal moves up to a selected depth. At AI turns it chooses the continuation with the highest score; at simulated human turns it assumes the opponent chooses the continuation with the lowest score. The chosen move is the one with the best score under this assumption.

### 6.2 Alpha-Beta Pruning

Alpha-beta pruning reduces the amount of search without changing the result that Minimax would produce for the same depth and move ordering. Alpha records the best value available to the maximizing player, and beta records the best value available to the minimizing player. When alpha is greater than or equal to beta, the rest of that branch can be skipped.

### 6.3 Move Ordering

The AI examines columns in center-first order: `3, 2, 4, 1, 5, 0, 6`. Central moves are often strategically useful; considering them early can help alpha-beta pruning eliminate more branches.

### 6.4 Heuristic Evaluation

When the search reaches its depth limit without a terminal result, it estimates the position by scoring four-cell windows in all four winning directions and rewarding AI pieces in the center column. The implementation uses these window weights:

| Pattern from the evaluated player's perspective | Score |
| --- | ---: |
| Four pieces | +100 |
| Three pieces and one empty cell | +5 |
| Two pieces and two empty cells | +2 |
| Three opponent pieces and one empty cell | -4 |
| Each piece in the center column | +3 |

Terminal wins and losses use a much larger score (`1,000,000`) than heuristic values. The remaining search depth is added to terminal scores so the AI prefers quicker wins and delays forced losses.

### 6.5 Difficulty Settings

| Difficulty | Search depth | Random-move chance |
| --- | ---: | ---: |
| Easy | 2 | 30% |
| Medium | 4 | 0% |
| Hard | 6 | 0% |

Increasing search depth gives the AI more foresight but can increase the number of positions it evaluates.

## 7. Complexity

Let `b` be the branching factor (at most seven legal columns) and `d` the search depth. Minimax has worst-case time complexity `O(b^d)`. Alpha-beta pruning can reduce the search considerably when strong moves are considered first; its idealized best case is approximately `O(b^(d/2))`. The recursive search uses `O(d)` stack space and reuses the board by applying and undoing moves.

## 8. Testing Plan

The automated Python tests in `tests/test_connect4.py` cover:

- initial board dimensions and contents
- gravity and piece placement
- rejection of moves in a full column
- horizontal, vertical, and diagonal win detection
- full-board detection
- selecting an immediate AI win
- blocking an immediate human win
- selecting a legal AI move

Run the test suite from the repository root with:

```bash
python -m unittest discover -s tests -v
```

The browser version should also be checked manually by opening `index.html` and trying legal and full-column moves, both player turn orders, each difficulty, win and draw situations, and starting a new game. Record actual test output and any required screenshots here if requested; do not report tests as passed unless they have been run.

## 9. Limitations

- The search is limited to a fixed depth, so the AI does not analyze the entire game tree.
- The heuristic is intentionally simple and may not recognize every long-term strategic threat.
- Easy mode can deliberately choose a random move, so it is not intended to play optimally.
- The desktop interface requires Tkinter; some Linux installations require the operating-system Tk package.
- The browser and Python versions are separate implementations, so changes to game behavior should be checked in both.

## 10. Possible Future Work

- Add a transposition table to cache previously evaluated board positions.
- Use iterative deepening and a time limit to control response time.
- Improve the heuristic with threat and playable-cell analysis.
- Add human-versus-human mode or online multiplayer.
- Compare Minimax against Monte Carlo Tree Search.

## 11. Conclusion

The project demonstrates how adversarial search can be applied to a familiar board game. Its game engine enforces the rules, while Minimax evaluates future moves and alpha-beta pruning avoids searching branches that cannot affect the decision. A heuristic makes depth-limited search practical, and the two interfaces make the same project accessible in a browser or as a Python desktop application.

## References

- Russell, S. J., & Norvig, P. *Artificial Intelligence: A Modern Approach*. Pearson. (Background on adversarial search and game-playing.)
- Connect Four project source files: `index.html` and `connect4.py`.
- Project algorithm documentation: `ALGORITHM.md`.

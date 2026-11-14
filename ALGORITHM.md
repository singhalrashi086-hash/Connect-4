# Connect Four AI Algorithm

This document describes the algorithm implemented in `index.html`.

## Game representation

The board is a 6-row by 7-column array. Each cell contains `0` for empty, `1` for the human player, or `2` for the AI. A move selects a column; the piece occupies the lowest empty row in that column. The AI considers legal columns from the center outward (`3, 2, 4, 1, 5, 0, 6`), which tends to find strong moves earlier and makes alpha-beta pruning more effective.

## Search: Minimax with alpha-beta pruning

The game is zero-sum. At AI turns, the search maximizes the score; at human turns, it minimizes the score, assuming both players choose their best move. The search stops at a win, draw, or configured depth limit. At the depth limit, the board is scored by the heuristic below.

```text
minimax(board, depth, alpha, beta, maximizing):
    if AI has won:    return WIN_SCORE + depth
    if human has won: return -WIN_SCORE - depth
    if no legal moves: return 0
    if depth == 0: return evaluate(board)

    if maximizing:
        best = -infinity
        for column in legal columns, center first:
            play AI move
            best = max(best, minimax(board, depth - 1, alpha, beta, false))
            undo move
            alpha = max(alpha, best)
            if alpha >= beta: stop searching this node
        return best
    else:
        best = +infinity
        for column in legal columns, center first:
            play human move
            best = min(best, minimax(board, depth - 1, alpha, beta, true))
            undo move
            beta = min(beta, best)
            if alpha >= beta: stop searching this node
        return best
```

Alpha-beta pruning does not change the result of Minimax. It skips branches that cannot improve the current choice. In the worst case the search is `O(b^d)` for branching factor `b` and depth `d`; good move ordering can reduce the effective work substantially (often described as approximately `O(b^(d/2))` in the ideal case).

## Heuristic evaluation

At a non-terminal leaf, the AI scores every contiguous four-cell window horizontally, vertically, and diagonally, plus the center column:

| Pattern from AI's perspective | Score |
| --- | ---: |
| Four AI pieces | +100 |
| Three AI pieces and one empty | +5 |
| Two AI pieces and two empty | +2 |
| Three human pieces and one empty | -4 |
| Each AI piece in the center column | +3 |

Scores from all windows are added. Terminal wins and losses use a much larger magnitude (`1,000,000`) so they outweigh heuristic preferences. Adding depth to terminal values prefers faster AI wins and delays forced losses.

## Difficulty settings

| Level | Search depth | Random-move chance |
| --- | ---: | ---: |
| Easy | 2 | 30% |
| Medium | 4 | 0% |
| Hard | 6 | 0% |

The browser UI reports the selected search depth, number of visited nodes, and elapsed time after each AI move.

## Complete-turn outline

1. Reject clicks while the game is busy, over, or the selected column is full.
2. Drop the human piece and check for a win or draw.
3. Run the AI search at the selected difficulty, play its chosen column, and check for a win or draw.
4. Return control to the human unless the game has ended.

The implementation is self-contained in `index.html`; there are no external packages or build steps. Open that file in a modern browser to play.
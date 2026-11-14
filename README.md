# Connect Four with AI (Minimax + Alpha-Beta Pruning)

**College AI Mini Project**

Ek Connect Four game jisme aap (Red) computer (Yellow) ke against khelte ho. Computer random move nahi chalta, wo **Minimax algorithm with Alpha-Beta Pruning** use karke aage ki chaalein "soch" kar best move chunta hai.

## Run kaise karein

### Option A: Browser / Phone (sabse aasan)

`index.html` file ko kisi bhi browser (Chrome, Safari, Firefox) mein kholo. Kuch install nahi karna.
Ye same game aur same AI (Minimax + Alpha-Beta) ka JavaScript version hai.

**Online play link (GitHub Pages):** repo ki *Settings → Pages → Branch: main → Save* karne par
`https://<username>.github.io/<repo-name>/` par game seedha khelne ke liye mil jata hai.

### Option B: Python (desktop)

```
python connect4.py
```

- Python 3.8+ chahiye. Koi pip install nahi karna.
- Windows / macOS: tkinter Python ke saath hi aata hai.
- Linux (Ubuntu/Debian): agar `No module named tkinter` aaye to `sudo apt install python3-tk`.

## Features

- 3 difficulty levels: Easy, Medium, Hard
- "AI pehle khele" option
- Piece girne ki animation, hover preview, jeetne wali 4 coins highlight
- Scoreboard (You / Computer / Draw)
- Har AI move ke baad dikhta hai: search depth, kitne nodes explore hue, kitna time laga

## Files

| File | Kya hai |
|------|---------|
| `index.html` | Browser/phone version (HTML + CSS + JavaScript) |
| `connect4.py` | Python desktop version (tkinter) |
| `ALGORITHM.md` | Poora algorithm, pseudocode, complexity |
| `README.md` | Ye file |

Dono versions mein 3 parts hain: **1. Game Engine** (board, valid moves, win/draw check), **2. AI** (heuristic + Minimax + Alpha-Beta), **3. GUI**.
Engine aur AI GUI se alag hain, isliye unhe bina GUI ke bhi test kiya ja sakta hai.

## AI kaise kaam karta hai

### 1. Minimax
Game ko ek tree ki tarah socho: har node ek board position hai, har branch ek possible move.
- **AI ki baari (MAX):** wo move chuno jisme score sabse zyada ho.
- **Human ki baari (MIN):** maan lo human sabse accha move chalega, yaani score sabse kam wala.
- Depth tak aage dekhne ke baad board ko score diya jata hai aur wo score upar propagate hota hai.

### 2. Alpha-Beta Pruning
Minimax ke bina har branch dekhna padta hai. Alpha-Beta mein agar pata chal jaye ki koi branch pehle se mili hui better option se achhi ho hi nahi sakti, to use **cut (prune)** kar dete hain. Result wahi milta hai, lekin kam nodes explore hote hain.

Optimisation: moves ko **center se bahar ki taraf** order kiya hai, kyunki center column usually strong hota hai aur isse pruning zyada hoti hai.

### 3. Heuristic Evaluation Function
Jab depth khatam ho jaye aur game finish na hua ho, to board ko score dete hain. Har 4-cell window (horizontal, vertical, diagonal) ke liye:

| Situation | Score |
|-----------|-------|
| AI ke 4 | +100 |
| AI ke 3 + 1 khali | +5 |
| AI ke 2 + 2 khali | +2 |
| Human ke 3 + 1 khali | -4 (taaki AI block kare) |
| Center column mein AI ka piece | +3 har piece |

Win/loss ka score bahut bada (1,000,000) rakha hai, aur jaldi jeetne ko better maana jata hai.

### 4. Difficulty
| Level | Search depth | Extra |
|-------|--------------|-------|
| Easy | 2 | 30% chance random move (galti) |
| Medium | 4 | - |
| Hard | 6 | - |

## Testing results

- AI ke paas jeetne ka move ho to wo le leta hai.
- Human ke jeetne ka single threat ho to AI block karta hai.
- Hard level par khali board par ~1,400 nodes aur ~0.05 sec.
- Medium AI ne random player ke against 20 mein se 20 games jeete.

## Viva ke liye possible questions

1. **Minimax kya hai?** Two-player zero-sum games ke liye algorithm jo maan kar chalta hai ki opponent bhi best khelega.
2. **Alpha-Beta pruning kyun?** Same answer deta hai, lekin useless branches kaat kar time bachata hai.
3. **Heuristic function kyun chahiye?** Poora game tree bahut bada hai (Connect Four mein lagbhag 4.5 trillion positions), isliye limited depth par board ko estimate karna padta hai.
4. **Difficulty kaise badli?** Search depth badha kar. Zyada depth = zyada aage dekhta hai = zyada strong.
5. **Time complexity?** Worst case O(b^d), best case alpha-beta ke saath lagbhag O(b^(d/2)), jahan b = branching factor (max 7) aur d = depth.
6. **Improvements?** Transposition table, iterative deepening, better heuristic, ya Monte Carlo Tree Search.

## Future improvements

- Transposition table (same position dobara calculate na ho)
- Iterative deepening with time limit
- Monte Carlo Tree Search (MCTS) ke saath comparison

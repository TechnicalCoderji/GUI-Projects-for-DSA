# 🧩 Sudoku Mastermind: Play, Solve, and Create Puzzles 🚀

[![GitHub License](https://img.shields.io/github/license/TechnicalCoderji/GUI-Projects-for-DSA?color=blue)](https://github.com/YourUsername/Sudoku)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-yellowgreen)](https://www.python.org/)

**A polished Sudoku experience** with an intuitive GUI for playing, solving, and designing puzzles. Save your progress, tackle AI-generated challenges, or craft your own Sudoku masterpiece!

![Sudoku GUI Demo]
![MAIN GUI]
(https://github.com/TechnicalCoderji/SUDOKU/blob/main/img/s1.png)
![Open File]
(https://github.com/TechnicalCoderji/SUDOKU/blob/main/img/s4.png)
![Save File]
(https://github.com/TechnicalCoderji/SUDOKU/blob/main/img/s5.png)
![SUDOKU Generator]
(https://github.com/TechnicalCoderji/SUDOKU/blob/main/img/s2.png)
![SUDOKU Solver]
(https://github.com/TechnicalCoderji/SUDOKU/blob/main/img/s3.png)

---

## 📦 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [File Structure](#-file-structure)
- [Algorithms](#-algorithms)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## ✨ Features

### 🎮 **Interactive GUI** (`main.py`)
- **Play Sudoku** with tools like:
  - ✏️ **Pens**: White, Yellow, Orange
  - 🧹 **Erase**, **Undo**, **Reset**
  - 💾 **Save/Load** puzzles (`.sudoku` format)
- **Design Mode**: Build custom Sudoku boards from scratch.

### ⚙️ **Under the Hood**
- **5 Solving Algorithms** (`solver.py`):
  1. Brute Force
  2. Backtracking
  3. Advanced Backtracking
  4. Constraint Propagation
  5. **DLX (Dancing Links)** 🚀
- **Smart Generator** (`generator.py`): 
  - Creates puzzles in 5 difficulties: **Easy -> Medium -> Hard -> Expert -> Legendary**.
  - Uses **Hybrid Backtracking with Constraint Propagation (HBCPCP)**.
- **Save System** (`save_loader.py`): Securely stores puzzles in `.sudoku` files.

---

## 📥 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/TechnicalCoderji/GUI-Project-for-DSA/SUDOKU.git
   cd Sudoku
   ```

2. **Install Pygame** (for GUI):
   ```bash
   pip install pygame
   ```

3. **Launch the GUI**:
   ```bash
   python main.py
   ```

---

## 📂 File Structure

```
SUDOKU/
├── game_board/           # Pre-saved .sudoku puzzles
├── img/                  # GUI assets (buttons, icons, fonts)
│
├── algorithm.py          # Core logic for solving/generating
├── generator.py          # Implements HBCPCP difficulty stages
├── solver.py             # All 5 solving algorithms
├── save_loader.py        # Handles .sudoku file I/O
├── main.py               # Pygame GUI (play/design mode)
└── tools.py              # GUI utilities (buttons, grids, colors)
```

---

## 🧠 Algorithms

### 🔍 **Solving** (`algorithm.py`)
- **Brute Force**: Tests all possibilities (for small grids).
- **Backtracking**: Recursive depth-first search.
- **Advanced Backtracking**: Optimized cell selection.
- **Constraint Propagation**: Eliminates possibilities iteratively.
- **DLX (Dancing Links)**: Solves "exact cover" Sudokus rapidly.

### 🎲 **Generation** (`generator.py`)
- **Hybrid Backtracking with Constraint Propagation (HBCPCP)**:
  1. **Fill Grid**: Backtracking with smart pruning.
  2. **Controlled Removal**: Delete numbers while ensuring solvability.
  3. **Difficulty Tuning**: Adjust ambiguity (Easy = 40+ clues, Legendary = <25 clues).

---

## 📜 License

**MIT License**  
Free to use, modify, and distribute. Attribution appreciated but not required.

---

## 🙏 Acknowledgements
- GUI icons by [Flaticon](https://www.flaticon.com).
- Pygame community for graphics tools.

---

🌟 **Enjoy Sudoku? Leave a star!**  
🐞 **Issues?** Report them [here](https://github.com/TechnicalCoderji/GUI-Projects-for-DSA/SUDOKU/issues).

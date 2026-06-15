*This project has been created as part of the 42 curriculum by lmezzaba, lrossi.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generation project developed in Python.

The goal of the project is to generate valid mazes from a configuration file, export them using a hexadecimal wall representation, display them visually, and provide a reusable maze generation package.

The project supports:

* Perfect mazes.
* Imperfect mazes.
* Reproducible generation using a seed.
* ASCII rendering.
* Shortest path computation.
* Export to hexadecimal format.
* Reusable maze generation library.

---

# Instructions

## Requirements

* Python 3.10 or newer

## Run the project

```bash
python3 a_maze_ing.py config.txt
```

## Build the reusable package

```bash
python3 -m pip install build
python3 -m build
```

Generated files:

```text
dist/
├── mazegen-lmezzaba-lrossi-1.0.0.tar.gz
└── mazegen-lmezzaba-lrossi-1.0.0-py3-none-any.whl
```

## Install the package

```bash
pip install dist/*.whl
```

---

# Configuration File Format

The configuration file contains one key-value pair per line.

Example:

```text
WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT=14,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Mandatory Keys

| Key         | Description       |
| ----------- | ----------------- |
| WIDTH       | Maze width        |
| HEIGHT      | Maze height       |
| ENTRY       | Entry coordinates |
| EXIT        | Exit coordinates  |
| OUTPUT_FILE | Output filename   |
| PERFECT     | Perfect maze flag |

## Optional Keys

| Key  | Description |
| ---- | ----------- |
| SEED | Random seed |

---

# Maze Generation Algorithm

The maze is generated using a Recursive Backtracker (Depth First Search).

Algorithm steps:

1. Start from the entry cell.
2. Mark the current cell as visited.
3. Randomly choose an unvisited neighbour.
4. Remove the wall between the two cells.
5. Continue recursively.
6. Backtrack when no unvisited neighbour remains.
7. Stop when every reachable cell has been visited.

---

# Why This Algorithm

Recursive Backtracker was chosen because:

* It is simple to implement.
* It guarantees a connected maze.
* It naturally produces perfect mazes.
* It is memory efficient.
* It generates visually pleasing mazes.

For imperfect mazes, additional walls may be removed after generation to create loops.

---

# Output Format

Each cell is represented by a hexadecimal digit.

Wall encoding:

| Bit | Direction |
| --- | --------- |
| 0   | North     |
| 1   | East      |
| 2   | South     |
| 3   | West      |

Example:

```text
A
```

Binary:

```text
1010
```

Meaning:

* East wall closed
* West wall closed

After the maze data:

```text
<maze>

entry_x,entry_y
exit_x,exit_y
NESW...
```

The final line contains the shortest path.

---

# Visual Representation

The maze can be displayed using terminal ASCII rendering.

Displayed elements:

* Walls
* Entry
* Exit
* Solution path
* 42 pattern

Available interactions:

* Generate a new maze
* Show solution
* Hide solution
* Change wall colour

---

# Reusable Module

The reusable component of the project is the `MazeGenerator` class.

Example:

```python
from mezagen import MazeGenerator

maze = MazeGenerator("config.txt")

maze.display()
maze.save_maze()
solution = maze.solve()
```

The reusable module provides access to:

* Maze structure
* Entry position
* Exit position
* Generated maze
* Solution path

---

# Team Organisation

## Lorenzo Mezzabarba

Responsibilities:

* Maze generation
* Maze solving
* File export
* Package creation

## Ludovico Rossi

Responsibilities:

* Parsing
* Testing
* Documentation
* Validation

---

# Project Planning

## Initial Plan

1. Configuration parser
2. Maze data structure
3. Maze generation
4. Maze export
5. Visual display
6. Packaging

## Evolution

During development:

* Additional validation was added.
* Solution path generation was added.
* Reusable package support was improved.
* Visualization features were expanded.

---

# What Worked Well

* DFS generation algorithm.
* Reusable architecture.
* Export format generation.
* Type checking with mypy.

# Possible Improvements

* Additional generation algorithms.
* MLX graphical interface.
* Maze generation animations.
* Performance optimizations for large mazes.

---

# Tools Used

* Python 3.10+
* setuptools
* build
* mypy
* flake8
* Git
* GitHub

---

# Resources

## Maze Generation

* Recursive Backtracker
* Depth First Search
* Graph Theory
* Spanning Trees

## Documentation

* Python Documentation
* PEP 8
* PEP 257
* setuptools Documentation

## AI Usage

AI tools were used for:

* Type hint verification
* Documentation drafting
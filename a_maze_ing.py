import sys

from mazegen import MazeGenerator


def main() -> int:
    """
    Run the maze generator from a configuration file.

    Returns:
        Process exit status.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return 1

    try:
        maze = MazeGenerator(sys.argv[1])
        maze.ask_input()
        return 0
    except Exception as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
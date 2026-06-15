import os
import random
from typing import TypeAlias, cast

from parsing import file_parser


Wall: TypeAlias = list[bool]
Coordinate: TypeAlias = tuple[int, int]
Direction: TypeAlias = tuple[int, int, str]
MazeGrid: TypeAlias = list[list["MazeGenerator.Cell"]]
PathNode: TypeAlias = tuple[Coordinate, str, list[Coordinate]]


class MazeGenerator:
    """Generate, solve, save and render a maze."""

    class Cell:
        """Represent one maze cell."""

        def __init__(
            self,
            up: tuple[bool, bool] = (False, True),
            down: tuple[bool, bool] = (False, True),
            left: tuple[bool, bool] = (False, True),
            right: tuple[bool, bool] = (False, True),
        ) -> None:
            self.up: Wall = list(up)
            self.down: Wall = list(down)
            self.left: Wall = list(left)
            self.right: Wall = list(right)
            self.is_visited = False
            self.is_solution = False

        def get_params_as_list(self) -> list[bool]:
            """Return closed walls in North, East, South, West order."""
            return [
                not self.up[0],
                not self.right[0],
                not self.down[0],
                not self.left[0],
            ]

    class Colors:
        """ANSI terminal colors."""

        RESET = "\033[0m"
        BG_BLACK = "\033[40m"
        BG_RED = "\033[41m"
        BG_GREEN = "\033[42m"
        BG_YELLOW = "\033[43m"
        BG_BLUE = "\033[44m"
        BG_MAGENTA = "\033[45m"
        BG_CYAN = "\033[46m"
        BG_WHITE = "\033[47m"
        BG_ORANGE = "\033[48;5;214m"
        BG_PURPLE = "\033[48;5;93m"
        BG_BROWN = "\033[48;5;130m"

    def __init__(self, config_path: str) -> None:
        config, success = file_parser(config_path)

        if not success:
            raise ValueError("Config file parsing failed")

        typed_config = cast(dict[str, object], config)

        self.maze_width = self._as_int(typed_config["WIDTH"])
        self.maze_height = self._as_int(typed_config["HEIGHT"])
        self.entry = self._as_coordinate(typed_config["ENTRY"])
        self.exit = self._as_coordinate(typed_config["EXIT"])
        self.seed = self._as_int(typed_config["SEED"])
        self.output_file = self._as_str(typed_config["OUTPUT_FILE"])
        self.is_perfect = self._as_bool(typed_config["PERFECT"])

        self.walls = self.Colors.BG_WHITE
        self.spaces = self.Colors.BG_BLACK
        self.picture = self.Colors.BG_CYAN
        self.color_entry = self.Colors.BG_YELLOW
        self.color_exit = self.Colors.BG_GREEN
        self.solution_color = self.Colors.BG_RED
        self.neutral = self.Colors.RESET
        self.show_solution = False

        self.maze = self.generate_maze()
        self._insert_ft_pattern_in_maze()
        self.sculpt_maze()

        if not self.is_perfect:
            self.make_imperfect()

        self.solution = self.solve_maze()
        self.save_maze()

    def _as_int(self, value: object) -> int:
        if not isinstance(value, int):
            raise TypeError("Expected int in config")
        return value

    def _as_bool(self, value: object) -> bool:
        if not isinstance(value, bool):
            raise TypeError("Expected bool in config")
        return value

    def _as_str(self, value: object) -> str:
        if not isinstance(value, str):
            raise TypeError("Expected str in config")
        return value

    def _as_coordinate(self, value: object) -> Coordinate:
        if not isinstance(value, (list, tuple)):
            raise TypeError("Expected coordinate in config")
        if len(value) != 2:
            raise ValueError("Coordinate must contain two values")
        x = value[0]
        y = value[1]
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Coordinate values must be integers")
        return x, y

    def generate_maze(self) -> MazeGrid:
        """Create the initial closed maze grid."""
        return [
            [
                self.Cell(
                    left=(False, False) if x == 0 else (False, True),
                    right=(
                        (False, False)
                        if x == self.maze_width - 1
                        else (False, True)
                    ),
                    up=(False, False) if y == 0 else (False, True),
                    down=(
                        (False, False)
                        if y == self.maze_height - 1
                        else (False, True)
                    ),
                )
                for x in range(self.maze_width)
            ]
            for y in range(self.maze_height)
        ]

    def render_maze(self) -> None:
        """Render the maze in the terminal."""
        os.system("clear")

        for y in range(self.maze_height):
            self._render_top_line(y)
            self._render_middle_line(y)

        self._render_bottom_line()

        if self.show_solution:
            print(f"Shortest path: {self.solution}")

    def _render_top_line(self, y: int) -> None:
        line = ""

        for x in range(self.maze_width):
            cell = self.maze[y][x]
            line += f"{self.walls} {self.neutral}"

            if cell.up[0]:
                line += f"{self.spaces}   {self.neutral}"
            else:
                line += f"{self.walls}   {self.neutral}"

        line += f"{self.walls} {self.neutral}"
        print(line)

    def _render_middle_line(self, y: int) -> None:
        line = ""

        for x in range(self.maze_width):
            cell = self.maze[y][x]

            if cell.left[0]:
                line += f"{self.spaces} {self.neutral}"
            else:
                line += f"{self.walls} {self.neutral}"

            if (x, y) == self.entry:
                line += f"{self.color_entry} S {self.neutral}"
            elif (x, y) == self.exit:
                line += f"{self.color_exit} E {self.neutral}"
            elif self._is_blocked_cell(cell):
                line += f"{self.picture}   {self.neutral}"
            elif self.show_solution and cell.is_solution:
                line += f"{self.solution_color} * {self.neutral}"
            else:
                line += f"{self.spaces}   {self.neutral}"

        last = self.maze[y][self.maze_width - 1]

        if last.right[0]:
            line += f"{self.spaces} {self.neutral}"
        else:
            line += f"{self.walls} {self.neutral}"

        print(line)

    def _render_bottom_line(self) -> None:
        line = ""

        for x in range(self.maze_width):
            cell = self.maze[self.maze_height - 1][x]
            line += f"{self.walls} {self.neutral}"

            if cell.down[0]:
                line += f"{self.spaces}   {self.neutral}"
            else:
                line += f"{self.walls}   {self.neutral}"

        line += f"{self.walls} {self.neutral}"
        print(line)

    def _is_blocked_cell(self, cell: Cell) -> bool:
        return (
            cell.up[1] is False
            and cell.down[1] is False
            and cell.left[1] is False
            and cell.right[1] is False
        )

    def _cell_is_open(self, x: int, y: int) -> bool:
        if x < 0 or y < 0:
            return False
        if x >= self.maze_width or y >= self.maze_height:
            return False
        return not self._is_blocked_cell(self.maze[y][x])

    def _would_create_3x3_open_area(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ) -> bool:
        for start_y in range(
            max(0, min(y1, y2) - 2),
            min(self.maze_height - 2, max(y1, y2)) + 1,
        ):
            for start_x in range(
                max(0, min(x1, x2) - 2),
                min(self.maze_width - 2, max(x1, x2)) + 1,
            ):
                if self._is_3x3_open(start_x, start_y):
                    return True
        return False

    def _is_3x3_open(self, start_x: int, start_y: int) -> bool:
        for dy in range(3):
            for dx in range(3):
                if not self._cell_is_open(start_x + dx, start_y + dy):
                    return False
        return True

    def _insert_ft_pattern_in_maze(self) -> None:
        ft_pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]

        pivot = self._find_valid_pattern_pivot(ft_pattern)

        if pivot is None:
            print("Maze too small or entry/exit blocks the 42 pattern")
            return

        pivot_x, pivot_y = pivot

        for pattern_y, row in enumerate(ft_pattern):
            for pattern_x, value in enumerate(row):
                if value == 1:
                    maze_x = pivot_x + pattern_x
                    maze_y = pivot_y + pattern_y
                    cell = self.maze[maze_y][maze_x]
                    cell.up = [False, False]
                    cell.down = [False, False]
                    cell.left = [False, False]
                    cell.right = [False, False]

    def _find_valid_pattern_pivot(
        self,
        pattern: list[list[int]],
    ) -> Coordinate | None:
        pattern_h = len(pattern)
        pattern_w = len(pattern[0])

        for pivot_y in range(1, self.maze_height - pattern_h):
            for pivot_x in range(1, self.maze_width - pattern_w):
                pivot = (pivot_x, pivot_y)

                if self._pattern_position_is_valid(pattern, pivot):
                    return pivot

        return None

    def _pattern_position_is_valid(
        self,
        pattern: list[list[int]],
        pivot: Coordinate,
    ) -> bool:
        pivot_x, pivot_y = pivot

        for pattern_y, row in enumerate(pattern):
            for pattern_x, value in enumerate(row):
                if value != 1:
                    continue

                maze_x = pivot_x + pattern_x
                maze_y = pivot_y + pattern_y

                if (maze_x, maze_y) == self.entry:
                    return False
                if (maze_x, maze_y) == self.exit:
                    return False

        return True

    def sculpt_maze(self) -> None:
        """Generate a perfect maze using depth-first search."""
        random.seed(self.seed)

        x, y = self.entry
        self.maze[y][x].is_visited = True
        stack: list[Coordinate] = [(x, y)]

        while stack:
            x, y = stack[-1]
            current = self.maze[y][x]
            neighbors = self._get_neighbors(x, y)
            random.shuffle(neighbors)

            moved = self._try_move(current, neighbors, stack)

            if not moved:
                stack.pop()

    def _get_neighbors(self, x: int, y: int) -> list[Direction]:
        neighbors: list[Direction] = []

        if y > 0:
            neighbors.append((x, y - 1, "up"))
        if y < self.maze_height - 1:
            neighbors.append((x, y + 1, "down"))
        if x > 0:
            neighbors.append((x - 1, y, "left"))
        if x < self.maze_width - 1:
            neighbors.append((x + 1, y, "right"))

        return neighbors

    def _try_move(
        self,
        current: Cell,
        neighbors: list[Direction],
        stack: list[Coordinate],
    ) -> bool:
        for nx, ny, direction in neighbors:
            neighbor = self.maze[ny][nx]

            if neighbor.is_visited:
                continue

            if not self._open_between(current, neighbor, direction):
                continue

            neighbor.is_visited = True
            stack.append((nx, ny))
            return True

        return False

    def _open_between(
        self,
        current: Cell,
        neighbor: Cell,
        direction: str,
    ) -> bool:
        if direction == "up":
            if not current.up[1] or not neighbor.down[1]:
                return False
            current.up[0] = True
            neighbor.down[0] = True
            return True

        if direction == "down":
            if not current.down[1] or not neighbor.up[1]:
                return False
            current.down[0] = True
            neighbor.up[0] = True
            return True

        if direction == "left":
            if not current.left[1] or not neighbor.right[1]:
                return False
            current.left[0] = True
            neighbor.right[0] = True
            return True

        if not current.right[1] or not neighbor.left[1]:
            return False

        current.right[0] = True
        neighbor.left[0] = True
        return True

    def make_imperfect(self) -> None:
        """Open extra walls to create cycles."""
        random.seed(self.seed + 42)

        openings = max(1, (self.maze_width * self.maze_height) // 10)
        opened = 0
        attempts = 0
        max_attempts = openings * 50

        while opened < openings and attempts < max_attempts:
            attempts += 1

            if self._try_open_random_wall():
                opened += 1

    def _try_open_random_wall(self) -> bool:
        x = random.randrange(self.maze_width)
        y = random.randrange(self.maze_height)
        cell = self.maze[y][x]

        if self._is_blocked_cell(cell):
            return False

        directions = self._get_neighbors(x, y)
        random.shuffle(directions)

        for nx, ny, direction in directions:
            neighbor = self.maze[ny][nx]

            if self._is_blocked_cell(neighbor):
                continue
            if self._would_create_3x3_open_area(x, y, nx, ny):
                continue
            if self._open_wall_if_closed(cell, neighbor, direction):
                return True

        return False

    def _open_wall_if_closed(
        self,
        cell: Cell,
        neighbor: Cell,
        direction: str,
    ) -> bool:
        if direction == "up" and not cell.up[0]:
            return self._open_between(cell, neighbor, "up")
        if direction == "down" and not cell.down[0]:
            return self._open_between(cell, neighbor, "down")
        if direction == "left" and not cell.left[0]:
            return self._open_between(cell, neighbor, "left")
        if direction == "right" and not cell.right[0]:
            return self._open_between(cell, neighbor, "right")
        return False

    def solve_maze(self) -> str:
        """Find the shortest path from entry to exit using BFS."""
        start = self.entry
        end = self.exit

        for row in self.maze:
            for cell in row:
                cell.is_solution = False

        queue: list[PathNode] = [(start, "", [start])]
        visited: set[Coordinate] = {start}

        while queue:
            (x, y), path, coords = queue.pop(0)

            if (x, y) == end:
                for px, py in coords:
                    self.maze[py][px].is_solution = True
                return path

            self._add_solution_neighbors(x, y, path, coords, queue, visited)

        return ""

    def _add_solution_neighbors(
        self,
        x: int,
        y: int,
        path: str,
        coords: list[Coordinate],
        queue: list[PathNode],
        visited: set[Coordinate],
    ) -> None:
        cell = self.maze[y][x]

        moves = [
            (cell.up[0], x, y - 1, "N"),
            (cell.right[0], x + 1, y, "E"),
            (cell.down[0], x, y + 1, "S"),
            (cell.left[0], x - 1, y, "W"),
        ]

        for is_open, nx, ny, letter in moves:
            coord = (nx, ny)

            if not is_open:
                continue
            if not self._inside_maze(nx, ny):
                continue
            if coord in visited:
                continue

            visited.add(coord)
            queue.append((coord, path + letter, coords + [coord]))

    def _inside_maze(self, x: int, y: int) -> bool:
        return 0 <= x < self.maze_width and 0 <= y < self.maze_height

    def save_maze(self) -> None:
        """Save the maze in the required hexadecimal format."""
        with open(self.output_file, "w", encoding="utf-8") as file:
            for y in range(self.maze_height):
                for x in range(self.maze_width):
                    bits = self.maze[y][x].get_params_as_list()
                    number = "".join(str(int(bit)) for bit in bits)
                    file.write(hex(int(number, 2))[2:].capitalize())
                file.write("\n")

            file.write("\n")
            file.write(f"{self.entry[0]},{self.entry[1]}\n")
            file.write(f"{self.exit[0]},{self.exit[1]}\n")
            file.write(f"{self.solution}\n")

    def change_colors(self) -> None:
        """Rotate terminal colors."""
        if self.walls == self.Colors.BG_WHITE:
            self.walls = self.Colors.BG_YELLOW
            self.spaces = self.Colors.BG_RED
            self.picture = self.Colors.BG_PURPLE
            self.color_entry = self.Colors.BG_GREEN
            self.color_exit = self.Colors.BG_ORANGE
            return

        if self.walls == self.Colors.BG_YELLOW:
            self.walls = self.Colors.BG_CYAN
            self.spaces = self.Colors.BG_BLACK
            self.picture = self.Colors.BG_BLUE
            self.color_entry = self.Colors.BG_GREEN
            self.color_exit = self.Colors.BG_MAGENTA
            return

        if self.walls == self.Colors.BG_CYAN:
            self.walls = self.Colors.BG_GREEN
            self.spaces = self.Colors.BG_BLACK
            self.picture = self.Colors.BG_BROWN
            self.color_entry = self.Colors.BG_YELLOW
            self.color_exit = self.Colors.BG_RED
            return

        self.walls = self.Colors.BG_WHITE
        self.spaces = self.Colors.BG_BLACK
        self.picture = self.Colors.BG_BLUE
        self.color_entry = self.Colors.BG_CYAN
        self.color_exit = self.Colors.BG_RED

    def regenerate(self) -> None:
        """Generate a new maze with a new seed."""
        self.seed = random.randint(1, 100000)
        self.maze = self.generate_maze()
        self._insert_ft_pattern_in_maze()
        self.sculpt_maze()

        if not self.is_perfect:
            self.make_imperfect()

        self.solution = self.solve_maze()
        self.save_maze()

    def ask_input(self) -> None:
        """Handle user interaction."""
        while True:
            self.render_maze()

            value = input(
                "=== A-Maze-Ing ===\n"
                "1. Regenerate a new maze\n"
                "2. Show/Hide path from entry to exit\n"
                "3. Rotate maze colors\n"
                "4. Quit\n"
                "Choice? (1-4)\n"
            )

            if value == "1":
                self.regenerate()
            elif value == "2":
                self.show_solution = not self.show_solution
            elif value == "3":
                self.change_colors()
            elif value == "4":
                print("Quitting it is")
                break
            else:
                print("Wrong input")


if __name__ == "__main__":
    try:
        maze = MazeGenerator("config_test.txt")
        maze.ask_input()
    except Exception as error:
        print(type(error).__name__, error)
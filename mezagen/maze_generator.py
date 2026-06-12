import random
from parsing import file_parser


class MazeGenerator:
    class Cell:
        def __init__(
            self,
            up=(False, True),
            down=(False, True),
            left=(False, True),
            right=(False, True),
        ):
            self.up = list(up)
            self.down = list(down)
            self.left = list(left)
            self.right = list(right)
            self.isVisited = False

        def getParamsAsList(self):
            return [
                not self.up[0],
                not self.right[0],
                not self.down[0],
                not self.left[0],
            ]

    def __init__(self, config_path: str) -> None:
        self.config, success = file_parser(config_path)

        if not success:
            raise ValueError("Config file parsing failed")

        self.maze_width = self.config["WIDTH"]
        self.maze_height = self.config["HEIGHT"]
        self.entry = list(self.config["ENTRY"])
        self.exit = list(self.config["EXIT"])
        self.seed = self.config["SEED"]
        self.output_file = self.config["OUTPUT_FILE"]
        self.is_perfect = self.config["PERFECT"]

        self.maze = self.generate_maze()
        self._insert_ft_pattern_in_maze()
        self.sculpt_maze()

        if not self.is_perfect:
            self.make_imperfect()

        self.solution = []

    def get_maze(self):
        return self.maze

    def get_entry(self):
        return self.entry

    def get_exit(self):
        return self.exit

    def get_solution(self):
        return self.solution

    def get_size(self):
        return self.maze_width, self.maze_height

    def generate_maze(self):
        return [
            [
                self.Cell(
                    left=(False, False) if x == 0 else (False, True),
                    right=(False, False)
                    if x == self.maze_width - 1
                    else (False, True),
                    up=(False, False) if y == 0 else (False, True),
                    down=(False, False)
                    if y == self.maze_height - 1
                    else (False, True),
                )
                for x in range(self.maze_width)
            ]
            for y in range(self.maze_height)
        ]

    def display(self):
        for y in range(self.maze_height):
            line = ""

            for x in range(self.maze_width):
                cell = self.maze[y][x]

                line += "+"

                if cell.up[0]:
                    line += "   "
                else:
                    line += "---"

            line += "+"
            print(line)

            line = ""

            for x in range(self.maze_width):
                cell = self.maze[y][x]

                if cell.left[0]:
                    line += " "
                else:
                    line += "|"

                if [x, y] == self.entry:
                    line += " S "
                elif [x, y] == self.exit:
                    line += " E "
                elif self._is_blocked_cell(cell):
                    line += "███"
                else:
                    line += "   "

            last = self.maze[y][self.maze_width - 1]

            if last.right[0]:
                line += " "
            else:
                line += "|"

            print(line)

        line = ""

        for x in range(self.maze_width):
            cell = self.maze[self.maze_height - 1][x]

            line += "+"

            if cell.down[0]:
                line += "   "
            else:
                line += "---"

        line += "+"
        print(line)

    def _is_blocked_cell(self, cell):
        return (
            cell.up[1] is False
            and cell.down[1] is False
            and cell.left[1] is False
            and cell.right[1] is False
        )

    def _cell_is_open(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= self.maze_width or y >= self.maze_height:
            return False
        return not self._is_blocked_cell(self.maze[y][x])

    def _would_create_3x3_open_area(self, x1, y1, x2, y2):
        for start_y in range(
            max(0, min(y1, y2) - 2),
            min(self.maze_height - 2, max(y1, y2)) + 1,
        ):
            for start_x in range(
                max(0, min(x1, x2) - 2),
                min(self.maze_width - 2, max(x1, x2)) + 1,
            ):
                all_open = True

                for dy in range(3):
                    for dx in range(3):
                        cx = start_x + dx
                        cy = start_y + dy

                        if not self._cell_is_open(cx, cy):
                            all_open = False
                            break

                    if not all_open:
                        break

                if all_open:
                    return True

        return False

    def _insert_ft_pattern_in_maze(self):
        ft_pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]

        pattern_h = len(ft_pattern)
        pattern_w = len(ft_pattern[0])

        valid_ft_pattern_pivot = None

        for pivot_y in range(1, self.maze_height - pattern_h):
            for pivot_x in range(1, self.maze_width - pattern_w):
                is_valid = True

                for fth in range(pattern_h):
                    for ftw in range(pattern_w):
                        if ft_pattern[fth][ftw] == 1:
                            maze_x = pivot_x + ftw
                            maze_y = pivot_y + fth

                            if [maze_x, maze_y] == self.entry:
                                is_valid = False

                            if [maze_x, maze_y] == self.exit:
                                is_valid = False

                if is_valid:
                    valid_ft_pattern_pivot = [pivot_x, pivot_y]
                    break

            if valid_ft_pattern_pivot is not None:
                break

        if valid_ft_pattern_pivot is None:
            print("Maze too small or entry/exit blocks the 42 pattern")
            return

        pivot_x = valid_ft_pattern_pivot[0]
        pivot_y = valid_ft_pattern_pivot[1]

        for fth in range(pattern_h):
            for ftw in range(pattern_w):
                if ft_pattern[fth][ftw] == 1:
                    maze_x = pivot_x + ftw
                    maze_y = pivot_y + fth

                    cell = self.maze[maze_y][maze_x]
                    cell.up = [False, False]
                    cell.down = [False, False]
                    cell.left = [False, False]
                    cell.right = [False, False]

    def sculpt_maze(self):
        random.seed(self.seed)

        x, y = self.entry

        self.maze[y][x].isVisited = True
        stack = [(x, y)]

        while stack:
            x, y = stack[-1]
            current = self.maze[y][x]

            neighbors = []

            if y > 0:
                neighbors.append((x, y - 1, "up"))
            if y < self.maze_height - 1:
                neighbors.append((x, y + 1, "down"))
            if x > 0:
                neighbors.append((x - 1, y, "left"))
            if x < self.maze_width - 1:
                neighbors.append((x + 1, y, "right"))

            random.shuffle(neighbors)

            found = False

            for nx, ny, direction in neighbors:
                neighbor = self.maze[ny][nx]

                if neighbor.isVisited:
                    continue

                if direction == "up":
                    if not current.up[1] or not neighbor.down[1]:
                        continue

                    current.up[0] = True
                    neighbor.down[0] = True

                elif direction == "down":
                    if not current.down[1] or not neighbor.up[1]:
                        continue

                    current.down[0] = True
                    neighbor.up[0] = True

                elif direction == "left":
                    if not current.left[1] or not neighbor.right[1]:
                        continue

                    current.left[0] = True
                    neighbor.right[0] = True

                else:
                    if not current.right[1] or not neighbor.left[1]:
                        continue

                    current.right[0] = True
                    neighbor.left[0] = True

                neighbor.isVisited = True
                stack.append((nx, ny))

                found = True
                break

            if not found:
                stack.pop()

    def make_imperfect(self):
        random.seed(self.seed + 1)

        openings = max(1, (self.maze_width * self.maze_height) // 10)
        opened = 0
        attempts = 0
        max_attempts = openings * 50

        while opened < openings and attempts < max_attempts:
            attempts += 1

            x = random.randrange(self.maze_width)
            y = random.randrange(self.maze_height)
            cell = self.maze[y][x]

            if self._is_blocked_cell(cell):
                continue

            directions = []

            if y > 0:
                directions.append((x, y - 1, "up"))
            if y < self.maze_height - 1:
                directions.append((x, y + 1, "down"))
            if x > 0:
                directions.append((x - 1, y, "left"))
            if x < self.maze_width - 1:
                directions.append((x + 1, y, "right"))

            random.shuffle(directions)

            for nx, ny, direction in directions:
                neighbor = self.maze[ny][nx]

                if self._is_blocked_cell(neighbor):
                    continue

                if self._would_create_3x3_open_area(x, y, nx, ny):
                    continue

                if direction == "up" and not cell.up[0]:
                    if cell.up[1] and neighbor.down[1]:
                        cell.up[0] = True
                        neighbor.down[0] = True
                        opened += 1
                        break

                elif direction == "down" and not cell.down[0]:
                    if cell.down[1] and neighbor.up[1]:
                        cell.down[0] = True
                        neighbor.up[0] = True
                        opened += 1
                        break

                elif direction == "left" and not cell.left[0]:
                    if cell.left[1] and neighbor.right[1]:
                        cell.left[0] = True
                        neighbor.right[0] = True
                        opened += 1
                        break

                elif direction == "right" and not cell.right[0]:
                    if cell.right[1] and neighbor.left[1]:
                        cell.right[0] = True
                        neighbor.left[0] = True
                        opened += 1
                        break

    def save_maze(self):
        with open(self.output_file, "w") as file:
            for col in range(self.maze_height):
                for row in range(self.maze_width):
                    number = "".join(
                        str(int(i))
                        for i in self.maze[col][row].getParamsAsList()
                    )
                    file.write(hex(int(number, 2))[2:].capitalize())

                file.write("\n")

            file.write("\n")
            file.write(f"{self.entry}\n")
            file.write(f"{self.exit}\n")
            file.write("shortest path\n")


if __name__ == "__main__":
    try:

        maze = MazeGenerator("../config_test.txt")
        maze.display()
        maze.save_maze()
    except Exception as e:
        print(e.args)
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
            return [not self.up[0], not self.right[0] ,not  self.down[0], not self.left[0]]
    
    class Colors:
        RESET      = "\033[0m"
        BG_BLACK   = "\033[40m"
        BG_RED     = "\033[41m"
        BG_GREEN   = "\033[42m"
        BG_YELLOW  = "\033[43m"
        BG_BLUE    = "\033[44m"
        BG_MAGENTA = "\033[45m"
        BG_CYAN    = "\033[46m"
        BG_WHITE   = "\033[47m"
        BG_ORANGE  = "\033[48;5;214m"
        BG_PINK    = "\033[48;5;213m"
        BG_PURPLE  = "\033[48;5;93m"
        BG_BROWN   = "\033[48;5;130m"

    def __init__(self, config_path: str) -> None:

        self.config, success = file_parser(config_path)

        if not success:
            return  
        
        self.maze_width = self.config["WIDTH"]
        self.maze_height =self.config["HEIGHT"]
        self.entry = list(self.config["ENTRY"])
        self.exit = list(self.config["EXIT"])
        self.seed = self.config["SEED"]
        self.ouput_file = self.config["OUTPUT_FILE"]
        
        self.walls = self.Colors.BG_WHITE
        self.spaces = self.Colors.BG_BLACK
        self.picture = self.Colors.BG_CYAN
        self.color_entry = self.Colors.BG_YELLOW
        self.color_exit = self.Colors.BG_GREEN
        self.neutral = self.Colors.RESET    #always resetting console color
        

        self.maze = self.generate_maze()
        self._insert_ft_pattern_in_maze()
        self.sculpt_maze()
        self.render_maze()
        self.save_maze()
        self.ask_input()

    def generate_maze(self):
        return [
            [
                self.Cell(
                    left=(False, False) if x == 0 else (False, True),
                    right=(False, False) if x == self.maze_width - 1 else (False, True),
                    up=(False, False) if y == 0 else (False, True),
                    down=(False, False) if y == self.maze_height - 1 else (False, True),
                )
                for x in range(self.maze_width)
            ]
            for y in range(self.maze_height)
        ]

    def render_maze(self):
        for y in range(self.maze_height):
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

            line = ""

            for x in range(self.maze_width):
                cell = self.maze[y][x]

                if cell.left[0]:
                    line += f"{self.spaces} {self.neutral}"
                else:
                    line += f"{self.walls} {self.neutral}"

                if [x, y] == self.entry:
                    line += f"{self.color_entry}   {self.neutral}"
                elif [x, y] == self.exit:
                    line += f"{self.color_exit}   {self.neutral}"
                elif self._is_blocked_cell(cell):
                    line += f"{self.picture}   {self.neutral}"
                else:
                    line += f"{self.spaces}   {self.neutral}"

            last = self.maze[y][self.maze_width - 1]

            if last.right[0]:
                line += f"{self.spaces} {self.neutral}"
            else:
                line += f"{self.walls} {self.neutral}"

            print(line)

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

    def _is_blocked_cell(self, cell):
        return (
            cell.up[1] is False
            and cell.down[1] is False
            and cell.left[1] is False
            and cell.right[1] is False
        )

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
        random.seed(self.seed)  # rende il labirinto riproducibile

        x, y = self.entry  # posizione iniziale

        self.maze[y][x].isVisited = True  # marca la partenza
        stack = [(x, y)]  # stack DFS

        while stack:

            x, y = stack[-1]  # ultima cella visitata
            current = self.maze[y][x]

            neighbors = []
            
            # raccoglie i vicini validi
            if y > 0:
                neighbors.append((x, y - 1, "up"))
            if y < self.maze_height - 1:
                neighbors.append((x, y + 1, "down"))
            if x > 0:
                neighbors.append((x - 1, y, "left"))
            if x < self.maze_width - 1:
                neighbors.append((x + 1, y, "right"))

            random.shuffle(neighbors)  # ordine casuale

            found = False  # trovato un vicino?

            for nx, ny, direction in neighbors:

                neighbor = self.maze[ny][nx]

                if neighbor.isVisited:
                    continue  # già visitato

                if direction == "up":
                    # controlla che il passaggio sia consentito
                    if not current.up[1] or not neighbor.down[1]:
                        continue

                    current.up[0] = True      # apre il muro sopra
                    neighbor.down[0] = True   # apre il muro opposto

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

                else:  # right
                    if not current.right[1] or not neighbor.left[1]:
                        continue

                    current.right[0] = True
                    neighbor.left[0] = True

                neighbor.isVisited = True  # marca visitato
                stack.append((nx, ny))     # avanza nel DFS

                found = True
                break  # esplora da questa nuova cella

            if not found:
                stack.pop()  # backtracking
    

    def save_maze(self):
        with open(self.ouput_file, "w") as file:
            for col in range(self.maze_height):
                for row in range(self.maze_width):
                    number = "".join(str(int(i)) for i in self.maze[col][row].getParamsAsList())
                    file.write(hex(int(number, 2))[2:].capitalize())
                file.write("\n")
            file.write("\n")
            file.write(f"{self.entry}\n")
            file.write(f"{self.exit}\n")
            file.write(f"shortest path\n")
    

    def change_colors(self):
        if self.walls == self.Colors.BG_WHITE:
            self.walls = self.Colors.BG_YELLOW
            self.spaces = self.Colors.BG_RED
            self.picture = self.Colors.BG_PURPLE
            self.color_entry = self.Colors.BG_GREEN
            self.color_exit = self.Colors.BG_ORANGE

        elif self.walls == self.Colors.BG_YELLOW:
            self.walls = self.Colors.BG_CYAN
            self.spaces = self.Colors.BG_BLACK
            self.picture = self.Colors.BG_BLUE
            self.color_entry = self.Colors.BG_GREEN
            self.color_exit = self.Colors.BG_MAGENTA

        elif self.walls == self.Colors.BG_CYAN:
            self.walls = self.Colors.BG_GREEN
            self.spaces = self.Colors.BG_BLACK
            self.picture = self.Colors.BG_BROWN
            self.color_entry = self.Colors.BG_YELLOW
            self.color_exit = self.Colors.BG_RED

        elif self.walls == self.Colors.BG_GREEN:
            self.walls = self.Colors.BG_WHITE
            self.spaces = self.Colors.BG_BLACK
            self.picture = self.Colors.BG_BLUE
            self.color_entry = self.Colors.BG_CYAN
            self.color_exit = self.Colors.BG_RED

    
    def ask_input(self):
        value = input(
            f"=== A-Maze-Ing ===\n"
            f"1. Regenerate a new maze\n"
            f"2. Show/Hide path from entry to exit\n"
            f"3. Rotate maze colors\n"
            f"4. Quit\n"
            f"Choice?(1-4)\n"
            )
        if value == "1":
            self.seed = random.randint(1, 400)
            self.maze = self.generate_maze()
            self._insert_ft_pattern_in_maze()
            self.sculpt_maze()
            self.render_maze()
            self.save_maze()
            self.ask_input()
        elif value == "2":
            print("yet to build homie\n")
        elif value == "3":
            self.change_colors()
            self.render_maze()
            self.ask_input()
        elif value == "4":
            print("Quitting it is\n")
        else:
            print("Wrooooooong input BRO.\n"
                  "Pay attention next time.\n")





if __name__ == "__main__":
    MazeGenerator("config_test.txt")

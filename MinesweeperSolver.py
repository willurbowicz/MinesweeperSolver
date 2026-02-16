from collections import deque


class MinesweeperSolver:
    current_game_board = []
    grid_width = 0
    grid_height = 0
    game_window_manager = 0

    def __init__(self, grid_width, grid_height, game_window_manager):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.game_window_manager = game_window_manager
        self.current_game_board = [["-" for _ in range(grid_width)] for _ in
                                   range(grid_height)]

    def is_valid_tile_or_flag(self, x, y):
        is_covered_tile = False
        valid_x = 0 <= x <= len(self.current_game_board[0]) - 1
        valid_y = 0 <= y <= len(self.current_game_board) - 1
        if valid_x and valid_y:
            is_covered_tile = self.current_game_board[y][x] == '-' or self.current_game_board[y][x] == 'F'
        return valid_x and valid_y and is_covered_tile

    def is_valid_tile(self, x, y):
        is_covered_tile = False
        valid_x = 0 <= x <= len(self.current_game_board[0]) - 1
        valid_y = 0 <= y <= len(self.current_game_board) - 1
        if valid_x and valid_y:
            is_covered_tile = self.current_game_board[y][x] == '-'
        return valid_x and valid_y and is_covered_tile

    def find_adjacent_flags(self, x, y):
        adjacent_flags = []
        for x in range(x - 1, x + 2):
            for y in range(y - 1, y + 2):
                if self.is_valid_tile_or_flag(x, y) and self.current_game_board[x][
                    y] == "F":
                    adjacent_flags.append((x, y))

        return adjacent_flags

    def find_adjacent_covered_tiles(self, row_index, col_index):
        adjacent_nodes = []
        for x in range(row_index - 1, row_index + 2):
            for y in range(col_index - 1, col_index + 2):
                if self.is_valid_tile(x, y) and not (x == row_index and y == col_index):
                    adjacent_nodes.append((x, y))

        return adjacent_nodes

    def find_adjacent_tiles(self, row_index, col_index):
        adjacent_nodes = []
        for x in range(row_index - 1, row_index + 2):
            for y in range(col_index - 1, col_index + 2):
                if self.is_valid_tile_or_flag(x, y) and not (x == row_index and y == col_index):
                    adjacent_nodes.append((x, y))

        return adjacent_nodes

    def print_game_state(self):
        print("Current game state:")
        for row in self.current_game_board:
            for element in row:
                print(element, end=" ")
            print()

    def find_flags(self):
        made_move = False
        for col_index, col in enumerate(self.current_game_board):
            for row_index, element in enumerate(col):
                if not element.isnumeric() or element == "0":
                    continue
                adjacent_nodes = self.find_adjacent_tiles(row_index, col_index)

                if len(adjacent_nodes) == int(element) and len(adjacent_nodes) > 0:
                    for adjacent_node in adjacent_nodes:
                        value = self.current_game_board[adjacent_node[1]][adjacent_node[0]]
                        if value == "-":
                            self.game_window_manager.right_click_coordinate(adjacent_node[0], adjacent_node[1])
                            made_move = True
                            self.current_game_board[adjacent_node[1]][adjacent_node[0]] = "F"

        return made_move

    def click_new_tiles(self):
        made_move = False
        for col_index, row in enumerate(self.current_game_board):
            for row_index, element in enumerate(row):
                if not element.isnumeric() or element == "0":
                    continue
                adjacent_nodes = self.find_adjacent_tiles(row_index, col_index)

                num_flags = 0
                for adjacent_node in adjacent_nodes:
                    value = self.current_game_board[adjacent_node[1]][adjacent_node[0]]
                    if value == "F":
                        num_flags += 1
                if not element == 'F':
                    if num_flags == int(element) and len(adjacent_nodes) > num_flags > 0:
                        for adjacent_node in adjacent_nodes:
                            value = self.current_game_board[adjacent_node[1]][adjacent_node[0]]
                            if not value == "F":
                                self.game_window_manager.click_coordinate(adjacent_node[0], adjacent_node[1])
                                made_move = True
                                clicked_tile_value = self.game_window_manager.get_tile_value(adjacent_node[0],
                                                                                             adjacent_node[1])
                                self.current_game_board[adjacent_node[1]][adjacent_node[0]] = clicked_tile_value
                                if clicked_tile_value == "0":
                                    tiles_to_check = deque(
                                        self.find_adjacent_covered_tiles(adjacent_node[0], adjacent_node[1]))
                                    while len(tiles_to_check) > 0:
                                        self.resolve_unknown_tiles(tiles_to_check)
                                        tiles_to_check.popleft()
        return made_move

    def resolve_unknown_tiles(self, queue):
        for tile in queue:
            clicked_tile_value = self.game_window_manager.get_tile_value(tile[0], tile[1])
            self.current_game_board[tile[1]][tile[0]] = clicked_tile_value
            if clicked_tile_value == "0":
                self.resolve_unknown_tiles(deque(self.find_adjacent_tiles(tile[0], tile[1])))

    def has_won(self):
        for row in self.current_game_board:
            for cell in row:
                if cell == "-":
                    return False
        return True

    def has_lost(self):
        for row in self.current_game_board:
            for cell in row:
                if cell == "B":
                    return True

        return False

    def calculate_constraints(self):
        constraints = []
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if not self.current_game_board[y][x].isnumeric() or self.current_game_board[y][x] == "0":
                    continue
                adjacent_nodes = self.find_adjacent_tiles(x, y)
                unknowns = set()
                flags = 0
                for node in adjacent_nodes:
                    if self.current_game_board[node[1]][node[0]] == "-":
                        unknowns.add(node)
                    elif self.current_game_board[node[1]][node[0]] == "F":
                        flags += 1
                if not unknowns:
                    continue
                mines = int(self.current_game_board[y][x]) - flags
                constraint = ((x, y), mines, unknowns)
                if len(constraint) != 3:
                    continue
                constraints.append(((x, y), mines, unknowns))
        return constraints

    def perform_subset_logic(self):
        constraints = self.calculate_constraints()
        for i in range(len(constraints)):
            for j in range(i + 1, len(constraints)):
                origin_j, mines_j, unknowns_j = constraints[j]
                origin_i, mines_i, unknowns_i = constraints[i]
                if unknowns_j.issubset(unknowns_i):

                    if mines_j > mines_i:
                        continue

                    diff_tiles = unknowns_i - unknowns_j
                    diff_mines = mines_i - mines_j
                    if diff_tiles:
                        if diff_mines == 0:
                            print(f"safe tiles: {diff_tiles}")
                            tile = next(iter(diff_tiles))
                            return tile, False
                        elif diff_mines == len(diff_tiles):
                            print(f"all mines: {diff_tiles}")
                            tile = next(iter(diff_tiles))
                            return tile, True

                elif unknowns_i.issubset(unknowns_j):
                    if mines_i > mines_j:
                        continue

                    diff_tiles = unknowns_j - unknowns_i
                    diff_mines = mines_j - mines_i
                    if diff_tiles:
                        if diff_mines == 0:
                            print(f"safe tiles: {diff_tiles}")
                            tile = next(iter(diff_tiles))
                            return tile, False
                        elif diff_mines == len(diff_tiles):
                            print(f"all mines: {diff_tiles}")
                            tile = next(iter(diff_tiles))
                            return tile, True
                else:
                    print("Really stuck, need to guess")
                    best_guess = ((0, 0), 0)
                    for constraint in constraints:
                        diff = len(constraint[2]) - constraint[1]
                        chance_of_safe = diff / len(constraint[2])
                        if chance_of_safe > best_guess[1]:
                            best_guess = (constraint, chance_of_safe)

                    tile = best_guess[0][2].pop()
                    return tile, False

    # def play_game(self):

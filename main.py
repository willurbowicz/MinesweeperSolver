import time
from collections import deque

import pyautogui

from GameWindowManager import GameWindowManager


def is_valid_tile_or_flag(x, y):
    is_covered_tile = False
    valid_x = 0 <= x <= len(current_game_board[0]) - 1
    valid_y = 0 <= y <= len(current_game_board) - 1
    if valid_x and valid_y:
        is_covered_tile = current_game_board[y][x] == '-' or current_game_board[y][x] == 'F'
    return valid_x and valid_y and is_covered_tile


def is_valid_tile(x, y):
    is_covered_tile = False
    valid_x = 0 <= x <= len(current_game_board[0]) - 1
    valid_y = 0 <= y <= len(current_game_board) - 1
    if valid_x and valid_y:
        is_covered_tile = current_game_board[y][x] == '-'
    return valid_x and valid_y and is_covered_tile


def find_adjacent_covered_tiles(row_index, col_index):
    adjacent_nodes = []
    for x in range(row_index - 1, row_index + 2):
        for y in range(col_index - 1, col_index + 2):
            if is_valid_tile(x, y) and not (x == row_index and y == col_index):
                adjacent_nodes.append((x, y))

    return adjacent_nodes


def find_adjacent_tiles(row_index, col_index):
    adjacent_nodes = []
    for x in range(row_index - 1, row_index + 2):
        for y in range(col_index - 1, col_index + 2):
            if is_valid_tile_or_flag(x, y) and not (x == row_index and y == col_index):
                adjacent_nodes.append((x, y))

    return adjacent_nodes


def build_game_state():
    for row_index, row in enumerate(current_game_board):
        for col_index, element in enumerate(row):
            x_offset = (col_index * game_window_manager.square_width) + game_window_manager.starting_x
            y_offset = (row_index * game_window_manager.square_width) + game_window_manager.starting_y
            current_game_board[row_index][col_index] = calculate_square_value(x_offset, y_offset)

    # print_game_state()


def print_game_state():
    print("Current game state:")
    for row in current_game_board:
        for element in row:
            print(element, end=" ")
        print()


def calculate_square_value(x, y):
    tile_color = pyautogui.pixel(x, y)
    match tile_color:
        case (189, 189, 189):
            if (pyautogui.pixel(x, y + 7)) != tile_color:
                return "-"  # unselected tile
            return "0"  # empty tile
        case (0, 0, 255):
            return "1"
        case (0, 123, 0):
            return "2"
        case (255, 0, 0):
            return "3"
        case (0, 0, 123):
            return "4"
        case (123, 0, 0):
            return "5"
        case (0, 0, 0):
            return "F"
        case _:
            return "?"


def find_flags():
    made_move = False
    for col_index, col in enumerate(current_game_board):
        for row_index, element in enumerate(col):
            if not element.isnumeric() or element == "0":
                continue
            adjacent_nodes = find_adjacent_tiles(row_index, col_index)

            if len(adjacent_nodes) == int(element) and len(adjacent_nodes) > 0:
                for adjacent_node in adjacent_nodes:
                    value = current_game_board[adjacent_node[1]][adjacent_node[0]]
                    if value == "-":
                        game_window_manager.right_click_coordinate(adjacent_node[0], adjacent_node[1])
                        made_move = True
                        current_game_board[adjacent_node[1]][adjacent_node[0]] = "F"

    return made_move


def click_new_tiles():
    made_move = False
    for col_index, row in enumerate(current_game_board):
        for row_index, element in enumerate(row):
            if not element.isnumeric() or element == "0":
                continue
            adjacent_nodes = find_adjacent_tiles(row_index, col_index)

            num_flags = 0
            for adjacent_node in adjacent_nodes:
                value = current_game_board[adjacent_node[1]][adjacent_node[0]]
                if value == "F":
                    num_flags += 1
            if not element == 'F':
                if num_flags == int(element) and len(adjacent_nodes) > num_flags > 0:
                    for adjacent_node in adjacent_nodes:
                        value = current_game_board[adjacent_node[1]][adjacent_node[0]]
                        if not value == "F":
                            game_window_manager.click_coordinate(adjacent_node[0], adjacent_node[1])
                            time.sleep(0.05)
                            made_move = True
                            clicked_tile_value = calculate_square_value(
                                (adjacent_node[0] * game_window_manager.square_width) + game_window_manager.starting_x,
                                (adjacent_node[1] * game_window_manager.square_width) + game_window_manager.starting_y)
                            current_game_board[adjacent_node[1]][adjacent_node[0]] = clicked_tile_value
                            if clicked_tile_value == "0":
                                tiles_to_check = deque(find_adjacent_covered_tiles(adjacent_node[0], adjacent_node[1]))
                                while len(tiles_to_check) > 0:
                                    resolve_unknown_tiles(tiles_to_check)
                                    tiles_to_check.popleft()
    return made_move


def resolve_unknown_tiles(queue):
    for tile in queue:
        # time.sleep(0.05)
        clicked_tile_value = calculate_square_value(
            (tile[0] * game_window_manager.square_width) + game_window_manager.starting_x,
            (tile[1] * game_window_manager.square_width) + game_window_manager.starting_y)
        current_game_board[tile[1]][tile[0]] = clicked_tile_value
        if clicked_tile_value == "0":
            resolve_unknown_tiles(deque(find_adjacent_tiles(tile[0], tile[1])))


def has_won():
    for row in current_game_board:
        for cell in row:
            if cell == "-":
                return False
    return True


if __name__ == "__main__":
    # # Test code for getting the pixel color at cursor location
    # currx, curry = pyautogui.position()
    # print(pyautogui.position())
    # print(pyautogui.pixel(currx, curry))

    game_window_manager = GameWindowManager()

    current_game_board = [["-" for x in range(game_window_manager.grid_width)] for y in
                          range(game_window_manager.grid_width)]

    game_window_manager.restart_game()
    game_window_manager.click_random_tile()

    has_easy_moves = True
    game_over = False
    # global current_game_board
    # current_game_board = [["-" for x in range(grid_width)] for y in range(grid_width)]
    build_game_state()

    while not game_over:
        while has_easy_moves:
            one = find_flags()
            two = click_new_tiles()

            if not (one or two):
                has_easy_moves = False

        # Ensure the victory popup has finished loading, then close it
        time.sleep(0.5)
        pyautogui.click(4019, 251)

        # if game_window_manager.get_game_state() == 'lose':
        #     # if pyautogui.pixel(game_window_manager.loss_pixel[0], game_window_manager.loss_pixel[1]) == (0, 0, 0):
        #     # if pyautogui.pixel(3467, 293) == (0, 0, 0):
        #     # if pyautogui.pixel(3634, 293) == (0, 0, 0):
        #     print("You lose.")
        #     game_over = True
        print_game_state()
        if has_won():
            print("You Win!")
            game_over = True
        else:
            print("Really stuck, need to guess")
            exit()
            # # print_game_state()
            # clicked = False
            # for j in range(game_window_manager.grid_width):
            #     for i in range(game_window_manager.grid_width):
            #         value = current_game_board[i][j]
            #         if value == "-":
            #             game_window_manager.click_coordinate(j, i)
            #             # found_tile = calculate_square_value(
            #             #     (i * game_window_manager.square_width) + game_window_manager.starting_x,
            #             #     (j * game_window_manager.square_width) + game_window_manager.starting_y)
            #             # current_game_board[i][j] = found_tile
            #             clicked = True
            #             has_easy_moves = True
            #             # print_game_state()
            #             # print("test")
            #             break
            #     # if clicked:
            #     #     break

            # continue

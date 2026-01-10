import random
import time

import keyboard
import pyautogui
# from collections import deque


def restart_game():
    pyautogui.click(3467, 293)

def is_valid_tile_or_flag(x, y):
    is_covered_tile = False
    valid_x = 0 <= x <= len(current_game_board[0]) - 1
    valid_y = 0 <= y <= len(current_game_board) - 1
    if valid_x and valid_y:
        is_covered_tile = current_game_board[y][x] == '-' or current_game_board[y][x] == 'F'
    return valid_x and valid_y and is_covered_tile

def is_valid_tile(x, y):
    is_covered_tile = False
    valid_x = 0 <= x <= len(current_game_board[0])-1
    valid_y = 0 <= y <= len(current_game_board)-1
    if valid_x and valid_y:
        is_covered_tile = current_game_board[y][x] == '-'
    return valid_x and valid_y and is_covered_tile

def find_adjacent_covered_tiles(row_index, col_index):
    adjacent_nodes = []
    for x in range(row_index-1, row_index+2):
        for y in range(col_index-1, col_index+2):
            if is_valid_tile(x, y) and not (x == row_index and y == col_index):
                adjacent_nodes.append((x,y))

    return adjacent_nodes

def find_adjacent_tiles(row_index, col_index):
    adjacent_nodes = []
    for x in range(row_index-1, row_index+2):
        for y in range(col_index-1, col_index+2):
            if is_valid_tile_or_flag(x, y) and not (x == row_index and y == col_index):
                adjacent_nodes.append((x,y))

    return adjacent_nodes


def click_random_tile():
    click_coordinate((random.randrange(0, grid_width)),(random.randrange(0, grid_width)))

def click_coordinate(x,y):
    x_coord = (x * square_width) + starting_x
    y_coord = (y * square_width) + starting_y
    pyautogui.click(x_coord, y_coord)

def right_click_coordinate(x,y):
    x_coord = (x * square_width) + starting_x
    y_coord = (y * square_width) + starting_y
    pyautogui.rightClick(x_coord, y_coord)

def build_game_state():
    for row_index, row in enumerate(current_game_board):
        for col_index, element in enumerate(row):
            x_offset = (col_index * square_width) + starting_x
            y_offset = (row_index * square_width) + starting_y
            current_game_board[row_index][col_index] = calculate_square_value(x_offset, y_offset)

    print_game_state()

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
            if (pyautogui.pixel(x, y+7)) != tile_color:
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
        case (0, 0, 0):
            return "F"
        case _:
            return "?"


def find_flags():
    print("Finding flags")
    for col_index, col in enumerate(current_game_board):
        for row_index, element in enumerate(col):
            if not element.isnumeric() or element == "0":
                continue
            # print(f"Finding adjacent nodes for: {row_index}, {col_index}: {element}")
            adjacent_nodes = find_adjacent_tiles(row_index, col_index)
            # print(f"Adjacent nodes: {adjacent_nodes}")

            if len(adjacent_nodes) == int(element) and len(adjacent_nodes) > 0:
                for adjacent_node in adjacent_nodes:
                    # value = calculate_square_value((adjacent_node[0] * square_width) + starting_x, (adjacent_node[1] * square_width) + starting_y)
                    value = current_game_board[adjacent_node[1]][adjacent_node[0]]
                    if value == "-":
                        right_click_coordinate(adjacent_node[0], adjacent_node[1])
                        current_game_board[adjacent_node[1]][adjacent_node[0]] = "F"


def click_new_tiles():
    for col_index, row in enumerate(current_game_board):
        for row_index, element in enumerate(row):
            if not element.isnumeric() or element == "0":
                continue
            adjacent_nodes = find_adjacent_tiles(row_index, col_index)

            num_flags = 0
            for adjacent_node in adjacent_nodes:
                # value = calculate_square_value((adjacent_node[0] * square_width) + starting_x, (adjacent_node[1]* square_width) + starting_y)
                value = current_game_board[adjacent_node[1]][adjacent_node[0]]
                if value == "F":
                    num_flags += 1
            if not element == 'F':
                if num_flags == int(element) and len(adjacent_nodes) > num_flags > 0:
                    # print(f"Flags = number for tile {row_index, col_index}, safe to click")
                    for adjacent_node in adjacent_nodes:
                        # value = calculate_square_value((adjacent_node[0] * square_width) + starting_x, (adjacent_node[1] * square_width) + starting_y)
                        value = current_game_board[adjacent_node[1]][adjacent_node[0]]
                        if not value == "F":
                            click_coordinate(adjacent_node[0], adjacent_node[1])
                            # clicked_tile_value = calculate_square_value((adjacent_node[0] * square_width) + starting_x, (adjacent_node[1] * square_width) + starting_y)
                            # tiles_to_check = deque()
                            # if clicked_tile_value == "0":
                            #     tiles_to_check.append(adjacent_node)


if __name__ == "__main__":
    # starting_x = 3600-- 3321-- 3371
    # starting_y = 205-- 389-- 390
    # square_width = 16
    # Assumes the zoom level is set to 300%
    starting_x = 3278
    starting_y = 399
    square_width = 48
    # small size board
    grid_width = 9
    # medium size board
    # grid_width = 16

    # currx, curry = pyautogui.position()
    # print(pyautogui.position())
    # print(pyautogui.pixel(currx, curry))
    # #play = False
    play = True
    restart_game()
    click_random_tile()
    # games_played = 1

    global current_game_board
    current_game_board = [["-" for x in range(grid_width)] for y in range(grid_width)]
    # print("Starting game: ",games_played)

    while play:
        # start_time = time.time()
        # Kill switch
        if keyboard.is_pressed('space'):
            play = False

        # Check if game has been lost
        # if pyautogui.pixel(3467, 293)== (0, 0, 0):
        #     print("Game Over")
        #     games_played += 1
        #     print ("Starting game: ", games_played)
        #     restart_game()
        #
        # # Check if game has been won
        # if pyautogui.pixel(3466, 278) == (0, 0, 0):
        #     print("You Win!")
        #     play = False

        # Build out game board state to make decisions
        build_game_state()
        # Calculate any missing flags from the board
        find_flags()
        # build_game_state()
        click_new_tiles()
        # end_time = time.time()
        # elapsed_time = end_time - start_time
        # print(f"Elapsed time for game loop: {elapsed_time}")
        if pyautogui.pixel(3466, 278) == (0, 0, 0) or pyautogui.pixel(3467, 293)== (0, 0, 0):
            play = False


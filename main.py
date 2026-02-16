from collections import deque

from GameWindowManager import GameWindowManager
from MinesweeperSolver import MinesweeperSolver

if __name__ == "__main__":
    game_window_manager = GameWindowManager()
    minesweeper_solver = MinesweeperSolver(game_window_manager.grid_width, game_window_manager.grid_height,
                                           game_window_manager)

    game_window_manager.reset_game()

    has_easy_moves = True
    game_over = False
    game_window_manager.click_coordinate(0, 0)
    found_tile = game_window_manager.get_tile_value(0, 0)
    minesweeper_solver.current_game_board[0][0] = found_tile
    if found_tile == "0":
        tiles_to_check = deque(minesweeper_solver.find_adjacent_covered_tiles(0, 0))
        while len(tiles_to_check) > 0:
            minesweeper_solver.resolve_unknown_tiles(tiles_to_check)
            tiles_to_check.popleft()

    while not game_over:
        while has_easy_moves:
            game_window_manager.handle_banner()
            one = minesweeper_solver.find_flags()
            two = minesweeper_solver.click_new_tiles()

            if not (one or two):
                has_easy_moves = False

        if minesweeper_solver.has_won():
            print("You Win!")
            minesweeper_solver.print_game_state()
            game_over = True
            break
        elif minesweeper_solver.has_lost():
            print("You Lose!")
            minesweeper_solver.print_game_state()
            game_over = True
            break
        else:
            tile, is_bomb = minesweeper_solver.perform_subset_logic()
            found_tile = game_window_manager.get_tile_value(tile[0], tile[1])
            if is_bomb:
                game_window_manager.right_click_coordinate(tile[0], tile[1])
                minesweeper_solver.current_game_board[tile[1]][tile[0]] = "F"
            else:
                game_window_manager.click_coordinate(tile[0], tile[1])
                value = game_window_manager.get_tile_value(tile[0], tile[1])
                minesweeper_solver.current_game_board[tile[1]][tile[0]] = value
                if value == "B":
                    print("You Lose!")
                    minesweeper_solver.print_game_state()
                    game_over = True
                    break
                if value == "0":
                    tiles_to_check = deque(minesweeper_solver.find_adjacent_covered_tiles(tile[0], tile[1]))
                    while len(tiles_to_check) > 0:
                        minesweeper_solver.resolve_unknown_tiles(tiles_to_check)
                        tiles_to_check.popleft()
            has_easy_moves = True

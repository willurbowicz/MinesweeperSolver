import random
import time

import mss
import pyautogui


class GameWindowManager:
    # Assumes the zoom level is set to 300%
    starting_x = 3278
    starting_y = 399
    # square_width = 48

    top_left_coord = (0, 0)
    smiley_coord = (0, 0)
    loss_pixel = (0, 0)
    win_pixel = (0, 0)

    grid_width = 0
    grid_height = 0
    square_width = 0

    SMILEYS = {
        "win": "resources/win.png",
        "lose": "resources/lose.png",
        "playing": "resources/smiley.png",
    }

    TILES = {
        "resources/tiles/tileBlank.png": "-",
        "resources/tiles/tile0.png": "0",
        "resources/tiles/tile1.png": "1",
        "resources/tiles/tile2.png": "2",
        "resources/tiles/tile3.png": "3",
        "resources/tiles/tile4.png": "4",
        "resources/tiles/tile5.png": "5",
        # "resources/tiles/tile6.png": "6",
        # "resources/tiles/tile7.png": "7",
        # "resources/tiles/tile8.png": "8",
        "resources/tiles/tileFlag.png": "F",
        "resources/tiles/tileBomb.png": "B",
    }

    def __init__(self):
        self.find_board_locations()

    def find_board_locations(self):
        location = self.get_smiley_location()
        if location is None:
            raise RuntimeError("Board not found on any monitor")
        self.smiley_coord = (location.left + location.width / 2, location.top + location.height / 2)
        pyautogui.click(self.smiley_coord)
        location = self.get_smiley_location()
        starting_tile = (int(self.smiley_coord[0]), int(self.smiley_coord[1] + location.height * 1.5))
        center = self.get_center_of_tile(starting_tile)
        self.top_left_coord = self.find_first_tile(center)
        self.count_board_width_and_height()
        print(f"Grid width: {self.grid_width}, Grid height: {self.grid_height}")

    def find_first_tile(self, tile):
        first_tile = tile
        board_width = 0
        cont = True
        top_left_tile = (0, 0)
        while cont:
            tile_to_check = (first_tile[0] - (board_width * self.square_width), first_tile[1])
            if pyautogui.pixel(int(tile_to_check[0]), int(tile_to_check[1])) == (255, 255, 255):
                top_left_tile = int(tile_to_check[0]) + (self.square_width * 2), int(tile_to_check[1])
                cont = False
            else:
                board_width += 1

        return top_left_tile

    def count_board_width_and_height(self):
        board_width = 0
        board_height = 0
        tile = self.top_left_coord
        cont = True
        while cont:
            tile_to_check = (tile[0] + (board_width * self.square_width), tile[1])
            if pyautogui.pixel(int(tile_to_check[0]), int(tile_to_check[1])) == (255, 255, 255):
                cont = False
            else:
                board_width += 1
        self.grid_width = board_width - 1

        cont = True
        while cont:
            tile_to_check = (tile[0], tile[1] + (board_height * self.square_width))
            if pyautogui.pixel(int(tile_to_check[0]), int(tile_to_check[1])) == (255, 255, 255):
                cont = False
            else:
                board_height += 1
        self.grid_height = board_height - 1

    def get_center_of_tile(self, orig_coord):
        coord = (int(orig_coord[0]) + 10, int(orig_coord[1]))
        primary_color = (189, 189, 189)
        left = 0
        right = 0
        up = 0
        down = 0
        go = True
        while go:
            # left
            if pyautogui.pixel(coord[0] + left, coord[1]) != primary_color:
                go = False
            else:
                left -= 1
        go = True
        while go:
            # right
            if pyautogui.pixel(coord[0] + right, coord[1]) != primary_color:
                go = False
            else:
                right += 1
        go = True
        while go:
            # up
            if pyautogui.pixel(coord[0], coord[1] + up) != primary_color:
                go = False
            else:
                up -= 1
        go = True
        while go:
            # down
            if pyautogui.pixel(coord[0], coord[1] + down) != primary_color:
                go = False
            else:
                down += 1
        center = (coord[0] + (left + right) / 2, coord[1] + (up + down) / 2)

        self.square_width = abs(left) + abs(right) + 13
        return center

    def convert_board_coords_to_pixels(self, x, y):
        screen_x = self.top_left_coord[0] + (x * self.square_width)
        screen_y = self.top_left_coord[1] + (y * self.square_width)
        # tile = self.get_center_of_tile((screen_x, screen_y))
        return screen_x, screen_y

    def handle_banner(self):
        with mss.mss() as sct:
            # Capture the entire virtual screen (all monitors)
            all_monitors_screenshot = sct.grab(sct.monitors[0])

            # Save to file
            output = "board.png"
            mss.tools.to_png(all_monitors_screenshot.rgb, all_monitors_screenshot.size, output=output)
            try:
                location = pyautogui.locate(
                    "resources/banner.png", "board.png", confidence=0.8
                )
                if location:
                    pyautogui.click(location.left + (location.width / 2), location.top + (location.height / 2))
                    time.sleep(1)

            except pyautogui.ImageNotFoundException:
                pass

    def get_tile_value(self, board_x, board_y):
        x, y = self.convert_board_coords_to_pixels(board_x, board_y)
        tile_to_check = (int(x - (self.square_width / 2)), int(y - (self.square_width / 2)),
                         int(x + (self.square_width / 2)), int(y + (self.square_width / 2)))

        with mss.mss() as sct:
            sct_img = sct.grab(tile_to_check)
            output = "tile.png"
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

            for template in self.TILES.keys():
                try:
                    location = pyautogui.locate(
                        template, "tile.png", confidence=0.8
                    )
                    if location:
                        return self.TILES.get(template)

                except pyautogui.ImageNotFoundException:
                    continue

        return None

    def get_smiley_location(self):
        with mss.mss() as sct:
            # Capture the entire virtual screen (all monitors)
            all_monitors_screenshot = sct.grab(sct.monitors[0])

            # Save to file
            output = "board.png"
            mss.tools.to_png(all_monitors_screenshot.rgb, all_monitors_screenshot.size, output=output)

            for template in self.SMILEYS.values():
                try:
                    location = pyautogui.locate(
                        template, "board.png", confidence=0.8
                    )
                    if location:
                        return location

                except pyautogui.ImageNotFoundException:
                    continue

        return None

    def click_coordinate(self, x, y):
        x_coord = (x * self.square_width) + self.top_left_coord[0]
        y_coord = (y * self.square_width) + self.top_left_coord[1]
        pyautogui.click(x_coord, y_coord)

    def right_click_coordinate(self, x, y):
        x_coord = (x * self.square_width) + self.top_left_coord[0]
        y_coord = (y * self.square_width) + self.top_left_coord[1]
        pyautogui.rightClick(x_coord, y_coord)

    def click_random_tile(self):
        self.click_coordinate((random.randrange(0, self.grid_width)),
                              (random.randrange(0, self.grid_width)))

    def restart_game(self):
        pyautogui.click(self.smiley_coord[0], self.smiley_coord[1])

import random

import mss
import pyautogui
from PIL import Image


class GameWindowManager:
    # Assumes the zoom level is set to 300%
    starting_x = 3278
    starting_y = 399
    square_width = 48
    # small size board
    # grid_width = 9

    # medium size board
    grid_width = 16

    def __init__(self):
        self.get_board_location_from_screenshot()

    def get_board_location_from_screenshot(self):
        # self.restart_game()
        with mss.mss() as sct:
            monitor_all = sct.monitors[0]
            sct_img = sct.grab(monitor_all)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            # Save the image
            img.save("board.png")

        board_image = 'board.png'
        smiley_image = 'resources/smiley.png'
        # Check if the template image exists in the main image file
        try:
            # locateOnScreen() can take a screenshot of the current screen,
            # but locate() is used to search within an existing file.
            # We specify a confidence level (requires OpenCV to be installed).
            location = pyautogui.locate(smiley_image, board_image, confidence=0.8)

            if location:
                print(f"Image found at coordinates (left, top, width, height): {location}")
                # Convert to boolean True/False
                image_exists = True
            else:
                print("Image not found.")
                image_exists = False

        except pyautogui.ImageNotFoundException:
            print("ImageNotFoundException: Template not found.")
            image_exists = False
            exit()
        except Exception as e:
            print(f"An error occurred: {e}")
            image_exists = False
            exit()

        print(f"Result: {image_exists}")

    def click_coordinate(self, x, y):
        x_coord = (x * self.square_width) + self.starting_x
        y_coord = (y * self.square_width) + self.starting_y
        pyautogui.click(x_coord, y_coord)

    def right_click_coordinate(self, x, y):
        x_coord = (x * self.square_width) + self.starting_x
        y_coord = (y * self.square_width) + self.starting_y
        pyautogui.rightClick(x_coord, y_coord)

    def click_random_tile(self):
        self.click_coordinate((random.randrange(0, self.grid_width)),
                              (random.randrange(0, self.grid_width)))

    def restart_game(self):
        # beginner
        pyautogui.click(3467, 293)
        # intermediate
        pyautogui.click(3634, 293)

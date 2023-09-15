import pyautogui
import time


def divide_number(number):
    parts = 1  # Starting with 4 parts

    while parts >= 1:
        if number % parts == 0:  # Check if the number is divisible into 'parts' equal parts
            equal_parts = number // parts  # Calculate the value of each equal part
            return equal_parts  # Return the divided number
        else:
            parts += 1  # Increment the number of parts and try again

    return None  # If no valid division is found, return None

def get_screen_grid_points():

    # Get the screen size
    screen_width, screen_height = pyautogui.size()

    grid_spacing_x = divide_number(screen_width)
    grid_spacing_y = divide_number(screen_height)

    # Calculate the number of grid points in each direction
    num_points_x = screen_width // grid_spacing_x
    num_points_y = screen_height // grid_spacing_y

    # Generate grid points
    grid_points = []
    for y in range(num_points_y + 1): # Example. 1080 height, is num_points_y, on 4 iteration it will cover till 810 becasue of 0 index.
        for x in range(num_points_x + 1):
            point = (x * grid_spacing_x, y * grid_spacing_y)
            grid_points.append(point)

    return grid_points


if __name__ == "__main__":
    get_screen_grid_points()
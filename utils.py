import pyautogui

# Disable the fail-safe mechanism
pyautogui.FAILSAFE = False

def move_mouse_to_point(pt):
        try:
            # Get the current mouse position
            current_x, current_y = pyautogui.position()
            pyautogui.moveTo(current_x + pt[0], current_y + pt[1], _pause=False)
        except Exception as e:
            print(f"An error occurred: {e}")

def point_inside_rectangle(x, y, rect_x, rect_y, rect_width, rect_height):
    return rect_x <= x < rect_x + rect_width and rect_y <= y < rect_y + rect_height

def relative_position(x, y, rect_x, rect_y):
    relative_x = x - rect_x
    relative_y = y - rect_y
    return relative_x, relative_y



def split_rectangle_into_grid(image, x, y, width, height):
    # Calculate the size of each row and column in the grid
    row_width = [int(width * 0.40), int(width * 0.2), int(width * 0.4)]
    col_height = [int(height * 0.45), int(height * 0.1), int(height * 0.45)]

    # Initialize an empty list to store the grid cells
    grid_cells = []
    GRID_size = 3

    cells = []
    for _ in range(GRID_size):
        row = []
        for _ in range(GRID_size):
            row.append(None)
        cells.append(row)

    labels = [
        ["top-left", "top", "top-right"],
        ["middle-left", "middle", "middle-right"],
        ["bottom-left", "bottom", "bottom-right"],
    ]

    for i in range(GRID_size):
        for j in range(GRID_size):

            cell_x = x + sum(row_width[:j])
            cell_y = y + sum(col_height[:i])

            cell_width = row_width[j]
            cell_height = col_height[i]

            cells[i][j] = (cell_x, cell_y, cell_width, cell_height, labels[i][j])
    
    return cells

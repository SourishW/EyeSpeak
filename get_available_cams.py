import cv2
import tkinter as tk
from tkinter import ttk

def check_available_cameras():
    index = 0
    available_cameras = []

    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            available_cameras.append(index)
            cap.release()
        index += 1
    return available_cameras

'''
Select from Available cameras.
'''
def show_camera_selection_GUI():
    def get_selected_index(dropdown, root, result):
        result['selected_index'] = dropdown.current()
        root.destroy()  # Close the GUI window
    
    
    # Call the function to check available cameras
    available_cameras = check_available_cameras()

    root = tk.Tk()
    root.title("Select Camera")
    root.resizable(False, False)
    window_width = 400
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y - window_height // 2}")

    # Create a style for the dropdown
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox", padding=6, width=20)

    # Create a list of options for the dropdown
    options = []
    for opt in available_cameras:
        options.append("Camera: " + str(opt))


    # Create a tkinter variable to store the selected option
    selected_option = tk.StringVar(root)

    # Create the dropdown widget
    dropdown = ttk.Combobox(root, textvariable=selected_option, values=options)
    dropdown.pack(pady=20)

    # Create a dictionary to store the result
    result = {'selected_index': None}

    # Create a button to get the selected index
    button = ttk.Button(root, text="Use Camera", command=lambda: get_selected_index(dropdown, root, result))
    button.pack()

    root.mainloop()
    return result['selected_index']
'''
Select from Available cameras - Ended.
'''
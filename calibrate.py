import tkinter as tk
import time
import sys
import threading
from eyetracker import EyeTracker
import cv2

cap = cv2.VideoCapture(0)

class RedBallGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Red Ball GUI")
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Set the tkinter window size to match the screen size
        root.geometry(f"{screen_width}x{screen_height}")


        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Fill the entire window
        
        self.ball_radius = 30
        self.ball_color = "red"
        self.ball = None  # Will hold the ball object

        self.__updated = False
        self.__cached_ball_x = 0
        self.__cached_ball_y = 0
        
    def create_ball(self, x, y):
        if self.ball:
            self.canvas.delete(self.ball)  # Delete existing ball if it exists
        self.ball = self.canvas.create_oval(
            x - self.ball_radius,
            y - self.ball_radius,
            x + self.ball_radius,
            y + self.ball_radius,
            fill=self.ball_color
        )
    
    def place_ball(self, x, y):
        self.__updated = True
        self.__cached_ball_x = x
        self.__cached_ball_y = y


    def __place_ball(self):
        if self.__updated:
            self.create_ball(self.__cached_ball_x, self.__cached_ball_y)
        self.__updated = False
    
    def clear_ball(self):
        if self.ball:
            self.canvas.delete(self.ball)
            self.ball = None
    
    def periodic_check(self, root):

        self.__place_ball()
        root.after(int(1000.0/60.0), lambda:self.periodic_check(root))

def get_target_coordinates(screen_width, screen_height):
    x = 0
    y = 0

    coordinates = []
    number_of_divisions = 5
    divisions = [i*(int(screen_height / number_of_divisions ) -1) for i in range(number_of_divisions)]

    for y_coordinate in divisions:
        x = 0
        while(x < screen_width):
            coordinates.append((x, y_coordinate)) 
            x += 400   

    return coordinates

def real_thread(app:RedBallGUI, screen_width, screen_height):
    coordinates = get_target_coordinates(screen_width, screen_height)
    my_tracker = EyeTracker()

    for x, y in coordinates:
        start_time = time.time()
        while time.time()-start_time < 2:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            my_tracker.add_frame_to_train_on(frame, (x,y))
            # cv2.imshow("frame",frame)

        app.place_ball(x, y)

    print("hi")
    my_tracker.train_model()
    while(True):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        x, y = my_tracker.track_eye_gaze()
        print(x, y)
        app.place_ball(x, y)
        key = cv2.waitKey(30)
        if key == ord('q'):
            break





def do_exit(root, mythread):
    root.quit()
    root.destroy()
    exit()
    


if __name__ == "__main__":
    root = tk.Tk()
    app = RedBallGUI(root)
    app.periodic_check(root)
    my_thread = threading.Thread(target=real_thread, args=(app,root.winfo_screenwidth(), root.winfo_screenheight()))
    my_thread.start()
    root.protocol("WM_DELETE_WINDOW", lambda:do_exit(root, my_thread))
    root.mainloop()

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from get_available_cams import check_available_cameras
import time
import pyautogui
from screen_grid import get_screen_grid_points
from iris import get_iris
from screen_calibration import calibrate_point
import mediapipe as mp 
import utils
from get_available_cams import show_camera_selection_GUI

# Disable the fail-safe mechanism
pyautogui.FAILSAFE = False

# Right eye convexHull indices list
RIGHT_EYE=[ 382, 256, 252, 253, 254, 339, 466, 260, 259, 257, 258, 286, 398] 
# irises Indices list
RIGHT_IRIS = [474,475, 476, 477]
LEFT_IRIS = [469, 470, 471, 472]


class VideoCaptureApp:
    def __init__(self, video_source=0, duration=30):
        self.video_source = video_source
        self.duration = duration
        self.initalizeCalibrationScreen()
        self.splitEyeProcess(self.video_source)
        
    def initalizeCalibrationScreen(self):
        # Create a Tkinter window
        self.window = tk.Tk()
       
        # Get the screen size
        self.screen_width, self.screen_height = pyautogui.size()
        # Set the window dimensions to match the screen size
        self.window.geometry(f"{self.screen_width}x{self.screen_height}")

        # Hide the title bar and maximize the window to full screen
        self.window.attributes("-fullscreen", True)

        # Create a blank canvas with a white background that fills the window
        self.canvas = tk.Canvas(self.window, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Write the text "ABCD EFG" at the center of the canvas
        text = self.canvas.create_text(self.screen_width/2, self.screen_height/2, text="Keep your gaze fixed on the red circle.\nIt initially appears on the top left corner of your screen and follow its movements.", font=("Arial", 18))
        # Update the canvas to show the text
        self.canvas.update()
        # Pause for 5 seconds
        time.sleep(5)
        # Remove the text from the canvas
        self.canvas.delete(text)
        # Update the canvas to reflect the removal of the text
        self.canvas.update()

        # Create a placeholder for the photo
        self.photo = None
        # Get the start time
        self.start_time = time.time()

        # Initalize self.eye_points to empty list. Our calibration function will populate it.
        self.eye_points = []

        # Create Calibration Matrices.
        self.initializeCalibration()
        
        # Run on realTime eyes.
        self.startProcess()

        # Start the Tkinter event loop
        self.window.mainloop()
    
    def initializeCalibration(self):
        
        self.screen_points = get_screen_grid_points()
       
        # Draw circles at each point with a delay of 0.1 seconds
        for index , point in enumerate(self.screen_points):
            x, y = point
            
            # Check if the point is in the corner
            if (x == 0 and y == 0) or (x == self.screen_width and y == 0) or (x == 0 and y == self.screen_height) or (x == self.screen_width and y == self.screen_height):
                radius = 30
            else:
                radius = 20
            
            # Calculate the coordinates for the circle
            x0 = x - radius
            y0 = y - radius
            x1 = x + radius
            y1 = y + radius
            
            # Draw a red circle at the current point
            circle = self.canvas.create_oval(x0, y0, x1, y1, fill="red")
            
            # Update the canvas to show the circle
            self.canvas.update()
            
            # Pause for 1 seconds
            time.sleep(2)
            # Instead of sleeping, Call capture_video(). It will process itself for 20 seconds. then reutn.
            # In that time it will get the average postion of iris.
            # Open the video source
            self.eye_points.append(
                self.capture_video()
            )
            
            self.canvas.itemconfig(circle, fill="white")
            self.canvas.update()
        return

    def capture_video(self):
        # [(left eye iris x, y), (right eye iris x, y)]
        self.vid = cv2.VideoCapture(self.video_source)
        pts = get_iris(self.vid, 100)
        self.vid.release()
        # Consider only left eye cordinates since both eyes move simultaneously.
        return pts[0]
       
            
    def startProcess(self):

        # Pause for 2 seconds
        # time.sleep(2)

        self.vid = cv2.VideoCapture(self.video_source)
        
        # Add a small delay after opening the camera (optional, you can adjust the value as needed)
        # cv2.waitKey(1000)

        mp_face_mesh = mp.solutions.face_mesh
        with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
        
            # Check if the camera is opened successfully
            if not self.vid.isOpened():
                raise Exception("Failed to read frame")
            
            
            LEFT_IRIS = [474,475, 476, 477]
            RIGHT_IRIS = [469, 470, 471, 472]

            while True:
            
                ret, frame = self.vid.read()
                if not ret:
                    print("Failed to read frame")
                    break

                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_h, img_w, _ = frame.shape

                results = face_mesh.process(rgb_frame)

                if not results.multi_face_landmarks:
                    continue                

                landmarks = results.multi_face_landmarks[0].landmark
                # Output: [(23,43), (13,34), ...]
                mesh_points = [(int(p.x * img_w), int(p.y * img_h)) for p in landmarks] 
                # Output: [[23,43], [13,34], ...], need it in this format for valid list of integer indices to slice.
                mesh_points = np.array(mesh_points) 

                (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                center_left = np.array([l_cx, l_cy], dtype=np.int32)
                center_right = np.array([r_cx, r_cy], dtype=np.int32)

                mouse_pt = calibrate_point(center_left, self.eye_points, self.screen_points)
                
                # print(mouse_pt)

                
                # utils.move_mouse_to_point(mouse_pt)



        self.vid.release()

    def splitEyeProcess(self, source):

        cap = cv2.VideoCapture(source)

        if(not cap.isOpened()):
            print("Could't open camera.")
            return
        
        mp_face_mesh = mp.solutions.face_mesh
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Frame not Available")
                    raise Exception("Frame not Available")
                    break
                
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_h, img_w, _ = frame.shape

                results = face_mesh.process(rgb_frame)

                if not results.multi_face_landmarks:
                    continue

                    
                landmarks = results.multi_face_landmarks[0].landmark
                # Output: [(23,43), (13,34), ...]
                mesh_points = [(int(p.x * img_w), int(p.y * img_h)) for p in landmarks] 
                # Output: [[23,43], [13,34], ...], need it in this format for valid list of integer indices to slice.
                mesh_points = np.array(mesh_points) 

                (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                center_left = np.array([l_cx, l_cy], dtype=np.int32)
                center_right = np.array([r_cx, r_cy], dtype=np.int32)

                cv2.circle(frame, center_left, 1, (0,255,0), -1, cv2.LINE_AA)
                cv2.circle(frame, center_right, 2, (0,255,0), -1, cv2.LINE_AA)

                cv2.polylines(frame, [mesh_points[RIGHT_EYE]], isClosed=True, color=(0, 0, 255), thickness=1)
                x, y, width, height = cv2.boundingRect(mesh_points[RIGHT_EYE])

                cv2.rectangle(frame, (x, y), (x + width, y + height), (200, 21, 36), 2)

                if utils.point_inside_rectangle(center_right[0], center_right[1], x, y, width, height):
                    relative_x, relative_y = utils.relative_position(center_right[0], center_right[1], x, y)
                    
                    roi = frame[y:y+height, x:x+width]
                    cells = utils.split_rectangle_into_grid(roi, x, y, width, height)

                    for row in cells:
                        for cell in row:

                            cell_x = cell[0]
                            cell_y = cell[1]
                            cell_width = cell[2]
                            cell_height = cell[3]
                            cell_label = cell[4]

                            if cell_x <= center_right[0] < cell_x + cell_width and cell_y <= center_right[1] < cell_y + cell_height:
                                cv2.rectangle(frame, (cell_x, cell_y), (cell_x + cell_width, cell_y + cell_height), (0, 0, 255), 1)
                                print(cell_label)

                                my_dict = {
                                    "top-left" : np.array([-1, -1]),
                                    "top" : np.array([0, -1]), 
                                    "top-right": np.array([1, -1]),
                                    "middle-left": np.array([-1, 0]), 
                                    "middle": np.array([0, 0]), 
                                    "middle-right" : np.array([1, 0]),
                                    "bottom-left": np.array([-1, 1]), 
                                    "bottom": np.array([0, 1]), 
                                    "bottom-right": np.array([1, 1])
                                }
                                my_dict[cell_label] *= 10
                                # utils.move_mouse_to_point(my_dict[cell_label])
                else:
                    print("The point is outside the rectangle.")

                # cv2.imshow('Mask', mask)     
                cv2.imshow('img', frame)
                key = cv2.waitKey(1)
                if key ==ord('q'):
                    break
        
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    cam_index = show_camera_selection_GUI()
    print("Selected Camera:", cam_index)

    if cam_index is not None:
        # app = VideoCaptureApp("http://192.168.0.102:4747/video?640x480", 20)
        app = VideoCaptureApp(cam_index, 20)
    cv2.destroyAllWindows()
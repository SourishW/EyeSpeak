import cv2, sys
import numpy as np
import mediapipe as mp 
mp_face_mesh = mp.solutions.face_mesh

LEFT_IRIS = [474,475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]



def get_iris(cap, iterations):

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:
        
        left_list = []
        right_list = []

        count = 0

        # Check if the camera is opened successfully
        if not cap.isOpened():
            raise Exception("Failed to read frame")
        
        while count <= iterations:
            
            ret, frame = cap.read()
            if not ret:
                return None
                raise Exception("Failed to read frame")

            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_h, img_w, _ = frame.shape

            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:

                landmarks = results.multi_face_landmarks[0].landmark
                # Output: [(23,43), (13,34), ...]
                mesh_points = [(int(p.x * img_w), int(p.y * img_h)) for p in landmarks] 
                # Output: [[23,43], [13,34], ...], need it in this format for valid list of integer indices to slice.
                mesh_points = np.array(mesh_points) 

                (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                center_left = np.array([l_cx, l_cy], dtype=np.int32)
                center_right = np.array([r_cx, r_cy], dtype=np.int32)

                left_list.append(center_left)
                right_list.append(center_right)
                count += 1
        
        # Calculate the average of x and y cords
        avg_x_left = sum(point[0] for point in left_list) / len(left_list)
        avg_y_left = sum(point[1] for point in left_list) / len(left_list)

        avg_x_right = sum(point[0] for point in right_list) / len(right_list)
        avg_y_right = sum(point[1] for point in right_list) / len(right_list)


        # Create the average point as a list [avg_x, avg_y]
        return [[int(avg_x_left), int(avg_y_left)], [int(avg_x_right), int(avg_y_right)]]
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

eye_cascade = cv2.CascadeClassifier('./cv2classifiers/haarcascade_eye.xml')

class EyeTracker:
    def __init__(self):
        self.ml_training_tuples = list()
    
    def __grab_largest_eyes_coordinates_from_frame(self, frame):
        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(grey_frame)
        if len(eyes) == 0:
            return None
        max_size_eye = max(eyes, key=lambda x:x[2]*x[3])
        return max_size_eye
    
    def __draw_eye_on_frame(self, frame, eye):
        (ex, ey, ew, eh) = eye
        cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    
    def __crop_frame_to_eye_roi(self, frame, eye):
        eye_x, eye_y, eye_width, eye_height = eye
        return frame[eye_y:eye_y+eye_height, eye_x:eye_x+eye_width]
    
    def __prepare_eye_roi_for_machine_learning(self, eye_roi, width =224, height=224):
        resized_frame = cv2.resize(eye_roi, (width, height))
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        set_values_between_0_1 = rgb_frame / 255.0
        return set_values_between_0_1

    def __process_and_crop(self, frame):
        largest_eye = self.__grab_largest_eyes_coordinates_from_frame(frame)
        if largest_eye is None:
            return
        
        self.__draw_eye_on_frame(frame, largest_eye)
        eye_roi = self.__crop_frame_to_eye_roi(frame, largest_eye)
        ml_ready = self.__prepare_eye_roi_for_machine_learning(eye_roi)
        return ml_ready

    def add_frame_to_train_on(self, frame, coordinates):
        ml_ready = self.__process_and_crop(frame)
        if ml_ready is not None:
            self.ml_training_tuples.append((ml_ready, coordinates))

    def train_model(self):
        frames, labels = zip(*self.ml_training_tuples)
        frames = np.array(frames)
        labels = np.array(labels)

        frames = frames.reshape(len(frames), -1)
        X_train, X_test, y_train, y_test = train_test_split(frames, labels, test_size=0.2, random_state=42)
        print(X_train.shape)

        print("hi")
        model = MLPRegressor(hidden_layer_sizes=(128, 64), max_iter=50, verbose=1)
        print("training")
        model.fit(X_train, y_train)
        print("fini training")

        mse = np.mean((model.predict(X_test) - y_test) ** 2)
        print(f"Mean Squared Error Of Trained Model: {mse}")
        self.model = model

    def track_eye_gaze(self, new_frame):
        processed_frame = self.__process_and_crop(new_frame)
        if processed_frame is None:
            return None
        return tuple(self.model.predict([processed_frame]))



        
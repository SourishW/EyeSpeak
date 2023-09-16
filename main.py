import cv2
import numpy as np

# cap = cv2.VideoCapture("./images/eye_calibration_video.mp4")
cap = cv2.VideoCapture(0)
eye_cascade = cv2.CascadeClassifier('./cv2classifiers/haarcascade_eye.xml')

def grab_largest_eyes_coordinates_from_frame(frame):
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(grey_frame)
    if len(eyes) == 0:
        return None
    max_size_eye = max(eyes, key=lambda x:x[2]*x[3])
    return max_size_eye

def draw_eye_on_frame(frame, eye):
    (ex, ey, ew, eh) = eye
    cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

def crop_frame_to_eye_roi(frame, eye):
    eye_x, eye_y, eye_width, eye_height = eye
    return frame[eye_y:eye_y+eye_height, eye_x:eye_x+eye_width]

def prepare_eye_roi_for_machine_learning(eye_roi, width =224, height=224):
    resized_frame = cv2.resize(eye_roi, (width, height))
    set_values_between_0_1 = resized_frame / 255.0
    rgb_frame = cv2.cvtColor(set_values_between_0_1, cv2.COLOR_BGR2RGB)
    return rgb_frame


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    max_size_eye = grab_largest_eyes_coordinates_from_frame(frame)
    if max_size_eye is None:
        continue
    draw_eye_on_frame(frame, max_size_eye)
    cropped_eye_roi = crop_frame_to_eye_roi(frame, max_size_eye)

    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, pupil_threshold = cv2.threshold(grey_frame, 20, 255, cv2.THRESH_BINARY_INV)
    _, white_partthreshold = cv2.threshold(grey_frame, 100, 255, cv2.THRESH_BINARY)
    combined_image = cv2.bitwise_or(pupil_threshold, white_partthreshold)
    
    cv2.imshow("frame",frame)
    cv2.imshow("threshold", pupil_threshold)
    cv2.imshow("cropped_eye_roi", cropped_eye_roi)
    # cv2.imshow("white_threshold", white_partthreshold)
    # cv2.imshow("both", combined_image)

    eyes = eye_cascade.detectMultiScale(frame)
    
    key = cv2.waitKey(30)
    if key == ord('q'):
        break

cv2.destroyAllWindows()

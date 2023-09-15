import cv2

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
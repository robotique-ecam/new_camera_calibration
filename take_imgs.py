import cv2
from datetime import datetime

cam = cv2.VideoCapture(2)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

cv2.namedWindow("calibration_window")

img_counter = 0
now = datetime.now()

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif (datetime.now() - now).total_seconds() > 2:
        # takes pictures every 2 second
        img_name = "calibration_imgs/fisheye_model_pictures_set/calibration_image_{}.jpg".format(
            img_counter
        )
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        now = datetime.now()
    resized = cv2.resize(frame.copy(), (1421, 800), interpolation=cv2.INTER_AREA)
    cv2.imshow("calibration_window", resized)

cam.release()

cv2.destroyAllWindows()

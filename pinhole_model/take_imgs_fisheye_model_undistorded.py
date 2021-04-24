import cv2
import numpy as np
import os
from datetime import datetime

def get_repo_directory():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

cam = cv2.VideoCapture(2)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

cv2.namedWindow("calibration_window")

img_counter = 0
now = datetime.now()

# You should replace these 3 lines with the output in calibration step
DIM = (3840, 2160)
K = np.array(
    [
        [1426.4349637104904, 0.0, 1919.8425216336193],
        [0.0, 1423.1510790046468, 1094.9067233281635],
        [0.0, 0.0, 1.0],
    ]
)
D = np.array(
    [
        [-0.036070207475902644],
        [-0.002003213487781793],
        [-0.0007185511458800288],
        [-0.0004833997296696256],
    ]
)


def undistort(img, balance=0.0, dim2=None, dim3=None):
    dim1 = img.shape[:2][::-1]  # dim1 is the dimension of input image to un-distort

    assert (
        dim1[0] / dim1[1] == DIM[0] / DIM[1]
    ), "Image to undistort needs to have same aspect ratio as the ones used in calibration"

    if not dim2:
        dim2 = dim1

    if not dim3:
        dim3 = dim1

    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0

    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(
        scaled_K, D, dim2, np.eye(3), balance=balance
    )
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(
        scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2
    )
    undistorted_img = cv2.remap(
        img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT
    )
    return undistorted_img


while True:
    ret, img = cam.read()
    frame = undistort(img, balance=0.3)
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
        img_name = get_repo_directory() + "/calibration_imgs/pinhole_model_from_fisheye_undistrorded_pictures_set/calibration_image_{}.jpg".format(
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

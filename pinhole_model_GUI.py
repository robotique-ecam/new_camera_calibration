import cv2
import numpy as np
import math
from vcam import vcam, meshGen


def undistort(img, camera_matrix, distortion_coefficients):
    """ Using a given calibration matrix, display the distorted, undistorted, and cropped frame"""
    distorted_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    scaled_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
        camera_matrix, distortion_coefficients, (3840, 2160), 1, (3840, 2160)
    )
    roi_x, roi_y, roi_w, roi_h = roi

    undistorted_frame = cv2.undistort(
        distorted_frame,
        camera_matrix,
        distortion_coefficients,
        None,
        scaled_camera_matrix,
    )

    cropped_frame = undistorted_frame[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]
    if cropped == 0:
        return undistorted_frame
    else:
        return cropped_frame


def update_img(x):
    global cropped
    D[0][0] = float(cv2.getTrackbarPos("K1", WINDOW_NAME)) * 2 / 100000 - 1
    D[1][0] = float(cv2.getTrackbarPos("K2", WINDOW_NAME)) * 2 / 100000 - 1
    D[2][0] = float(cv2.getTrackbarPos("P1", WINDOW_NAME)) * 2 / 100000 - 1
    D[3][0] = float(cv2.getTrackbarPos("P2", WINDOW_NAME)) * 2 / 100000 - 1
    D[4][0] = float(cv2.getTrackbarPos("K3", WINDOW_NAME)) * 2 / 100000 - 1
    K[0][0] = cv2.getTrackbarPos("mtx1", WINDOW_NAME)
    K[1][1] = cv2.getTrackbarPos("mtx2", WINDOW_NAME)
    cropped = cv2.getTrackbarPos("cropped", WINDOW_NAME)

    undistorted_frame = undistort(img, K, D)
    print("\n\n############## Camera Matrix ##################")
    print(K)
    print("\n############## Distortion Coefficients ##################")
    print(D)
    cv2.imshow("output", undistorted_frame)


K = np.array(
    [
        [3.96852066e03, 0.0, 1.93101581e03],
        [0.0, 3.86244387e03, 1.08377085e03],
        [0.0, 0.0, 1.0],
    ]
)
D = np.array(
    [
        [-9.18833987e-01],
        [3.25444608e-01],
        [-4.78048443e-03],
        [-6.78371276e-04],
        [2.55123013e-01],
    ]
)

cropped = 0

WINDOW_NAME = "output"
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW_NAME, 700, 700)

# Creating the tracker bar for all the features
cv2.createTrackbar("mtx1", WINDOW_NAME, int(K[0][0]), 10000, update_img)
cv2.createTrackbar("mtx2", WINDOW_NAME, int(K[1][1]), 10000, update_img)
cv2.createTrackbar(
    "K1", WINDOW_NAME, int((D[0][0] + 1) * (100000 / 2)), 100000, update_img
)
cv2.createTrackbar(
    "K2", WINDOW_NAME, int((D[1][0] + 1) * (100000 / 2)), 100000, update_img
)
cv2.createTrackbar(
    "P1", WINDOW_NAME, int((D[2][0] + 1) * (100000 / 2)), 100000, update_img
)
cv2.createTrackbar(
    "P2", WINDOW_NAME, int((D[3][0] + 1) * (100000 / 2)), 100000, update_img
)
cv2.createTrackbar(
    "K3", WINDOW_NAME, int((D[4][0] + 1) * (100000 / 2)), 100000, update_img
)
cv2.createTrackbar("cropped", WINDOW_NAME, 0, 1, update_img)

img = cv2.imread("./undistorded_results/board_overview.jpg")

update_img(1)

while True:
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

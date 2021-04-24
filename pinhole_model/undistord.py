import numpy as np
import cv2
import os

def get_repo_directory():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Define Camera Matrix
camera_matrix = np.array(
    [
        [8.51158290e02, 0.0, 1.89003916e03],
        [0.0, 8.47796721e02, 1.17912096e03],
        [0.0, 0.0, 1.0],
    ]
)

# Define distortion coefficients
distortion_coefficients = np.array(
    [-0.00131221, -0.00089388, 0.00234124, 0.00322031, 0.00010104]
)

frame = cv2.imread(
    get_repo_directory() + "/undistorded_results/200_pictures_fisheye/board_overview_undistord_balance_0_3.jpg"
)

distorted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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

cv2.imwrite(
    get_repo_directory() + "/undistorded_results/pinhole_correction_over_fisheye_model/board_overview_undistord.jpg",
    undistorted_frame,
)
cv2.imwrite(
    get_repo_directory() + "/undistorded_results/pinhole_correction_over_fisheye_model/board_overview_undistord_cropped.jpg",
    cropped_frame,
)

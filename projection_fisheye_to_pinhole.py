import cv2
import numpy as np
import os
from cv2 import aruco
from datetime import datetime

ratio = 2.702322308

DIM=(3840,2160)
K=np.array([[1426.4349637104904, 0.0, 1919.8425216336193], [0.0, 1423.1510790046468, 1094.9067233281635], [0.0, 0.0, 1.0]])
D=np.array([[-0.036070207475902644], [-0.002003213487781793], [-0.0007185511458800288], [-0.0004833997296696256]])
new_K = [[8.59993203e+02, 0.00000000e+00, 1.87111502e+03],
 [0.00000000e+00, 8.58013359e+02, 1.16514527e+03],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]

def convert_point(pt):
    new_x = pt[0] * new_K[0][0] + new_K[0][2]
    new_y = pt[1] * new_K[1][1] + new_K[1][2]
    return (int(new_x), int(new_y))

def draw_line(pts):
    pt1 = convert_point(pts[0])
    pt2 = convert_point(pts[1])

    cv2.line(img, pt1, pt2, (158,108,253), 5)

def undis_and_draw(marker):
    points_2d = np.asarray(marker)

    points_2d = points_2d[:, 0:2].astype('float32')
    points2d_undist = np.empty_like(points_2d)
    points_2d = np.expand_dims(points_2d, axis=1)

    result = cv2.fisheye.undistortPoints(points_2d, K, D)

    draw_line([result[0][0], result[1][0]])
    draw_line([result[1][0], result[2][0]])
    draw_line([result[2][0], result[3][0]])
    draw_line([result[3][0], result[0][0]])


original = cv2.imread("./undistorded_results/board_overview.jpg")
img = cv2.imread("./undistorded_results/200_pictures_fisheye/board_overview_undistord_balance_0_3.jpg")

gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
parameters =  aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
original = aruco.drawDetectedMarkers(original.copy(), corners, ids)
for i in range(len(corners)):
    undis_and_draw(corners[i][0])
resized_origin = cv2.resize(original.copy(), (1421, 800), interpolation = cv2.INTER_AREA)
resized = cv2.resize(img.copy(), (1421, 800), interpolation = cv2.INTER_AREA)

#print((x1,y1), (x2,y2))
while True:
    cv2.imshow("original", resized_origin)
    cv2.imshow("rectangle", resized)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

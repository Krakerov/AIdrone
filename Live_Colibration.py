
import cv2
import numpy as np
import time
import Camers_show
# Определение размеров шахматной доски
CHECKERBOARD = (6,9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objpoints = []
imgpoints = []

# Определение мировых координат для 3D точек
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

Rvecs_list = []
Tvecs_list = []

cap = cv2.VideoCapture(0)
images = []
np_img = []
while True:
    objpoints = []

    imgpoints = [] 
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    if ret == True:
        objpoints.append(objp)
        # уточнение координат пикселей для заданных 2d точек.
        corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
        
        imgpoints.append(corners2)
        # Нарисовать и отобразить углы
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        img2 = cv2.drawChessboardCorners(img, CHECKERBOARD, corners, ret)
    
    h,w = img.shape[:2]
    if len(objpoints)>0 and len(imgpoints)>0:
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        
        #time.sleep(0.5)
        rvers_norm = (rvecs[0][0][0]**2+rvecs[0][0][0]**2 + rvecs[0][0][0]**2)**0.5
        Rvecs_list.append([int(rvecs[0][0][0]*100/rvers_norm),int(rvecs[0][1][0]*100/rvers_norm),int(rvecs[0][2][0]*100/rvers_norm)])
        Tvecs_list.append([int(tvecs[0][0][0]),int(tvecs[0][1][0]),int(tvecs[0][2][0])])
        if len(Rvecs_list)>20:
            Rvecs_list = Rvecs_list[1:]
        if len(Tvecs_list)>20:
            Tvecs_list = Tvecs_list[1:]
        #print(Rvecs_list, Tvecs_list)
        print('Начало')
        print("Camera matrix : \n")
        print(mtx)
        print("dist : \n")
        print(dist)
        print("Вращение : \n")
        print(rvecs)
        print(int(rvecs[0][2][0]))
        print("Расположение : \n")
        print(tvecs)

        print('Усредненное вращение: ')
        True_cameras_massiv = [
            [[int(tvecs[0][0][0]),int(tvecs[0][1][0]),int(tvecs[0][2][0])],[int(rvecs[0][0][0]),int(rvecs[0][1][0]),int(rvecs[0][2][0])]]
            ]
        srednee_tvers = [int(np.average(Tvecs_list, axis=0)[0]),int(np.average(Tvecs_list, axis=0)[1]),int(np.average(Tvecs_list, axis=0)[2])]
        srednee_rvers = [int(np.average(Rvecs_list, axis=0)[0]),int(np.average(Rvecs_list, axis=0)[1]),int(np.average(Rvecs_list, axis=0)[2])]
        cameras_massiv = [
            [srednee_tvers, srednee_rvers]
            ]
        Camers_show.Show_cams(cameras_massiv)
    cv2.imshow('Subpoints', img)
    #cv2.imshow('orig', img2)
    
    #Camers_show.Show_cams()
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
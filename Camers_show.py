import cv2
import numpy

img = numpy.zeros((400, 400, 3), dtype = "uint8") 
img2 = numpy.zeros((400, 100, 3), dtype = "uint8") 
def Show_cams(cameras_massiv):
    img[:] = (0,255,255)
    img2[:] = (0,255,255)
    K_dot = 10
    K_angle = 1
    Cam_dot = cameras_massiv[0][0]
    Cam_angl = cameras_massiv[0][1]
    print(Cam_dot,Cam_angl)
    cv2.circle(img, (Cam_dot[0] * K_dot+200, Cam_dot[1]*K_dot+200), 10, (255, 0, 0), 3)
    cv2.line(img, (Cam_dot[0]* K_dot+200, Cam_dot[1]*K_dot+200), (Cam_dot[0]*K_dot+200 + Cam_angl[0]*K_angle, Cam_dot[1]*K_dot+200 + Cam_angl[1]*K_angle), (0, 0, 255), 5)
    

    cv2.circle(img2, (50, 400 - Cam_dot[2]), 10, (255, 0, 0), 3)
    cv2.line(img2, (50, 400 - Cam_dot[2]  ), (50 + Cam_angl[0]*K_angle, 400 - Cam_dot[2] - Cam_angl[2]*K_angle), (0, 0, 255), 5)
    cv2.imshow('heyght', img2)
    cv2.imshow('Camers', img) 
    k = cv2.waitKey(30) & 0xFF
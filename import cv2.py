import cv2
import numpy
import SampleApp
import random
from time import sleep

def nothing(x):
	pass
cv2.namedWindow("Track")
cv2.createTrackbar('T1',"Track", 0, 255, nothing)
cv2.createTrackbar('T2',"Track", 0, 255, nothing)
treck_img = numpy.zeros((30,700,3), numpy.uint8)
class Point:
     def __init__(self,x,y):
          self.x = x
          self.y = y
def sorting(kek):
      return kek[2]
def MasPlus(array1, array2):
     array = []
     for i in range(len(array1)):
          array.append(array1[i]+array2[i])
     return array
def MasMinus(array1, array2):
     array = []
     for i in range(len(array1)):
          array.append(array1[i]-array2[i])
     return array
def ccw(A,B,C):  # две функции для проверки на пересекаемость отрезков
    return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)
def intersect(A,B,C,D):
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
def push_vect(vect_massiv, vect, maks_count = 10):
    vect = numpy.reshape(vect, (1,3))
    vect_massiv = numpy.append(vect_massiv, vect, axis = 0)
    if len(vect_massiv)>maks_count:
        vect_massiv = vect_massiv[1:]
    return(vect_massiv)
def SredneVector(vect_massiv):
    return(numpy.average(vect_massiv, axis=0))
     
cap = cv2.VideoCapture(1)
print("cap: ")
print (cap)
cap.set(cv2.CAP_PROP_FPS, 30)

Cord_massiv = numpy.array([
                (-36, -36, 0)
            ],
            dtype=numpy.double)



while True:
    minim = cv2.getTrackbarPos('T1','Track')
    maxi = cv2.getTrackbarPos('T2','Track')
    
    ret, frame = cap.read()
    cv2.imshow('Track', treck_img)


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray_frame = cv2.fastNlMeansDenoising(gray_frame, None, 10, 10, 7, 15) 
    gray_frame = cv2.bilateralFilter(gray_frame,9,75,75)
    if maxi>20:
        gray = cv2.inRange(gray_frame, minim, maxi)
    else: gray = cv2.inRange(gray_frame, 150, 255)

    size = frame.shape
    height, width = frame.shape[0:2]
    conturs, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    list_dots = []
    for i in conturs:
         moments = cv2.moments(i)
         #moments = sorted(moments, key = ['m00'])
         if moments["m00"]>10 and len(moments) >=3:
            cx = int(moments["m10"] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
            cv2.drawContours(frame, i, -1, (0,255,0), 2)
            #cv2.line(frame, (cx, 0), (cx, height), (0, 255, 0), 2)
            #cv2.line(frame, (0, cy), (width, cy), (0, 255, 0), 2)
            #list_dots.append([cx,cy,moments["m00"]])
            list_dots.append([cx,cy])
    if len(list_dots)>=4:
        list_dots = list_dots[0:4]
        #print(list_dots)
        #print(" ")
        pts = numpy.array(list_dots, numpy.int32)
        pts = pts.reshape((-1,1,2))
        
        # Усли диагонали квадрата не пересекаются  => порядок точек неверен, надо поменять
        if not intersect(Point(list_dots[0][0],list_dots[0][1]), Point(list_dots[2][0],list_dots[2][1]), Point(list_dots[1][0],list_dots[1][1]),Point(list_dots[3][0],list_dots[3][1])):
            Prom_dot = list_dots[0]  
            list_dots[0] = list_dots[1]
            list_dots[1] = Prom_dot

        cv2.polylines(frame,[pts],True,(0,255,255))

        vec1 = MasMinus(list_dots[0], list_dots[1])
        vec1 = (vec1[0]**2 + vec1[1]**2)**0.5
        vec2 = MasMinus(list_dots[2], list_dots[1])
        vec2 = (vec2[0]**2 + vec2[1]**2)**0.5
        vec3 = MasMinus(list_dots[0], list_dots[2])
        vec3 = (vec3[0]**2 + vec3[1]**2)**0.5
        maxvec = max(vec2, vec1, vec3)
        
        if maxvec == vec1:  # рассматриваем только 3 точки чтобы найти дагональ
            center = (MasPlus(list_dots[0], list_dots[1]))
        elif maxvec == vec2:
            center = (MasPlus(list_dots[2], list_dots[1]))
        else:
            center = (MasPlus(list_dots[0], list_dots[2]))
        center[0] = int(center[0]/2)
        center[1] = int(center[1]/2)
        #print(center)
        cv2.line(frame, (center[0], 0), (center[0], height), (0, 255, 0), 2)  # Перекрестие через центр
        cv2.line(frame, (0, center[1]), (width, center[1]), (0, 255, 0), 2)
    
        points_3D = numpy.array(
            [
                (-36, -36, 0),
                (-36, 36, 0),
                (36, 36, 0),
                (36, -36, 0)
            ],
            dtype=numpy.double
        )

       
        matrix_camera = numpy.array(
            [(710.44632329, 0.00000000, 320.0),
            (0.00000000, 707.18061381, 240.0),
            (0.00000000, 0.00000000, 1.00000000)],
            dtype=numpy.double
        )
        dist = numpy.array((-0.26807578, 0.12441642, -0.03627257, 0.04421583, -0.02867549), dtype=numpy.double)
        list_dots = numpy.array(list_dots, dtype=numpy.double)

        success, vector_rotation, vector_translation = cv2.solvePnP(points_3D, list_dots, matrix_camera, dist) # numpy.zeros((3,1)), numpy.zeros((3,1)), cv2.SOLVEPNP_IPPE_SQUARE)
        if success:
            # print(numpy.round(vector_translation, 5))
            # print(vector_translation.view(float).reshape(vector_translation.shape + (-1,))[0][0][0])

            
            normalvectorCord = [int(vector_translation[0].tolist()[0]),int( vector_translation[1].tolist()[0]),int(vector_translation[2].tolist()[0])]
            normalvectorRot = [int(vector_rotation[0].tolist()[0]), int(vector_rotation[1].tolist()[0]),int(vector_rotation[2].tolist()[0])]
            
            
            
            axis = numpy.array([[0,0,0], [1,0,0], [0,1,0], [0,0,1]], dtype = 'float32').reshape((4,1,3))
        #     axis = numpy.array(
        #     [
        #         (0, 0, 0),
        #         (1, 0, 0),
        #         (0, 1, 0),
        #         (0, 0, 1)
        #     ],
        #     dtype=numpy.double
        # )

            axis_points, jac = cv2.projectPoints(axis, vector_rotation, vector_translation, matrix_camera, dist)
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0,0,0)]
            
            #check axes points are projected to camera view.
            if len(axis_points) > 0:
                axis_points = axis_points.reshape((4,2))

                origin = (int(axis_points[0][0]),int(axis_points[0][1]) )
                #print (center, origin)
                #print(numpy.linalg.norm(center - numpy.array(origin)))
                if numpy.linalg.norm(center - numpy.array(origin))< 10:  # Проверка координат на вменяемость
                    #print(normalvectorCord, normalvectorRot)

                    Cord_massiv = push_vect(Cord_massiv, normalvectorCord)
                    StabvectorCord = SredneVector(Cord_massiv)
                    StabvectorCord = [int(StabvectorCord[0]), int(StabvectorCord[1]),int(StabvectorCord[2])]


                    # SampleApp.SetPosition(StabvectorCord, [0,0,0])  # отправляем коардинаты в Юнити



                    #sleep(0.5)
                    #SampleApp.SetPosition(normalvectorCord, normalvectorRot)
                    # for p, c in zip(axis_points[1:], colors[:3]):
                    #     p = (int(p[0]), int(p[1]))


                    #     if origin[0] > 5*frame.shape[1] or origin[1] > 5*frame.shape[1]:break
                    #     if p[0] > 5*frame.shape[1] or p[1] > 5*frame.shape[1]:break


                    #     cv2.line(frame.astype(int), origin, p, c, 5)

            
    hsv_gray_frame = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
    sv_gray_frame = cv2.bilateralFilter(gray_frame,9,75,75)

    cv2.imshow('orig', frame)
    cv2.imshow('gray', gray)
    #cv2.imshow('hsv', hsv)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
cap.release()

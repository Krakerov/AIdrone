import cv2
import numpy

def nothing(x):
	pass
cv2.namedWindow("Track")
cv2.createTrackbar('T1',"Track", 0, 255, nothing)
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
cap = cv2.VideoCapture(0)
print("cap: ")
print (cap)
cap.set(cv2.CAP_PROP_FPS, 30)

cv2.createTrackbar('T2',"Track", 0, 255, nothing)

while True:
    minim = cv2.getTrackbarPos('T1','Track')
    maxi = cv2.getTrackbarPos('T2','Track')
    ret, frame = cap.read()
    print(ret)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.bilateralFilter(gray_frame,9,75,75)
    if maxi>20:
        gray = cv2.inRange(gray_frame, minim, maxi)
    else: gray = cv2.inRange(gray_frame, 243, 255)

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
    if len(list_dots)>=3:
        list_dots = list_dots[0:3]
        pts = numpy.array(list_dots, numpy.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(frame,[pts],True,(0,255,255))

        vec1 = MasMinus(list_dots[0], list_dots[1])
        vec1 = (vec1[0]**2 + vec1[1]**2)**0.5
        vec2 = MasMinus(list_dots[2], list_dots[1])
        vec2 = (vec2[0]**2 + vec2[1]**2)**0.5
        vec3 = MasMinus(list_dots[0], list_dots[2])
        vec3 = (vec3[0]**2 + vec3[1]**2)**0.5
        maxvec = max(vec2, vec1, vec3)
        
        if maxvec == vec1:
            center = (MasPlus(list_dots[0], list_dots[1]))
        elif maxvec == vec2:
            center = (MasPlus(list_dots[2], list_dots[1]))
        else:
            center = (MasPlus(list_dots[0], list_dots[2]))
        center[0] = int(center[0]/2)
        center[1] = int(center[1]/2)
        print(center)
        cv2.line(frame, (center[0], 0), (center[0], height), (0, 255, 0), 2)
        cv2.line(frame, (0, center[1]), (width, center[1]), (0, 255, 0), 2)



    hsv_gray_frame = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
    sv_gray_frame = cv2.bilateralFilter(gray_frame,9,75,75)

    cv2.imshow('orig', frame)
    cv2.imshow('gray', gray)
    #cv2.imshow('hsv', hsv)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
cap.release()

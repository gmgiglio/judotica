import numpy as np
import cv2
from robot2 import *


def elegirPunto():
    apretado = False
    x,y = 0,0
    def _mouseEvent(event, _x, _y, flags, param):
            x = _x
            y= _y
            apretado = True

    cv2.setMouseCallback(tituloVentana,_mouseEvent)

    while not apretado:
        global img
        _, img = capture.read()
        cv2.imshow(tituloVentana, img)

    cv2.setMouseCallback(tituloVentana, None)

    return x,y



img = 1
hsv_img = 1

lower= np.array([0,50,50],np.uint8)
upper= np.array([5,255,255],np.uint8)
error = np.array([15,0,0],np.uint8)

tituloVentana = "Original Image"
cv2.namedWindow( tituloVentana,  cv2.CV_WINDOW_AUTOSIZE )


capture = cv2.VideoCapture(0)

if capture.isOpened():
    capture.open(0)      

xprom = 0
yprom = 0
par = 0.9

print elegirPunto()

#  ciclo de captura de imagen
while True:
    global img
    _, img = capture.read()            

    cv2.imshow(tituloVentana, img)





cv2.destroyAllWindows()
 

def centroMasa(self,color):
        global lower
        global upper

        lower = color
        upper = color

        lower = cv2.subtract(lower,error)
        upper = cv2.add(upper,error)

        Title_tracker = "Color Tracker"
        Title_original = "Original Image"


        imgBlur = cv2.blur(self.img,(10,10))

        hsv_img = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)

        thres = cv2.inRange(hsv_img, lower, upper)

        moments = cv2.moments(thres, 0)

        area = moments['m00']

        vector = None
        if(area > 1000):
            x = (np.uint32)(moments['m10']/area)
            y = (np.uint32)(moments['m01']/area)
            vector = [x, y]

        return vector







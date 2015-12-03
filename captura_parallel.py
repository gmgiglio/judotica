import numpy as np
import cv2
from threading import Thread


class Captura(Thread):

    def __init__(self,numCam):
        Thread.__init__(self)
        self.numCam = numCam
        self.abierta = False

    def iniciarCaptura(self):

        self.tituloVentana = "Original Image"

        cv2.namedWindow(self.tituloVentana,  cv2.CV_WINDOW_AUTOSIZE )

        self.capture = cv2.VideoCapture(self.numCam)

        if self.capture.isOpened():
            self.capture.open(0)

        self.abierta = True
        self.start()

    def run(self):
        while self.abierta:
            _, self.img = self.capture.read()



    def pararCaptura(self):
            self.abierta = False


    def centroMasa(self,color):
        lower = color
        upper = color

        lower = cv2.subtract(lower,error)
        upper = cv2.add(upper,error)

        Title_tracker = "Color Tracker"
        Title_original = "Original Image"


        img = cv2.blur(self.img,(10,10))

        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        thres = cv2.inRange(hsv_img, lower, upper)

        moments = cv2.moments(thres, 0)

        area = moments['m00']

        vector = None
        if(area > 1000):
            x = (np.uint32)(moments['m10']/area)
            y = (np.uint32)(moments['m01']/area)
            vector = [x, y]

        return vector


    def posClick(self):

        x,y = 0,0
        def _mouseEvent(self,event, _x, _y, flags, param):

            x = _x
            y= _y

            if event == cv2.EVENT_LBUTTONDOWN:
                self.cierra = True

        cv2.setMouseCallback(self.tituloVentana,_mouseEvent)

        while True:

            cv2.imshow(self.tituloVentana, self.img)




""""

def color_pos(vec):
    global lastImage
    lastImage = cv2.cvtColor(lastImage, cv2.COLOR_BGR2HSV)
    return lastImage [vec[1]][vec[0]]

error = np.array([15,0,0],np.uint8);

def pos_objeto(color):
    global lower
    global upper

    lower = color
    upper = color

    lower = cv2.subtract(lower,error)
    upper = cv2.add(upper,error)

    Title_tracker = "Color Tracker"
    Title_original = "Original Image"

    
    _, img = capture.read()

    img = cv2.blur(img,(10,10))

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

    thres = cv2.inRange(hsv_img, lower, upper)
                
    moments = cv2.moments(thres, 0)
                
    area = moments['m00']

    vector = None
    if(area > 1000):
        x = (np.uint32)(moments['m10']/area)
        y = (np.uint32)(moments['m01']/area)
        vector = [x, y]

    return vector


def centro():
    dimenciones =  capture.read()[1].shape[:2]
    return [dimenciones[0]/2 , dimenciones[1]/2]
"""




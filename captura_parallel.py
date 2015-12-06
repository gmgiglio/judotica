import numpy as np
import cv2
import threading as th
import time


class Captura(th.Thread):

    def __init__(self,numCam):
        th.Thread.__init__(self)
        self.numCam = numCam
        self.abierta = False


    def iniciarCaptura(self):

        self.tituloVentana = "Original Image"

        cv2.namedWindow(self.tituloVentana,  cv2.CV_WINDOW_AUTOSIZE )


        self.capture = cv2.VideoCapture(self.numCam)

        if self.capture.isOpened():
            self.capture.open(self.numCam)

        self.abierta = True

        _, self.img = self.capture.read()
        self.imgLock = th.Lock()

        self.start()

    def run(self):

        while self.abierta:

            _, self.img = self.capture.read()
            cv2.imshow(self.tituloVentana,self.img)






    def pararCaptura(self):
            self.abierta = False


    errorColor = np.array([15,0,0],np.uint8)
    def centroMasa(self,color):
        lower = color
        upper = color

        lower = cv2.subtract(lower,Captura.errorColor)
        upper = cv2.add(upper,Captura.errorColor)


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

        params = [0,0]
        def _mouseEvent(self,event, x, y, flags, param):

            params[(x,y),True]

            if event == cv2.EVENT_LBUTTONDOWN:
                cierra = True


        cv2.setMouseCallback(self.tituloVentana,_mouseEvent)

        while not params[1]:
            continue


cap = Captura(0)
cap.iniciarCaptura()


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




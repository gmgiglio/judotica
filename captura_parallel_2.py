import numpy as np
import cv2
from threading import Thread
import time

class Captura(Thread):

    def __init__(self,numCam):
        Thread.__init__(self)
        self.numCam = numCam
        self.abierta = False
        self.mostrarImagen = False

    def iniciarCaptura(self):

        self.tituloVentana = "Original Image"

        cv2.namedWindow(self.tituloVentana,  cv2.CV_WINDOW_AUTOSIZE )

        self.capture = cv2.VideoCapture(self.numCam)

        if self.capture.isOpened():
            self.capture.open(0)

        self.abierta = True
        _, self.img = self.capture.read()
        self.start()

    def run(self):
        while self.abierta:
            _, self.img = self.capture.read()
            if self.mostrarImagen:
                cv2.imshow(self.tituloVentana,self.img)
                print 'a'


    def pararCaptura(self):
            self.abierta = False



cap = Captura(0)
cap.mostrarImagen = True
cap.iniciarCaptura()

time.sleep(10)
cap.pararCaptura()



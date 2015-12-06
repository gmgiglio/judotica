__author__ = 'gianfrancogiglio'

import numpy as np
import cv2
import tcp_client_robot_1_2015 as tcp
import time

#tcp.iniciar()

class Robot:

    def __init__(self,objGrande,objChico):
        self.objGrande = objGrande
        self.objChico = objChico


    def direccion(self):
        return [int(self.objChico.pos[0]) - int(self.objGrande.pos[0]), int(self.objChico.pos[1]) - int(self.objGrande.pos[1])]


class Jigoro(Robot):

    razonGiro = 0.4 # 22,9183 grados
    razonAvanzar = 1

    def avanzar(self,num):
        for i in range(num):
            tcp.enviarMensaje('s')
            time.sleep(1)
    def retroceder(num):
        for i in range(num):
            tcp.enviarMensaje('w')
            time.sleep(1)

    def girarDerecha(self,angulo):
        n = int(self.razonGiro * angulo)
        for i in range(n):
            tcp.enviarMensaje('d')
            time.sleep(1)

    def girarIzquierda(self,angulo):
        n = int(self.razonGiro * angulo)
        for i in range(n):
            tcp.enviarMensaje('a')
            time.sleep(1)


    def calibrarGiro(self):
        giros = []
        for i in range(5):
            dir = self.direccion()
            angulo1 = np.arctan2(dir[0],dir[1])
            self.girarIzquierda(i)
            dir = self.direccion()
            angulo2 = np.arctan2(dir[0],dir[1])
            giros.append((angulo2 - angulo1)/i)
        for i in range(5):
            dir = self.direccion()
            angulo1 = np.arctan2(dir[0],dir[1])
            self.girarDerecha(i)
            dir = self.direccion()
            angulo2 = np.arctan2(dir[0],dir[1])
            giros.append((angulo2 - angulo1)/i)
        razonGiro = np.mean(giros)


objetos = []

class Objeto:

    def __init__(self,color):
        self.color = color

    def actualizar(self,pos):
        self.pos = pos

def _mouseEvent(event, x, y, flags, param):
    global jigoro
    global hsv_img

    if event == cv2.EVENT_LBUTTONDOWN:

            objetos.append(Objeto(hsv_img[y,x,0]))

            if len(objetos) == 2:
                jigoro = Jigoro(objetos[0],objetos[1])

            elif len(objetos) ==5:
                global enemy
                enemy = Robot(objetos[2],objetos[3])



img = 1
hsv_img = 1

lower= np.array([0,50,50],np.uint8)
upper= np.array([5,255,255],np.uint8)
error = np.array([15,0,0],np.uint8);


Title_original = "Original Image"

cv2.namedWindow( Title_original,  cv2.CV_WINDOW_AUTOSIZE )

cv2.setMouseCallback(Title_original,_mouseEvent)

capture = cv2.VideoCapture(0)

if capture.isOpened():
    capture.open(0)


def ciclo():
    global img
    global hsv_img
    global lower
    global upper

    _, img = capture.read()

    cv2.imshow(Title_original, img)

    img = cv2.blur(img,(10,10))

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for obj in objetos:

        lower[0] = obj.color
        upper[0] = obj.color

        lower = cv2.subtract(lower,error)
        upper = cv2.add(upper,error)


        thres = cv2.inRange(hsv_img, lower, upper)

        moments = cv2.moments(thres, 0)

        area = moments['m00']

        if(area > 1000):

            x = (np.uint32)(moments['m10']/area)
            y = (np.uint32)(moments['m01']/area)

            cv2.circle(img, (x, y), 2, (255, 255, 255), 10)

            obj.actualizar((x,y))

    cv2.imshow(Title_original, img)

    if cv2.waitKey(10) == 27:
        capture.release()
        return True

    global jigoro
    if len(objetos) >= 3:
        print jigoro.direccion()


    if cv2.waitKey(10) == 27:
        capture.release()
        return

while True:
   ciclo()




cv2.destroyAllWindows()

import numpy as np
import cv2
#import tcp_client_robot_1_2015 as tcp
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

    def avanzar(self, num):
        for i in range(num):
            tcp.enviarMensaje('s')
            time.sleep(0.2)
    def retroceder(num):
        for i in range(num):
            tcp.enviarMensaje('w')
            time.sleep(0.2)

    def girarDerecha(self, angulo):
        n = int(self.razonGiro * angulo)
        for i in range(n):
            tcp.enviarMensaje('d')
            time.sleep(0.2)

    def girarIzquierda(self, angulo):
        n = int(self.razonGiro * angulo)
        for i in range(n):
            tcp.enviarMensaje('a')
            time.sleep(0.2)


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

    def girarAPunto(self,punto):
        dirAPunto = [int(punto[0]) - int(self.objGrande.pos[0]), int(punto[1]) - int(self.objGrande.pos[1])]
        dir = self.direccion()
        angAPunto = np.arctan2(dirAPunto[0],dirAPunto[1])
        ang = np.arctan2(dir[0],dir[1])
        if angAPunto > ang:
            self.girarIzquierda(4)
        else:
            self.girarDerecha(4)

        return np.abs(ang - angAPunto)




objetos = []

class Objeto:

    def __init__(self,color):
        self.color = color
        print "color" , color

    def actualizar(self,pos):
        self.pos = pos

def _mouseEvent(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        global jigoro
        print x,y
        obj = Objeto(hsv_img[y,x,0])
        objetos.append(obj)
        obj.actualizar((x,y))

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
Title_parcial = "Parcial"
Title_color = "Color"
cv2.namedWindow( Title_original,  cv2.CV_WINDOW_AUTOSIZE )
cv2.namedWindow(Title_parcial, cv2.CV_WINDOW_AUTOSIZE)
cv2.namedWindow(Title_color)

cv2.setMouseCallback(Title_original,_mouseEvent)

capture = cv2.VideoCapture(0)

if capture.isOpened():
    capture.open(0)

def centro():
    dimenciones =  img.shape[:2]
    return [dimenciones[0]/2 , dimenciones[1]/2]

errorGiro = 3.14
margenLocal = 200

img_aux = 0
while True:
    _, img = capture.read()

    cv2.imshow(Title_original, img)

    img = cv2.blur(img,(10,10))

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for obj in objetos:

        lower[0] = obj.color
        upper[0] = obj.color

        lower = cv2.subtract(lower,error)
        upper = cv2.add(upper,error)

        imgParcial = hsv_img.copy()
        xMin = max(0 , obj.pos[0] - margenLocal)
        xMax = min(img.shape[1], obj.pos[0] + margenLocal)
        yMin = max(0 , obj.pos[1] - margenLocal)
        yMax = min(img.shape[0], obj.pos[1] + margenLocal)

        imgParcial = img.copy()[yMin: yMax, xMin: xMax]

        cv2.imshow(Title_parcial, imgParcial)
        thresGrande = cv2.inRange(hsv_img, lower, upper)
        thresChico = cv2.inRange(imgParcial, lower, upper)

        moments = cv2.moments(thresChico, 0)

        area = moments['m00']

        if(area > 10):

            x = (np.uint32)(moments['m10']/area) + xMin
            y = (np.uint32)(moments['m01']/area) + yMin


            cv2.circle(img, (x, y), 2, (255, 255, 255), 10)

            obj.actualizar((x,y))

            img_aux = cv2.bitwise_and(img,img, mask= thresGrande)

            cv2.imshow(Title_color, img_aux)


    cv2.imshow(Title_original, img)
    cv2.imshow(Title_color, img_aux)


    if len(objetos) >= 2 and errorGiro:
        global jigoro
        errorGiro = jigoro.girarAPunto()


    if cv2.waitKey(10) == 27:
            capture.release()
            break

"""
    if len(objetos) >= 3:
        if error > 0.01:
            #error = jigoro.girarAPunto(centro())
"""



cv2.destroyAllWindows()











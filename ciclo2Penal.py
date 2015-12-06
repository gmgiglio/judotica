import numpy as np
import cv2
import tcp_client_robot_1_2015 as tcp
import time

#instrucciones = {'centro': 'c', 'pelota': 'a', 'item3': 'abcdef'}
#instruc = eval(input('comando: '))


tcp.iniciar()

class Robot:

    def __init__(self,objGrande,objChico):
        self.objGrande = objGrande
        self.objChico = objChico


    def direccion(self):

        return [int(self.objChico.pos[0]) - int(self.objGrande.pos[0]), int(self.objChico.pos[1]) - int(self.objGrande.pos[1])]


class Jigoro(Robot):

    razonGiro = 0.4 # 22,9183 grados
    razonAvanzar = 1

    def __init__(self,objGrande,objChico):
        self.objGrande = objGrande
        self.objChico = objChico
        self.errorGiro = 3.14
        self.modo = 1  #0 quuieto, 1 girando, 2 avanzando

    def avanzar(self, num):
        for i in range(num):
            tcp.enviarMensaje('s')
        time.sleep(2)
    def retroceder(num):
        for i in range(num):
            tcp.enviarMensaje('w')
        time.sleep(2)

    def girarDerecha(self, n):
        for i in range(n):
            tcp.enviarMensaje('d')
        time.sleep(2)

    def girarIzquierda(self, n):
        for i in range(n):
            tcp.enviarMensaje('a')
        time.sleep(2)

    def pos(self):
        return self.objGrande.pos

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
            self.girarIzquierda(1)
        else:
            self.girarDerecha(1)

        return np.abs(ang - angAPunto)

    def irAPunto(self,punto):

        if self.modo == 1:

            if self.errorGiro > 0.08:
                self.errorGiro = self.girarAPunto(punto)
                print 'giro' , self.errorGiro
            else:
                self.modo = 2
                self.errorGiro = 3.14

        elif self.modo == 2:

            if np.abs(self.pos()[0] - punto[0]) > 10 and np.abs(self.pos()[1] - punto[1]) > 10:
                self.avanzar(8)
                print 'avanzar'
                self.modo = 1
            else:
                self.modo = 0
                print'llegamos!'



objetos = []

class Objeto:

    def __init__(self,color):
        self.color = color
        self.colDisplay = (255,255,255)


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
            objetos[0].colDisplay = (0,255,0)
            objetos[1].colDisplay = (0,255,0)

        elif len(objetos) == 3:
            objetos[2].colDisplay = (255,0,0)



        elif len(objetos) ==5:
            global enemy
            enemy = Robot(objetos[2],objetos[3])
            objetos[3].colDisplay = (0,0,255)
            objetos[4].colDisplay = (0,0,255)


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

_, img = capture.read()

dimenciones =  img.shape[:2]
cen =  [dimenciones[1]/2 , dimenciones[0]/2]

margenLocal = 200


img_aux = 0
while True:
    _, img = capture.read()

    imgBlur = cv2.blur(img,(10,10))

    hsv_img = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)

    for obj in objetos:

        lower[0] = obj.color
        upper[0] = obj.color

        lower = cv2.subtract(lower,error)
        upper = cv2.add(upper,error)

        #imgParcial = hsv_img.copy()
        #xMin = max(0 , obj.pos[0] - margenLocal)
        #xMax = min(imgBlur.shape[1], obj.pos[0] + margenLocal)
        #yMin = max(0 , obj.pos[1] - margenLocal)
        #yMax = min(imgBlur.shape[0], obj.pos[1] + margenLocal)

        #imgParcial = imgBlur.copy()[yMin: yMax, xMin: xMax]

        #cv2.imshow(Title_parcial, imgParcial)
        thresGrande = cv2.inRange(hsv_img, lower, upper)
        thresChico = cv2.inRange(hsv_img, lower, upper)

        moments = cv2.moments(thresChico, 0)

        area = moments['m00']

        if(area > 10):

            x = (np.uint32)(moments['m10']/area) #+ xMin
            y = (np.uint32)(moments['m01']/area) #+ yMin


            cv2.circle(img, (x, y), 2, obj.colDisplay, 10)


            obj.actualizar((x,y))

            img_aux = cv2.bitwise_and(imgBlur,imgBlur, mask= thresGrande)

            cv2.imshow(Title_color, img_aux)

    cv2.circle(img, (cen[0],cen[1]), 2, (255,255,255), 10)
    cv2.imshow(Title_original, img)
    cv2.imshow(Title_color, img_aux)

    global jigoro
    global arcoAmigo

    if len(objetos) >= 3:
        jigoro.avanzar(15)
        jigoro.retroceder(5)
        break

    if cv2.waitKey(10) == 27:
            capture.release()
            break





cv2.destroyAllWindows()











import numpy as np
import cv2
import tcp_client_robot_1_2015 as tcp
import time


def subImagen(img, pos, margen):

    xMin = max(0 , pos[0] - margen)
    xMax = min(img.shape[1], pos[0] + margen)
    yMin = max(0 , pos[1] - margen)
    yMax = min(img.shape[0], pos[1] + margen)

    ret =  img[yMin: yMax, xMin: xMax].copy()
    return ret , (xMin,yMin)

objetos = []
esquinasCancha = []
objetosVisibles = []

class Objeto:
    def __init__(self,pos,colorDisplay = (255,255,255)):
        self.colDisplay = colorDisplay
        self.pos = pos

class Movil(Objeto):
    def __init__(self,color,area,colorDisplay = (255,255,255)):
        self.color = color
        self.colDisplay = colorDisplay
        self.area = area


    def actualizar(self,pos):
        self.pos = pos


def _mouseEvent(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(esquinasCancha) < 2:
            global esquinasCancha
            esq = Objeto((x,y),(0,255,255))
            esquinasCancha.append(esq)
            objetos.append(esq)
            objetosVisibles.append(esq)

            if len(esquinasCancha) == 2:
                for esq in esquinasCancha:
                    if esq in esquinasCancha: objetosVisibles.remove(esq)


        else:

            global lower
            global upper

            margen = 5
            col = cv2.mean(hsv_img[y - margen : y + margen, x - margen : x + margen])[0]

            lo = lower.copy()
            up = upper.copy()

            lo[0] = col
            up[0] = col

            lower = cv2.subtract(lower,error)
            upper = cv2.add(upper,error)

            hsv_imgParcial, _ = subImagen(hsv_img , (x,y) , margenLocal)
            thresChico = cv2.inRange(hsv_imgParcial, lower, upper)
            momentsChico = cv2.moments(thresChico, 0)
            areaChica = momentsChico['m00']

            mov = Movil(col, areaChica)
            mov.colDisplay = (0,255,0)
            objetos.append(mov)
            objetosVisibles.append(mov)
            mov.actualizar((x,y))




img = 1
hsv_img = 1

lower= np.array([0,50,50],np.uint8)
upper= np.array([5,255,255],np.uint8)
error = np.array([5,0,0],np.uint8)


Title_original = "Original Image"
Title_parcial = "Parcial"

cv2.namedWindow( Title_original,  cv2.CV_WINDOW_AUTOSIZE )
cv2.namedWindow(Title_parcial, cv2.CV_WINDOW_AUTOSIZE)

cv2.setMouseCallback(Title_original,_mouseEvent)

for i in range(10,-1,-1):
    capture = cv2.VideoCapture(i)
    if capture.isOpened():
        capture.open(i)
        print 'camara:', i
        break

_, img = capture.read()

dimenciones =  img.shape[:2]
cen =  [dimenciones[1]/2 , dimenciones[0]/2]

margenLocal = 200


img_aux = 0

imgParcial = 0
while True:


    _, img = capture.read()
    if len(esquinasCancha) == 2:
        img = img[esquinasCancha[0].pos[1] : esquinasCancha[1].pos[1] , esquinasCancha[0].pos[0] : esquinasCancha[1].pos[0]]

    imgBlur = cv2.blur(img,(10,10))

    hsv_img = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)

    for obj in [obj for obj in objetos if isinstance(obj, Movil)]:

        lower[0] = obj.color
        upper[0] = obj.color

        lower = cv2.subtract(lower,error)
        upper = cv2.add(upper,error)


        ml = max(80, min(margenLocal , int(obj.area/10000)))


        hsv_imgParcial , pos = subImagen(hsv_img,obj.pos,ml)

        imgParcial, _ = subImagen(img,obj.pos,ml)

        thresGrande = cv2.inRange(hsv_img, lower, upper)
        thresChico = cv2.inRange(hsv_imgParcial, lower, upper)

        momentsGrande = cv2.moments(thresGrande, 0)
        momentsChico = cv2.moments(thresChico, 0)


        areaChica = momentsChico['m00']
        areaGrande = momentsGrande['m00']


        if (areaChica > 10):
            x2 = (np.uint32)(momentsChico['m10']/areaChica) + pos[0]
            y2 = (np.uint32)(momentsChico['m01']/areaChica) + pos[1]
            img2 = cv2.bitwise_and(imgParcial,imgParcial, mask= thresChico)


            cv2.circle(img, (x2, y2), 2, (0,255,0) , 10)

            cv2.rectangle(img, pos, (pos[0] + imgParcial.shape[1], pos[1] + imgParcial.shape[0]), 255, 2)


            cv2.imshow(Title_parcial, img2)
            obj.actualizar((x2,y2))



    for obj in objetosVisibles:
        cv2.circle(img, obj.pos, 2, obj.colDisplay, 10)


    cv2.imshow(Title_original, img)



    key = cv2.waitKey(10)
    if key == 27:
        capture.release()
        break
    elif key == 122:
        obj = objetos.pop()
        for list in (esquinasCancha , objetosVisibles):
            if obj in list: list.remove(obj)



cv2.destroyAllWindows()











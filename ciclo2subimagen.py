import numpy as np
import cv2
import tcp_client_robot_1_2015 as tcp
import time


def subImagen(img, pos, margen):

    xMin = max(0 , pos[0] - margen)
    xMax = min(img.shape[1], pos[0] + margen)
    yMin = max(0 , pos[1] - margenLocal)
    yMax = min(img.shape[0], pos[1] + margen)

    return img.copy()[yMin: yMax, xMin: xMax], (xMin,yMin)


objetos = []

class Objeto:

    def __init__(self,color,area):
        self.color = color
        self.colDisplay = (255,255,255)
        self.area = area


    def actualizar(self,pos):
        self.pos = pos

def _mouseEvent(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        global lower
        global upper

        col = hsv_img[y,x,0]

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

        obj = Objeto(col, areaChica)
        col = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)[y,x]
        obj.colDisplay = (col[0],col[1],col[2])
        objetos.append(obj)
        obj.actualizar((x,y))



img = 1
hsv_img = 1

lower= np.array([0,50,50],np.uint8)
upper= np.array([5,255,255],np.uint8)
error = np.array([5,0,0],np.uint8)


Title_original = "Original Image"
Title_parcial = "Parcial"
Title_color = "Color"
cv2.namedWindow( Title_original,  cv2.CV_WINDOW_AUTOSIZE )
cv2.namedWindow(Title_parcial, cv2.CV_WINDOW_AUTOSIZE)
cv2.namedWindow(Title_color)

cv2.setMouseCallback(Title_original,_mouseEvent)

for i in range(10,-1,-1):
    capture = cv2.VideoCapture(i)
    if capture.isOpened():
        capture.open(i)
        print i
        break

_, img = capture.read()

dimenciones =  img.shape[:2]
cen =  [dimenciones[1]/2 , dimenciones[0]/2]

margenLocal = 200


img_aux = 0

imgParcial = 0
while True:
    _, img = capture.read()

    imgBlur = cv2.blur(img,(10,10))

    hsv_img = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)

    for obj in objetos:

        lower[0] = obj.color
        upper[0] = obj.color

        lower = cv2.subtract(lower,error)
        upper = cv2.add(upper,error)


        ml = max(50 ,  min(margenLocal , int(obj.area/10000)))


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

        if(areaGrande > 10):

            x = (np.uint32)(momentsGrande['m10']/areaGrande)
            y = (np.uint32)(momentsGrande['m01']/areaGrande)


            cv2.circle(img, (x, y), 2, (255,0,0) , 10)

            img_aux = cv2.bitwise_and(imgBlur,imgBlur, mask= thresGrande)

            cv2.imshow(Title_color, img_aux)



    cv2.circle(img, (cen[0],cen[1]), 2, (255,255,255), 10)

    #cv2.imshow(Title_parcial, imgParcial)
    cv2.imshow(Title_original, img)
    cv2.imshow(Title_color, img_aux)



    if cv2.waitKey(10) == 27:
            capture.release()
            break





cv2.destroyAllWindows()










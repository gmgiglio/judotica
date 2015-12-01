import numpy as np
import cv2
import time

def iniciar():
    global capture

    Title_tracker = "Color Tracker"
    Title_original = "Original Image"
                  
    cv2.namedWindow( Title_tracker,  cv2.CV_WINDOW_AUTOSIZE )
    cv2.namedWindow( Title_original,  cv2.CV_WINDOW_AUTOSIZE )

    capture = cv2.VideoCapture(0)

    if capture.isOpened():
        capture.open(0)

        
cierra = False
def _mouseEvent(event, _x, _y, flags, param):
    global hsv_img
    global lower
    global upper
    global error
    global x
    global y
    x = _x
    y= _y

    if event == cv2.EVENT_LBUTTONDOWN:
        global cierra
        cierra = True


def pos_inicial():
    global capture
    img = 1
    hsv_img = 1

    Title_tracker = "Color Tracker"
    Title_original = "Original Image"
                  
    cv2.namedWindow( Title_tracker,  cv2.CV_WINDOW_AUTOSIZE )
    cv2.namedWindow( Title_original,  cv2.CV_WINDOW_AUTOSIZE )

    cv2.setMouseCallback(Title_original,_mouseEvent)


    while True:
        _, img = capture.read()
        cv2.imshow(Title_original, img)


        if cv2.waitKey(10) == 27:
            capture.release()
            break
        if cierra:
            vector = [x, y]
            capture.release()
            break

    cv2.destroyAllWindows()
    return vector



def color_pos(vec):
    global hsv_img
    return hsv_img[vec[0],vec[1],0]

def pos_objeto(color):
    global lower
    global upper
    global error
    
    lower[0] = color
    upper[0] = color    

    lower = cv2.subtract(lower,error)
    upper = cv2.add(upper,error)

    Title_tracker = "Color Tracker"
    Title_original = "Original Image"

    
    _, img = capture.read()            

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

    thres = cv2.inRange(hsv_img, lower, upper)
                
    moments = cv2.moments(thres, 0)
                
    area = moments['m00']

    if(area > 1000):
                   
        x = (np.uint32)(moments['m10']/area)
        y = (np.uint32)(moments['m01']/area)
        vector = [x, y]
        cv2.circle(img, (x, y), 2, (255, 255, 255), 10)             
    return vector


def centro():
    dimenciones =  capture.read()[1].shape[:2]
    return [dimenciones[0]/2 , dimenciones[1]/2]

iniciar()
pos = pos_inicial()
print pos
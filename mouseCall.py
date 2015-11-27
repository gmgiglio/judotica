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
def _mouseEvent(event, x, y, flags, param):
    global hsv_img
    global lower
    global upper
    global error

    if event == cv2.EVENT_LBUTTONDOWN:
        lower[0] = hsv_img[y,x,0]
        upper[0] = hsv_img[y,x,0]     

        lower = cv2.subtract(lower,error)
        upper = cv2.add(upper,error) 
        global cierra
        cierra = True
        #print lower, upper


def pos_inicial():
    global hsv_img
    global lower
    global upper
    global error
    img = 1
    hsv_img = 1

    lower= np.array([0,50,50],np.uint8)
    upper= np.array([5,255,255],np.uint8)
    error = np.array([15,0,0],np.uint8);

    Title_tracker = "Color Tracker"
    Title_original = "Original Image"
                  
    cv2.namedWindow( Title_tracker,  cv2.CV_WINDOW_AUTOSIZE )
    cv2.namedWindow( Title_original,  cv2.CV_WINDOW_AUTOSIZE )

    cv2.setMouseCallback(Title_original,_mouseEvent)

    capture = cv2.VideoCapture(0)

    if capture.isOpened():
        capture.open(0)
  

    xprom = 0
    yprom = 0
    par = 0.9
    while True:
        _, img = capture.read()            

        cv2.imshow(Title_original, img)

        img = cv2.blur(img,(10,10))

        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

        thres = cv2.inRange(hsv_img, lower, upper)
                    
        moments = cv2.moments(thres, 0)
                    
        area = moments['m00']

        if(area > 1000):
                       
            x = (np.uint32)(moments['m10']/area)
            y = (np.uint32)(moments['m01']/area)
            vector = [x, y]
            cv2.circle(img, (x, y), 2, (255, 255, 255), 10)
            #print 'x: ' + str(x) + ' y: ' + str(y)
            img_aux = cv2.bitwise_and(img,img, mask= thres)              
      
            cv2.imshow(Title_tracker, img_aux)

        if cv2.waitKey(10) == 27:
            capture.release()
            break
        if cierra:
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
   
    #capture = cv2.VideoCapture(0)

    #if capture.isOpened():
        #capture.open(0)
    
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
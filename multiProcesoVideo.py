__author__ = 'gianfrancogiglio'

import multiprocessing as mp
import cv2
import time



def correrVideo(q):

    capture = cv2.VideoCapture(0)

    if capture.isOpened():
        capture.open(0)

    Title_original = "Original Image"

    cv2.namedWindow( Title_original,  cv2.CV_WINDOW_AUTOSIZE )

    while True:
        _, img = capture.read()
        q.put(img)
        cv2.imshow(Title_original, img)


def imprimir(q):
    img = q.get()
    while True:
        print img.shape
        time.sleep(4)


q = mp.Queue()

pros1 = mp.Process(target= correrVideo,args=(q,))
pros2 = mp.Process(target= imprimir, args= (q,) )


pros1.start()
pros2.start()
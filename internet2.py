import os
import threading
import matplotlib.pyplot
import cv2


#assert os.path.isfile(video_path_1)
#assert os.path.isfile(video_path_2)


class MyThread (threading.Thread):
    maxRetries = 20

    def __init__(self, thread_id, name, video_url, thread_lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.video_url = video_url
        self.thread_lock = thread_lock

    def run(self):
        print "Starting " + self.name
        window_name = self.name
        print "nombre", window_name
        cv2.namedWindow("hola")
        video = cv2.VideoCapture(self.video_url)
        while True:
            # self.thread_lock.acquire()  # These didn't seem necessary
            got_a_frame, image = video.read()
            # self.thread_lock.release()
            if not got_a_frame:  # error on video source or last frame finished
                break
            cv2.imshow(window_name, image)
            key = cv2.waitKey(50)
            if key == 27:
                break
        cv2.destroyWindow(window_name)
        print self.name + " Exiting"


def main():
    thread_lock = threading.Lock()
    thread1 = MyThread(1, "hola", 0, thread_lock)
    thread2 = MyThread(2, "chao", 0, thread_lock)
    thread1.start()
    thread2.start()
    print "Exiting Main Thread"

if __name__ == '__main__':
    main()

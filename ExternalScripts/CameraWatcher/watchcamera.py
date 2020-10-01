import cv2
import zmq
import io
import numpy as np


class FurHatStream:
    def __init__(self, size, record):
        self.size = size
        self.record = record
        context = zmq.Context()
     
        self.footage_socket = context.socket(zmq.SUB)
        self.footage_socket.connect('tcp://192.168.43.131:3000')
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        if record:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter("output.avi", fourcc, 10, self.size)
       
    def run(self):
        while True:
            try:
                frame = self.footage_socket.recv()
                imgBuff = np.frombuffer(frame, dtype=np.uint8)
                print(imgBuff)
                img = cv2.imdecode(imgBuff, cv2.IMREAD_COLOR)
                img = cv2.resize(img, self.size, interpolation = cv2.INTER_AREA)
                if self.record:
                    self.video_writer.write(img)
                cv2.imshow("FurHatStream", img)
                cv2.waitKey(1)

            except KeyboardInterrupt:
                if self.record:
                    self.video_writer.release()
                cv2.destroyAllWindows()  
                break


stream = FurHatStream(size = (800, 600), record = False)
stream.run()
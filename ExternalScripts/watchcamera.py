import cv2
import zmq
import base64
import io
import numpy as np
from PIL import Image 
context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.connect('tcp://192.168.43.131:3000')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, "")

while True:
    try:
        frame = footage_socket.recv()
        imgBuff = np.frombuffer(frame, dtype=np.uint8)
        print(imgBuff)
        img = cv2.imdecode(imgBuff, cv2.IMREAD_COLOR)
        
        scale_percent = 200
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        
        cv2.imshow("image", resized)
        cv2.waitKey(1)

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break

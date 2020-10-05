"""Usage: 
    watchcamera.py [-o FILE] [--width=WIDTH] [--height=HEIGHT] HOST

Example, try:
    watchcamera.py 127.0.0.1
    watchcamera.py -o output.avi 127.0.0.1
    watchcamera.py --width=1920 --height=1080 -o output.avi 127.0.0.1

Options:
    -h --help                   show this
    -o FILE, --output FILE      filename of recording, if not provided no recording will be made.
    --width=WIDTH               width of the stream [default: 800]
    --height=HEIGHT             height of the stream [default: 600]

"""

import cv2
import zmq
import io
import numpy as np
from docopt import docopt

class FurHatStream:
    def __init__(self, host, size, record_output):
        self.size = size
        self.record_output = record_output
        #Testing facial recongintion
        context = zmq.Context()
        host = 'tcp://{0}:3000'.format(host)
        print('Setting host to: {0}'.format(host))
        print('Setting size to: {0}'.format(size))
        if record_output:
            print('Setting output file to: {0}'.format(record_output))
        else:
            print('No recoring will be made')

        self.footage_socket = context.socket(zmq.SUB)
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.footage_socket.setsockopt(zmq.RCVHWM, 1)
        self.footage_socket.setsockopt(zmq.CONFLATE, 1)
        
        self.footage_socket.connect(host)
        if record_output:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(record_output, fourcc, 10, self.size)
       
    def run(self):
        print('Running')
        print('To exit close this script with Ctrl+C')
        while True:
            try:
                frame = self.footage_socket.recv()
                imgBuff = np.frombuffer(frame, dtype=np.uint8)
                #print(imgBuff)
                img = cv2.imdecode(imgBuff, cv2.IMREAD_COLOR)
                img = cv2.resize(img, self.size, interpolation = cv2.INTER_AREA)
                if self.record_output:
                    self.video_writer.write(img)
                cv2.imshow("FurHatStream", img)
                cv2.waitKey(1)

            except KeyboardInterrupt:
                if self.record_output:
                    self.video_writer.release()
                cv2.destroyAllWindows()  
                break

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Furhat camerastreamer v.1')
    record_output = arguments["--output"]
    host = arguments["HOST"]
    width = arguments["--width"]
    height = arguments["--height"]
    print('Starting')
    stream = FurHatStream(host = host, size = (int(width), int(height)), record_output=record_output)
    stream.run()

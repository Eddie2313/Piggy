import time
import sys
import select
import termios
import tty
import cv2
import numpy as np
import onnxruntime as ort
from picamera2 import Picamera2
from gpiozero import Motor
#this wont work on your computer since its using picamera and a model trained on my device
#use for learning purposes


MODEL_PATH = "/home/pi/piggy/yolo_carrot/models/best.onnx"
IMGSZ = 640

CONF_THRES = 0.4
IOU_THRES = 0.45

BASE_SPEED = 0.45
TURN_GAIN = 0.6
DEADZONE = 0.08

STOP_TOO_CLOSE_AREA = 0.18
MIN_BOX_AREA = 0.003
LOST_TIMEOUT = 0.6


LEFT = Motor(17, 27, enable=18, pwm=True)
RIGHT = Motor(22, 23, enable=19, pwm=True)

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def drive(l, r):
    l = clamp(l, -1, 1)
    r = clamp(r, -1, 1)

    if l > 0: LEFT.forward(l)
    elif l < 0: LEFT.backward(-l)
    else: LEFT.stop()

    if r > 0: RIGHT.forward(r)
    elif r < 0: RIGHT.backward(-r)
    else: RIGHT.stop()

def stop():
    LEFT.stop()
    RIGHT.stop()
#used ai to help me with the decode
def decode(out):
    out = out[0] if out.ndim == 3 else out  

    
    if out.shape[0] != 84:
        
        return None

    boxes = out[:4, :].T        
    cls_scores = out[4:, :].T   

    conf = cls_scores.max(axis=1)

    keep = conf > CONF_THRES
    if not np.any(keep):
        return None

    boxes = boxes[keep]
    conf = conf[keep]

    i = int(np.argmax(conf))
    return boxes[i]
#motor logic
#normally with a headless robot termios wouldn't work since we arent usin a terminal but i kept it herere so that when we tested out the pi via ssh it would let us 
#see the program running and exit out

def main():
    sess = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
    inp = sess.get_inputs()[0].name

    cam = Picamera2()
    cam.configure(cam.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    ))
    cam.start()
    time.sleep(0.5)

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setcbreak(fd)

    last_seen = 0

    try:
        while True:
            if select.select([sys.stdin], [], [], 0)[0]:
                if sys.stdin.read(1) == "q":
                    break

            frame = cam.capture_array()
            h, w = frame.shape[:2]

            img = cv2.resize(frame, (IMGSZ, IMGSZ))
            x = img.astype(np.float32) / 255.0
            x = np.transpose(x, (2, 0, 1))[None]

            out = sess.run(None, {inp: x})[0]
            box = decode(out)

            now = time.time()

            if box is not None:
                cx = box[0]
                cy = box[1]
                bw = box[2]
                bh = box[3]

                area = (bw * bh) / (IMGSZ * IMGSZ)

                last_seen = now

                if area > STOP_TOO_CLOSE_AREA:
                    stop()
                    print("STOP (too close)")
                elif area < MIN_BOX_AREA:
                    stop()
                else:
                    x_err = (cx - IMGSZ/2) / (IMGSZ/2)
                    if abs(x_err) < DEADZONE:
                        x_err = 0

                    turn = x_err * TURN_GAIN
                    drive(BASE_SPEED - turn, BASE_SPEED + turn)
                    print("CHASE")

            else:
                if now - last_seen > LOST_TIMEOUT:
                    stop()
                    print("STOP (lost)")

            time.sleep(0.01)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        stop()
        cam.stop()

if __name__ == "__main__":
    main()
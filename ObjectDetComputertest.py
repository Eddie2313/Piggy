#look at ObjectDetectionYolo.py first
import os
import time

import cv2
import numpy as np
import onnxruntime as ort
import os
#same deal with this program
#it wont work on your device becauase the model is on my device
#same code logic as objectdetectionyolo.py but instead of using picamera we use laptop webcam
#####
#settings below
MODEL_PATH = MODEL_PATH = "C:/Users/pixel/OneDrive/Documents/Piggy project/Piggy-1/runs/detect/train/weights/best.onnx"
IMGSZ = 640

CONF_THRES = 0.4
IOU_THRES = 0.45

BASE_SPEED = 0.45
TURN_GAIN = 0.6
DEADZONE = 0.08

STOP_TOO_CLOSE_AREA = 0.18
MIN_BOX_AREA = 0.003
LOST_TIMEOUT = 0.6
#####

#LEFT = Motor(17, 27, enable=22, pwm=True)
#RIGHT = Motor(23, 24, enable=25, pwm=True)


def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def drive(l, r):
     print(f"drive L={l:.2f} R={r:.2f}")
def stop():
    print("stop")
#### 
# used ai for decode 

def decode(out):

    
    out = out[0]  

    
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

def main():
    sess = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
    inp = sess.get_inputs()[0].name

   # cam = Picamera2()
    #cam.configure(cam.create_preview_configuration(
     #   main={"format": "RGB888", "size": (640, 480)}
#))
 #   cam.start()
  #  time.sleep(0.5)

   # fd = sys.stdin.fileno()
    #old = termios.tcgetattr(fd)
    #tty.setcbreak(fd)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("camera cannot be opened.")
        exit()              
   
    last_seen = time.time()
#ignore motor logic didnt feel like commenting it out, but it wont do anything either way
#focus on the print out logic if the carrot is detected

    try:
        while True:
          
            ret, frame=cap.read() 
           
            if not ret:
                continue
            h, w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.resize(rgb, (IMGSZ, IMGSZ))
            display = img.copy()
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
                x1=int (cx-bw/2)
                x2=int (cx+bw/2)
                y1=int (cy-bh/2)
                y2=int (cy+bh/2)
#here since we used the computer we can easily build bounding boxes and labels around the carrot it detects 
# wont be able to do this on the pi however

                cv2.rectangle(display, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.circle(display, (int(cx), int(cy)), 5, (0,0,255), -1)
                cv2.putText(display, "Carrot", (x1, max(y1 - 10, 20)),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)   
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
            cv2.imshow("Carrot Detected", display)

   
            if cv2.waitKey(1) & 0xFF == ord('q'):
                  break
            time.sleep(0.01)


    finally:
        #termios.tcsetattr(fd, termios.TCSADRAIN, old)
       # stop()
       # cam.stop()
        cap.release()
        cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
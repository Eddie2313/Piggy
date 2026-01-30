import cv2
import numpy as np
#ideal HSV colors for the carrot
ORANGE_LOW = np.array([5, 120, 80])
ORANGE_HIGH = np.array([25, 255, 255])
MIN_AREA = 1500 # ignores any orange "noise", must be a minum size to evaluate

MIN_ASPECT_RATIO = 2.0# height/width ratio 
MIN_SOLIDITY = 0.80 #has to be solid enought to evaluate, no gaps or holes

cap = cv2.VideoCapture(0) # turns on camera 

if not cap.isOpened():
    raise RuntimeError("Camera not detected.")# shows message if camera isnt detected 

while True:
    ret, frame = cap.read()# 
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)# converts from open cv bgr to hsv 

    mask = cv2.inRange(hsv, ORANGE_LOW, ORANGE_HIGH) #in the mask, orange pixels turn white, and all other colors turn black
# dont know these next lines 
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)# removes small white noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) # fills small black holes inside orange shape

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#

    carrot_found = False # assumes no carrot until proven otherwise

    if contours:
        largest = max(contours, key=cv2.contourArea)# finds the largest contour

        area = cv2.contourArea(largest)# gets blob size in pixels
        if area > MIN_AREA:# only works if area is big enough to matter
            x, y, w, h = cv2.boundingRect(largest)# creates a bounding recatangle

            aspect_ratio = h / float(w)# creates an aspect ratio height divided by width 
            hull = cv2.convexHull(largest) # builds the convex hull of the contour largest.
            hull_area = cv2.contourArea(hull) #calculates the area inside the hull polygon
            solidity = area / float(hull_area) if hull_area > 0 else 0 #(area of the actual contour) ÷ (area of its convex hull)

            perimeter = cv2.arcLength(largest, True) #Measures the perimeter (outline length) of the contour.
            epsilon = 0.02 * perimeter#epsilon is the max deviation between the original contour and the original version, 
            #Sets a “tolerance” for simplifying the contour.
            approx = cv2.approxPolyDP(largest, epsilon, True) #uses Dougler-Pecker algom and it removes points that don’t change the shape much (within epsilon).

            if (aspect_ratio > MIN_ASPECT_RATIO) and (solidity > MIN_SOLIDITY) and (len(approx) < 20):#condtions to be met to identify carrot 
                carrot_found = True

            color_box = (0, 255, 0) if carrot_found else (0, 0, 255) #if carrot found green text, otherwise red text 
            cv2.rectangle(frame, (x, y), (x + w, y + h), color_box, 2)#draws the rectangle around the frame

            cv2.drawContours(frame, [largest], -1, color_box, 2)#draws the actual contour of the item
                #each of these lines below puts a text according the corresponding aspect we are looking at
                # like area, aspeact or solidity
            cv2.putText(frame, f"Area: {int(area)}", (x, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_box, 2)
            cv2.putText(frame, f"Aspect: {aspect_ratio:.2f}", (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_box, 2)
            cv2.putText(frame, f"Solidity: {solidity:.2f}", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_box, 2)

            label = "CARROT (orange + shape)" if carrot_found else "Incorrect object (not carrot-like)" #finally labels carrot if carrot is found otherwise incorrect object
            cv2.putText(frame, label, (x, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_box, 2)

    cv2.imshow("Piggy Vision - Camera", frame)#opens the camera
    cv2.imshow("Orange Mask", mask)#opens the mask

    if cv2.waitKey(1) & 0xFF == ord('q'):#press q in order to exit camera
        break

cap.release()
cv2.destroyAllWindows()#exits out of the camera and mask windows

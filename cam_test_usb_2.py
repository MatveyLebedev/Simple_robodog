import numpy as np
import cv2
import time

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 100)
cam.set(cv2.CAP_PROP_EXPOSURE, -10)

ret, frame = cam.read()
S = time.time()
while(True):
    ret, frame = cam.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    im_blure = cv2.blur(gray_frame, (4, 4))

    r, imgf = cv2.threshold(im_blure, 250, 255, cv2.THRESH_BINARY)
    M = cv2.moments(imgf)

    try:
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])

        print('X : ', cX, ', Y : ', cY, ', FPS =', round(1/(time.time()-S)) )
        cv2.circle(frame, (cX, cY), 5, (255, 0, 255), -1)
    except:
        print('No target', ', FPS = ', round(1/(time.time()-S)) )
    S = time.time()

    cv2.imshow('img', frame)
    cv2.imshow('img_gray', gray_frame)
    cv2.imshow('im_blur', im_blure)
    cv2.imshow('imf_filterd', imgf)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

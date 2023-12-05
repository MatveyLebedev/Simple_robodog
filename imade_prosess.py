import numpy as np
import cv2

img = cv2.imread('imgs/im2.jpg', cv2.COLOR_BGR2GRAY)
r, imgf = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY)
M = cv2.moments(imgf)
cX = int(M['m10'] / M['m00'])
cY = int(M['m01'] / M['m00'])

print('X : ', cX, ' Y : ', cY)
cv2.circle(imgf, (cX, cY), 5, (0, 0, 0), -1)

cv2.imshow('im2', img)
cv2.imshow('om1', imgf)

cv2.waitKey(0)
cv2.destroyAllWindows()

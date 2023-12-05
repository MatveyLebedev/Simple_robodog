import numpy as np
import cv2


cam = cv2.VideoCapture(0)

ret, frame = cam.read()
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

cv2.imwrite('imgs/im2.jpg', gray_frame)
arr = np.array(frame)
np.save('imgs/arr2', gray_frame)

cam.release()
cv2.destroyAllWindows()
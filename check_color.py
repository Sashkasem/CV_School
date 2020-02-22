import cv2
import numpy as np
import constants as const

cap = cv2.VideoCapture(0)

def colorChek(imgHSV):
    # define range of blue color in HSV
    lower_blue = np.array(const.l_blueHSV)
    upper_blue = np.array(const.u_blueHSV)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(imgHSV, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(imgHSV, imgHSV, mask=mask)
    return mask, res

while(1):

    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    cv2.imshow('frame', frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask, res = colorChek(hsv)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
#component_of_color(hsv, n_rows, n_cols)
cv2.destroyAllWindows()
cap.release()
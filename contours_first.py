import cv2
import numpy as np
import constants as const

cap = cv2.VideoCapture(0)



while(1):

    # Take each frame
    _, frame = cap.read()
    frame = cv2.resize(frame, (const.CAM_WIDTH, const.CAM_HEIGHT))
    # Convert BGR to HSV
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 0)
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    image_with_contours = frame.copy()
    image_with_contours = cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 3)
    cv2.imshow('frame',frame)
    cv2.imshow('image_with_contours', image_with_contours)
    cv2.imshow('gray', gray)
    cv2.imshow('thresh', thresh)



    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
#component_of_color(hsv, n_rows, n_cols)
cv2.destroyAllWindows()
cap.release()
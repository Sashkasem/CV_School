import cv2
import numpy as np
import constants as const

cap = cv2.VideoCapture(0)



while(1):

    # Take each frame
    _, frame = cap.read()
    frame = cv2.resize(frame, (const.CAM_WIDTH, const.CAM_HEIGHT))
    # Convert BGR to HSV
    black = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sobel = cv2.Sobel(black,cv2.CV_64F,1,0,ksize=5)
    laplacian = cv2.Laplacian(black,cv2.CV_64F)
    canny = cv2.Canny(frame, 100, 200)

    cv2.imshow('frame',frame)
    cv2.imshow('black', black)
    cv2.imshow('laplacian', laplacian)
    cv2.imshow('sobel', sobel)
    cv2.imshow('canny', canny)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
#component_of_color(hsv, n_rows, n_cols)
cv2.destroyAllWindows()
cap.release()
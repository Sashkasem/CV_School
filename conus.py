import cv2
import numpy as np
import constants as const

cap = cv2.VideoCapture(0)

selected_color = None

def onmouse(event, x, y, flags, param):
    global selected_color
    if flags & cv2.EVENT_FLAG_LBUTTON:
        #taking squire cur 3x3
        cut = frame[y-1:y+2, x-1:x+2]
        cut_average = list(cv2.mean(cut))[0:3]
        selected_color = [int(x) for x in cut_average]

def colorChek(imgHSV):
    # define range of blue color in HSV
    if selected_color is None:
        lower = np.array(const.l_blueHSV)
        upper = np.array(const.u_blueHSV)
    else:
        #lower = np.array(selected_color)
        #upper = np.array(selected_color)
        lower = cv2.cvtColor(np.uint8([[selected_color]]), cv2.COLOR_BGR2HSV)
        upper = cv2.cvtColor(np.uint8([[selected_color]]), cv2.COLOR_BGR2HSV)
        print("lower: ",lower.tolist())

        lower = np.add(lower.tolist()[0][0],[-10,-10,-10])
        upper = np.add(upper.tolist()[0][0], [10, 10, 10])
        print("upper: ",upper)
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(imgHSV, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(imgHSV, imgHSV, mask=mask)
    return mask, res


cv2.namedWindow('frame')
cv2.setMouseCallback('frame', onmouse)

while(1):

    # Take each frame
    _, frame = cap.read()
    frame = cv2.resize(frame, (const.CAM_WIDTH, const.CAM_HEIGHT))
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask, res = colorChek(hsv)
    if selected_color is not None:
        cv2.circle(frame, (const.CAM_WIDTH-20,20), 20, selected_color, -1)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
#component_of_color(hsv, n_rows, n_cols)
cv2.destroyAllWindows()
cap.release()
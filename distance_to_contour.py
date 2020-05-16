import cv2
import numpy as np
import constants as const

cap = cv2.VideoCapture(0)

selected_color = None
cursor_x = 0
cursor_y = 0
distance_to_contour = -2
font = cv2.FONT_HERSHEY_SIMPLEX

def onmouse(event, x, y, flags, param):
    global selected_color , cursor_x, cursor_y
    cursor_x = x
    cursor_y = y
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

        lower = np.add(lower.tolist()[0][0],[-10,-30,-30])
        upper = np.add(upper.tolist()[0][0], [10, 30, 30])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(imgHSV, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(imgHSV, imgHSV, mask=mask)
    return mask, res

def component(img):
    img, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours.sort(key = lambda cnt: cv2.contourArea(cnt) , reverse=True)
    if contours:
        big_comp = contours[0]
    else:
        big_comp = None
    return big_comp

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', onmouse)

while(1):

    # Take each frame
    _, frame = cap.read()
    frame = cv2.resize(frame, (const.CAM_WIDTH, const.CAM_HEIGHT))
    # Convert BGR to HSV
    frame = cv2.blur(frame,(3,3))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask, res = colorChek(hsv)
    if selected_color is not None:
        cv2.circle(frame, (const.CAM_WIDTH-20,20), 20, selected_color, -1)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res', res)
    contour_big = frame.copy()

    big_comp = component(mask)
    if big_comp is not None:
        contour_big = cv2.drawContours(contour_big, [big_comp], 0, (0, 255, 0), 3)
        distance_to_contour = cv2.pointPolygonTest(big_comp,(cursor_x,cursor_y),True)
        cv2.putText(contour_big, str(int(distance_to_contour)) , (10, 100), font, 2, (255, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('contour_big', contour_big)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
#component_of_color(hsv, n_rows, n_cols)
cv2.destroyAllWindows()
cap.release()
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

        lower = np.add(lower.tolist()[0][0],[-10,-30,-30])
        upper = np.add(upper.tolist()[0][0], [10, 30, 30])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(imgHSV, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(imgHSV, imgHSV, mask=mask)
    return mask, res

def component(img):
    rows, cols = img.shape
    pointComponent = np.ones((rows, cols), np.int)
    pointComponent *= -1
    num = 0
    queue = []
    maximums = []
    counter = 0

    for i in range(rows):
        for j in range(cols):

            if img[i,j] == 0 or pointComponent[i][j] != -1:
                continue
            pointComponent[i][j] = num
            num += 1
            queue.append([i,j])
            counter = 1
            while(len(queue)>0):
                p = queue.pop(0)
                for di in range(-1,2):
                    for dj in range (-1,2):

                        if (p[0]+di == rows) or (p[0]+di == -1) or (p[1]+dj == cols) or (p[1]+dj == -1):
                            continue
                        if di == 0 or dj == 0:
                            continue
                        if img[p[0]+di][p[1]+dj] == 0:
                            continue
                        if pointComponent[p[0]+di][p[1]+dj] != -1:
                            continue
                        pointComponent[p[0]+di][p[1]+dj] = num
                        queue.append([p[0]+di,p[1]+dj])
                        counter+=1
            maximums.append(counter)
    if not maximums:
        print("PROBLEM")
        return img

    big_component_amount = max(maximums)
    big_component_index = maximums.index(big_component_amount)
    big_comp = img.copy()
    for i in range(rows):
        for j in range(cols):
            if pointComponent[i][j] != big_component_index:
               big_comp[i][j] = 0
    return big_comp

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', onmouse)

while(1):

    # Take each frame
    _, frame = cap.read()
    frame = cv2.resize(frame, (const.CAM_WIDTH, const.CAM_HEIGHT))
    # Convert BGR to HSV
    frame = cv2.blur(frame,(9,9))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask, res = colorChek(hsv)
    if selected_color is not None:
        cv2.circle(frame, (const.CAM_WIDTH-20,20), 20, selected_color, -1)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res', res)
    big_comp = component(mask)
    cv2.imshow('big_comp', big_comp)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
#component_of_color(hsv, n_rows, n_cols)
cv2.destroyAllWindows()
cap.release()
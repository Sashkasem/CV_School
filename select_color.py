import cv2

cap = cv2.VideoCapture(0)

#set camera width and height
CAM_WIDTH = 640
CAM_HEIGHT = 480

selected_color = None

def onmouse(event, x, y, flags, param):
    global selected_color
    if flags & cv2.EVENT_FLAG_LBUTTON:
        #taking squire cur 3x3
        cut = frame[y-1:y+2, x-1:x+2]
        cut_average = list(cv2.mean(cut))[0:3]
        selected_color = [int(x) for x in cut_average]

# create window and set callback
cv2.namedWindow('img')
cv2.setMouseCallback('img', onmouse)

while(1):

    # Take each frame
    _, frame = cap.read()
    frame = cv2.resize(frame, (CAM_WIDTH, CAM_HEIGHT))

    #drawing selected colors
    if selected_color is not None:
        cv2.circle(frame, (CAM_WIDTH-20,20), 20, selected_color, -1)

    #show image
    cv2.imshow('img', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()

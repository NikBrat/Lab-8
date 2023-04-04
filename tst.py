import cv2 as cv
import math
cap = cv.VideoCapture(0)
size = (1280, 720)
fly = cv.imread('fly64.png')
height, width = fly.shape[:2]

if not cap.isOpened():
    print('Cannot open camera')
    exit()
while True:
    ret, frame = cap.read()
    frame = cv.resize(frame, size)
    if not ret:
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (21, 21), 0)
    T, blck = cv.threshold(gray, 75, 255, cv.THRESH_BINARY_INV)
    contours, hierarchy = cv.findContours(blck, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        c = max(contours, key=cv.contourArea)
        x, y, w, h = cv.boundingRect(c)
        if x+w > (math.ceil(size[0]/2)):
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        else:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
    centre = (math.ceil(x+(h/2)), y)
    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

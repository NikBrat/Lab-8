import cv2 as cv
from math import ceil

fly = cv.imread('fly64.png', cv.IMREAD_UNCHANGED)
height, width = fly.shape[:2]
fly_gray = cv.cvtColor(fly, cv.COLOR_BGR2GRAY)
b, g, r, alpha = cv.split(fly)

ret, mask = cv.threshold(alpha, 10, 255, cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask)

point = cv.imread('ref-point.jpg')
gray = cv.cvtColor(point, cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(gray, (21, 21), 0)
T, blck = cv.threshold(gray, 75, 255, cv.THRESH_BINARY_INV)
contours, hierarchy = cv.findContours(blck, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
c = max(contours, key=cv.contourArea)
x, y, w, h = cv.boundingRect(c)
cv.rectangle(point, (x, y), (x + w, y + h), (0, 255, 0), 1)

centre = (x + ceil(w / 2), y + ceil(h / 2))
fly_x = centre[0] - ceil(width / 2)
fly_y = centre[1] - ceil(height / 2)

roi = point[fly_x:(fly_x + width), fly_y:(fly_y + height)]
fly = cv.imread('fly64.png')
roi_place = cv.bitwise_and(roi, roi, mask=mask_inv)
fly_to_roi = cv.bitwise_and(fly, fly, mask=mask)

finished_piece = cv.add(roi_place, fly_to_roi)

point[fly_x:(fly_x + width), fly_y:(fly_y + height)] = finished_piece

cv.imshow('grande finale', point)
cv.waitKey(0)
cv.destroyAllWindows()

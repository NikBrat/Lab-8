import cv2 as cv
from math import ceil
fly = cv.imread('fly64.png')
point = cv.imread('ref-point.jpg')
fly_gray = cv.cvtColor(fly, cv.COLOR_BGR2GRAY)
cv.imshow('orig', fly)
height, width = fly.shape[:2]
gray = cv.cvtColor(point, cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(gray, (21, 21), 0)
T, blck = cv.threshold(gray, 75, 255, cv.THRESH_BINARY_INV)
contours, hierarchy = cv.findContours(blck, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
c = max(contours, key=cv.contourArea)
x, y, w, h = cv.boundingRect(c)
cv.rectangle(point, (x, y), (x + w, y + h), (0, 255, 0), 1)
centre = (ceil(x + (w / 2)), ceil(y + (h / 2)))
fly_x = ceil(centre[0]-width/2)
fly_y = ceil(centre[1]-height/2)
roi = point[fly_x:fly_x+width, fly_y:fly_y+height]
dst = cv.add(roi, fly)
cv.imshow('point', dst)

cv.waitKey(0)
cv.destroyAllWindows()

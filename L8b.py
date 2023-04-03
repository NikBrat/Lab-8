import cv2 as cv
# 4 вариант
# 1 задание

img = cv.imread('variant-4.jpeg')
# разбиваем изображение на каналы
b, g, r = cv.split(img)
# выводим синий канал
cv.imshow("Blue channel only", img)
cv.imshow("Blue channel only1", b)
cv.waitKey(0)




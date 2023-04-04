import cv2 as cv
# 4 вариант
# 1 задание
img = cv.imread('variant-4.jpeg')
# разбиваем изображение на каналы
b, g, r = cv.split(img)
# выводим синий канал
cv.imshow("Original photo", img)
cv.imshow("Blue channel only", b)
cv.waitKey(0)
cv.destroyAllWindows()





import cv2 as cv
from math import ceil, floor


# 4 вариант
def photo_task():
    """Функция, выполняющая 1 задание"""

    img = cv.imread('variant-4.jpeg')
    # разбиваем изображение на каналы
    b, g, r = cv.split(img)
    # выводим синий канал
    # и оригинал

    cv.imshow("Original photo", img)
    cv.imshow("Blue channel only", b)


def video_task():
    """Функция для 2 и 3 заданий"""
    option = int(input("Отслеживать полное попадание метки(1), её большой части(2)"
                       " или её края(3)?:\n"))
    cap = cv.VideoCapture(0)
    size = (1280, 720)
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
        t, blck = cv.threshold(blurred, 75, 255, cv.THRESH_BINARY_INV)
        contours, hierarchy = cv.findContours(blck, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        cv.rectangle(frame, (floor(size[0] / 2), 1), (size[0], size[1] - 2), (255, 0, 255), 1)
        if len(contours) > 0:
            c = max(contours, key=cv.contourArea)
            x, y, w, h = cv.boundingRect(c)
            if option == 1:
                opt = x
            elif option == 2:
                opt = x + ceil(w / 2)
            else:
                opt = x + w
            if opt > (ceil(size[0] / 2)):
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            else:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)

            cv.imshow('frame', frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()


# photo_task()
video_task()

cv.waitKey(0)
cv.destroyAllWindows()

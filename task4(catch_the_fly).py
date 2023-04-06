import cv2 as cv

fly = cv.imread('fly64.png', cv.IMREAD_UNCHANGED)
height, width = fly.shape[:2]
# Получаем альфа-канал
b, g, r, alpha = cv.split(fly)
# Маска для мухи
ret, mask = cv.threshold(alpha, 10, 255, cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask)

point = cv.imread('ref-point.jpg')
height1, width1 = point.shape[:2]
size = (1280, 720)
# Центр экрана, начало и конец центрального прямоугольника
centre = (size[0] // 2, size[1] // 2)
centre_s = (centre[0] - width1 // 2, centre[1] - height1 // 2)
centre_d = (centre[0] + width1 // 2, centre[1] + height1 // 2)
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print('Cannot open camera')
    exit()

while True:
    ret, frame = cap.read()
    frame = cv.resize(frame, size)
    if not ret:
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Построение центрального прямоугольника
    cv.rectangle(frame, centre_s, centre_d, (0, 204, 255), 1)
    # Построение прямоугольника вокруг метки
    blurred = cv.GaussianBlur(gray, (21, 21), 0)
    t, blck = cv.threshold(blurred, 75, 255, cv.THRESH_BINARY_INV)
    contours, hierarchy = cv.findContours(blck, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        c = max(contours, key=cv.contourArea)
        x, y, w, h = cv.boundingRect(c)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        if (centre_s[0] <= x <= centre_d[0] and centre_s[0] <= x + w <= centre_d[0]) \
                and (centre_s[1] <= y <= centre_d[1] and centre_s[1] <= y+h <= centre_d[1]):
            # точное совпадение центра мухи и метки. ОЧень капризно работает
            # if (x + w//2) == centre[0] and (y + h//2) == centre[1]:
                # Начальные координаты для вставки мухи
                fly_x = centre_s[0] + 72
                fly_y = centre_s[1] + 69
                fly_xd = centre_d[0] - 72
                fly_yd = centre_d[1] - 69
                print(fly_x, fly_y, fly_xd, fly_yd)

                roi = frame[fly_y:fly_yd, fly_x:fly_xd]
                # Ещё раз читаем изображение, fly содержал 3 канала
                # Необходимо для 'наложения' маски
                fly = cv.imread('fly64.png')

                roi_place = cv.bitwise_and(roi, roi, mask=mask_inv)
                fly_to_roi = cv.bitwise_and(fly, fly, mask=mask)

                finished_piece = cv.add(roi_place, fly_to_roi)

                frame[fly_y:fly_yd, fly_x:fly_xd] = finished_piece
    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()

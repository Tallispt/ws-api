import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from utils.image_utils import resize_img, resize_img_by_percentage, manipulate_img, detect_contours, cut_warp_image, cut_spots, auto_canny, remove_edge_percent, find_kernel
from utils.base64_utils import readb64, encode64
from utils.histogram_utils import plot_BW_hist
from assets.data import data as base

img = cv.imread("src/imgs/IMG_1858.jpg")

def detect_sensor_by_image(image):
    img = resize_img(image)
    canny = manipulate_img(img)
    drawn, contour = detect_contours(img, canny)
    output = cut_warp_image(image, contour)
    base64 = encode64(output)
    return base64, [canny, drawn, output]

def detect_sensor_by_base64(base64):
    image = readb64(base64)
    return detect_sensor_by_image(image)

# base64, image_array = detect_sensor_by_base64(base)
base64, image_array = detect_sensor_by_image(img)
i = remove_edge_percent(image_array[2], 5)
# for i in image_array:
#     cv.namedWindow("output window", cv.WINDOW_KEEPRATIO)
#     cv.imshow("output window", i)
#     cv.waitKey(0)

spots = cut_spots(i)



def function(i):
    resized = resize_img_by_percentage(i)
    blur = cv.blur(resized, (9 ,9))
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    # blur = cv.bilateralFilter(i,9,75,75)
    v = np.median(gray)
    ret, thr = cv.threshold(gray, (v+30), 255, cv.THRESH_TOZERO)
    # canny = cv.Canny(thr, 0, 70)
    canny = auto_canny(gray, 0.6)
    # canny = cv.dilate(canny, kernel, iterations=1)
    # canny = cv.erode(canny, kernel, iterations=1)
    # plot_BW_hist(thr)
    # cv.namedWindow("output window", cv.WINDOW_KEEPRATIO)
    # cv.imshow("output window", thr)
    cv.namedWindow("output", cv.WINDOW_KEEPRATIO)
    cv.imshow("output", thr)
    cv.waitKey(0)


# preto e branco, blur e circle detection
for i in spots:
    # i = resize_img(i, 100)
    gray = cv.cvtColor(i, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 31)
    thr = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 15, 2)
    # dialata = cv.dilate(thr, (5,5), iterations=2)
    # blur = cv.blur(dialata, (5,5))
    # v = np.median(blur)
    # print(v)
    # plot_BW_hist(blur)
    # rows = blur.shape[0]
    # circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 1, rows / 16,
    #                            param1=110, param2=17,
    #                            minRadius=int(rows/6), maxRadius=int(rows/4))
    # if circles is not None:
    #     circles = np.uint16(np.around(circles))
    #     for c in circles[0, :]:
    #         center = (c[0], c[1])
    #         # circle center
    #         cv.circle(blur, center, 1, (0, 100, 100), 3)
    #         # circle outline
    #         radius = c[2]
    #         cv.circle(blur, center, radius, (255, 0, 255), 3)
    cv.namedWindow("blur", cv.WINDOW_KEEPRATIO)
    cv.imshow("blur", thr)
    cv.waitKey(0)

# Aplicar mascara no circulo utilizando ponto central e 0,7 do raio
# Fazer média dos pontos e extrair um array final ordenado com replicadas, RGB, CMYK, HSV, Euclidian distance
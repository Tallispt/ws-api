import cv2 as cv
import numpy as np

def find_kernel(img):
    num_pixels = img.shape[0]*img.shape[1]
    num_kernel = int(np.sqrt(num_pixels)/12)
    if (num_kernel%2 == 0) :
        num_kernel = num_kernel + 1
    
    kernel = (num_kernel, num_kernel)
    return kernel

def resize_img(img: cv.Mat, height=504):
    width = int(img.shape[1] * height / img.shape[0])
    dim = (width, height)
    return cv.resize(img, dim, interpolation=cv.INTER_AREA)

def resize_img_by_percentage(img: cv.Mat, percent=60):
    width = int(img.shape[1] * percent / 100)
    height = int(img.shape[0] * percent / 100)
    dim = (width, height)
    return cv.resize(img, dim, interpolation=cv.INTER_AREA)

def auto_canny(img: cv.Mat, sigma=0.33) -> cv.Mat:
    # compute the median of the single channel pixel intensities
    v = np.median(img)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv.Canny(img, lower, upper)
    # return the edged image
    return edged

def manipulate_img(img: cv.Mat, kernel=(5,5), sigma=0.5):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, kernel, 0)
    canny = auto_canny(blur, sigma)
    return canny

def detect_contours(img: cv.Mat, canny: cv.Mat):
    cnts, _ = cv.findContours(
        canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:5]
    copy = img.copy()
    max = np.array([])
    for c in cnts:
        epsilon = 0.015 * cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, epsilon, True)
        if(len(approx) == 4 and cv.contourArea(c) > 1000):
          copy = cv.drawContours(copy, [approx], 0, [0, 255, 0], 5)
          max = approx
          break
    return copy, max

def cut_warp_image(img: cv.Mat, contour: list):
    points = np.multiply(contour.reshape(4,2), img.shape[0]/504)
    input_points = np.zeros((4, 2), dtype="float32")

    points_sum = points.sum(axis=1)
    input_points[0] = points[np.argmin(points_sum)]
    input_points[3] = points[np.argmax(points_sum)]

    points_diff = np.diff(points, axis=1)
    input_points[1] = points[np.argmin(points_diff)]
    input_points[2] = points[np.argmax(points_diff)]

    (top_left, top_right, bottom_right, bottom_left) = input_points
    bottom_width = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
    top_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
    right_height = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
    left_height = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))
    # Output image size
    max_width = max(int(bottom_width), int(top_width))
    max_height = max(int(right_height), int(left_height))
    # Desired points values in the output image
    converted_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])
    # Perspective transformation
    matrix = cv.getPerspectiveTransform(input_points, converted_points)
    img_output = cv.warpPerspective(img, matrix, (max_width, max_height))
    return img_output

def remove_edge_percent(img, percentage=2):
    height = img.shape[0]
    width = img.shape[1]
    diff_w = int(width*percentage/200)
    diff_h = int(height*percentage/200)
    return img[diff_h:height-diff_h, diff_w:width-diff_w]

def cut_spots(image, dim=[6,3]):
    spot_array = list()
    y_size = int(image.shape[0]/dim[0])
    x_size = int(image.shape[1]/dim[1])
    for i in range(dim[0]):
        for j in range(dim[1]) :
            row_start = y_size*i
            row_end = y_size*(i+1)            
            col_start = x_size*j
            col_end = x_size*(j+1)
            spot_array.append(image[row_start:row_end, col_start:col_end])
    return spot_array

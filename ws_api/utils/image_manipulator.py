import cv2
import numpy as np
from .image_class import Image


def resize(img: Image, height: int = 504):
    width = int(img.w * height / img.h)
    dim = (width, height)
    return Image(cv2.resize(img.image, dim, interpolation=cv2.INTER_AREA))


def thresh(img: Image, kernel=(5, 5), lower_thr=130, upper_thr=255):
    gray = cv2.cvtColor(img.image, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, kernel)
    _, threshold = cv2.threshold(blur, lower_thr, upper_thr, cv2.THRESH_BINARY)
    return Image(threshold)


def find_contour(img: Image, min_area=5000):
    contours, _ = cv2.findContours(img.image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return np.empty(), 0

    biggest = np.array([])
    max_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > min_area:
            approx = cv2.approxPolyDP(
                contour, 0.01 * cv2.arcLength(contour, True), True
            )

            if area > max_area and len(approx) >= 4:
                biggest = approx
                max_area = area

    return biggest, max_area


def create_masked(img: Image, contour):
    if contour.size == 0:
        return img
    mask = np.zeros(img.dim, np.uint8)
    cv2.fillPoly(mask, [contour], (255, 255, 255))
    return Image(cv2.bitwise_and(img.image, img.image, mask=mask))


def gray(img: Image):
    if len(img.image.shape) > 2:
        return Image(cv2.cvtColor(img.image, cv2.COLOR_BGR2GRAY))
    return img


def split(img: Image):
    if len(img.image.shape) == 2:
        return None, None, None
    (B, G, R) = cv2.split(img.image)
    return Image(R), Image(G), Image(B)


def detect_circles(
    img: Image,
    radius_percent=1.0,
    kernel=(7, 7),
    min_dist=40,
    param_1=50,
    param_2=15,
    min_radius=1,
    max_radius=35,
    sorting_type="h",
):

    sorting_types = {"h": "Horizontal sorting (Default)", "v": "Vertical sorting"}

    img = gray(img)
    blur = cv2.blur(img.image, kernel)
    detected_circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        1,
        min_dist,
        param1=param_1,
        param2=param_2,
        minRadius=min_radius,
        maxRadius=max_radius,
    )

    if detected_circles is None:
        raise ConnectionAbortedError("No circles detected.")

    mean_radius = np.rint(np.average(detected_circles[0], axis=0) * radius_percent)[
        2
    ].astype(int)
    detected_circles = np.rint(detected_circles[0, :, :2]).astype(int)

    if sorting_type not in sorting_types:
        raise ValueError("Not existing sorting type!")

    if sorting_type == "h":
        detected_circles = np.uint16(
            sorted(detected_circles, key=lambda k: [k[1], k[0]])
        )

    if sorting_type == "v":
        detected_circles = np.uint16(
            sorted(detected_circles, key=lambda k: [k[0], k[1]])
        )

    detected_circles = np.hstack(
        (detected_circles, np.full((detected_circles.shape[0], 1), mean_radius))
    )

    return detected_circles


def transpose_points(transp_img: Image, pts_img: Image, pts: np.array):
    new_pts = pts * np.sqrt((transp_img.h * transp_img.w) / (pts_img.h * pts_img.w))
    return new_pts.astype(int)


def draw_circles(img: Image, pts: np.array, numered=True):
    image_copy = img.image.copy()
    for i, pt in enumerate(pts):
        cv2.circle(
            image_copy,
            (pt[0], pt[1]),
            pt[2],
            (0, 0, 255),
            int(np.ceil(np.prod(img.dim) * 1e-7)),
        )

        cv2.circle(
            image_copy,
            (pt[0], pt[1]),
            1,
            (255, 0, 0),
            int(np.ceil(np.prod(img.dim) * 1e-6)),
        )

        if numered:
            cv2.putText(
                image_copy,
                str(i + 1),
                (pt[0] - 10, pt[1] + 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                int(np.ceil(np.prod(img.dim) * 4e-7)),
                (0, 0, 0),
                int(np.ceil(np.prod(img.dim) * 5e-7)),
                cv2.LINE_AA,
            )

    return Image(image_copy)


def av_value(pts: np.array, image: Image, mode=0):
    modes = {
        0: "Original mode",
        1: "RGB half height mode",
        2: "HSV threshold mode",
    }

    if mode not in modes:
        raise ValueError("Unsupported spot averaging method")

    values = []
    for pt in pts:
        spot_image, new_pt = cut_spot(pt, image)
        masked_region = mask_with_pt(new_pt, spot_image.image)
        # masked_region = mask_with_pt(pt, image.image)
        rgb_value = []

        if mode == 0:
            rgb_value = np.round(
                cv2.mean(spot_image.image, mask=masked_region)[:-1]
            ).astype(int)
            # rgb_value = np.mean(masked_region, axis=(0, 1)).filled(0).round().astype(int)

        if mode == 1:
            hist = create_hist(spot_image.image, mask=masked_region)
            rgb_value = find_av_with_half_height(hist)

        if mode == 2:
            region = hsv_thresh(spot_image.image, mask=masked_region)
            rgb_value = np.round(cv2.mean(region, mask=masked_region)[:-1]).astype(int)

        values.append(rgb_value[::-1])

    return np.array(values)


# def mask_with_pt(pt: np.array, img: cv2.Mat):
#   mask = np.zeros_like(img)
#   cv2.circle(mask, (pt[0], pt[1]), pt[2], (255, 255, 255), thickness=cv2.FILLED)
#   region = cv2.bitwise_and(img, mask)
#   masked_region = np.ma.masked_where(region == 0, region)
#   return masked_region


def mask_with_pt(pt: np.array, img: cv2.Mat):
    mask = np.zeros(img.shape[:2], np.uint8)
    cv2.circle(mask, (pt[0], pt[1]), pt[2], (255, 255, 255), thickness=cv2.FILLED)
    return mask


def create_hist(img: cv2.Mat, mask=None):
    values = []
    x_lim = 0 if np.any(mask) else 1
    for i in range(img.shape[2]):
        hist = cv2.calcHist([img], [i], mask, [256], [x_lim, 256])
        if not np.any(mask):
            hist = hist[:-1]
            hist = np.insert(hist, 0, 0)
        values.append(hist)
    return np.reshape(values, [img.shape[2], 256])


def find_av_with_half_height(hists: np.array, height_calc=0.5):
    rgb = []
    for i in range(len(hists)):
        hist = hists[i]
        max_index = np.argmax(hist)

        max_value = hist[max_index]
        half_height = max_value * height_calc

        left_index = (
            np.where(hist[:max_index] <= half_height)[0][-1]
            if np.any(hist[:max_index] <= half_height)
            else 0
        )
        right_index = (
            np.where(hist[max_index:] <= half_height)[0][0] + max_index
            if np.any(hist[max_index:] <= half_height)
            else 255
        )

        weighted_sum = sum((i * hist[i]) for i in range(left_index, right_index + 1))
        sum_of_weights = sum(hist[left_index : right_index + 1])
        mean_index = np.round(weighted_sum / sum_of_weights).astype(int)
        rgb.append(mean_index)
    return rgb


def hsv_thresh(img: cv2.Mat, mask=None):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    hist_h = cv2.calcHist([h], [0], mask, [180], [0, 181])
    hist_s = cv2.calcHist([s], [0], mask, [256], [0, 256])
    hist_v = cv2.calcHist([v], [0], mask, [256], [0, 256])

    h_max, s_max, v_max = hist_h.argmax(), hist_s.argmax(), hist_v.argmax()

    h_left_index, h_right_index = np.clip(h_max - 20, 0, 180), np.clip(
        h_max + 20, 0, 180
    )

    s_max_value = hist_s[s_max].astype(int)[0]
    half_height = s_max_value * 0.1
    s_left_index = (
        np.where(hist_s[:s_max] <= half_height)[0][-1] - 5
        if np.any(hist_s[:s_max] <= 20)
        else 0
    )
    s_right_index = (
        np.where(hist_s[s_max:] <= 20)[0][0] + s_max + 5
        if np.any(np.where(hist_s[s_max:] <= 20))
        else 255
    )

    s_left_index, s_right_index = (
        np.clip(s_left_index, 0, 255),
        np.clip(s_right_index, 0, 255),
    )

    lower_val = np.array([h_left_index, s_left_index, 20], dtype=np.uint8)
    upper_val = np.array([h_right_index, s_right_index, 255], dtype=np.uint8)

    frame_threshed = cv2.inRange(hsv, lower_val, upper_val)
    region = cv2.bitwise_and(img, img, mask=mask)
    region = cv2.bitwise_and(region, region, mask=frame_threshed)
    return region


def cut_spot(pt, img):
    spot_image = img.image[
        pt[1] - (pt[2] + 10) : pt[1] + (pt[2] + 10),
        pt[0] - (pt[2] + 10) : pt[0] + (pt[2] + 10),
    ]
    new_pt = int(len(spot_image) / 2)
    new_pts = [new_pt, new_pt, pt[2]]
    return Image(spot_image), new_pts


def create_maked_spot(pt, img, mask):
    masked_region = cv2.bitwise_and(img, img, mask=mask)
    masked_spot = masked_region[
        pt[1] - (pt[2] + 10) : pt[1] + (pt[2] + 10),
        pt[0] - (pt[2] + 10) : pt[0] + (pt[2] + 10),
    ]
    return Image(masked_spot)


def return_detected_circles(img_bytes, form_data):

    kernel = (int(form_data["kernel"]), int(form_data["kernel"]))
    min_dist = int(form_data["minDist"])
    param_1 = int(form_data["param1"])
    param_2 = int(form_data["param2"])
    min_radius = int(form_data["minRadius"])
    max_radius = int(form_data["maxRadius"])
    radius_percent = int(form_data["radiusPercent"])

    img = Image(img_bytes)
    resized_image = resize(img)
    threshold = thresh(resized_image)
    biggest, max_area = find_contour(threshold)
    masked_img = create_masked(resized_image, biggest)

    _, _, B = split(masked_img)

    pts = detect_circles(
        B,
        radius_percent=radius_percent,
        kernel=kernel,
        min_dist=min_dist,
        param_1=param_1,
        param_2=param_2,
        min_radius=min_radius,
        max_radius=max_radius,
        sorting_type="h",
    )

    new_pts = transpose_points(img, masked_img, pts)

    drawn_img = draw_circles(masked_img, pts, numered=True)

    return new_pts, drawn_img


# def find_kernel(img):
#     num_pixels = img.shape[0]*img.shape[1]
#     num_kernel = int(np.sqrt(num_pixels)/12)
#     if (num_kernel%2 == 0) :
#         num_kernel = num_kernel + 1

#     kernel = (num_kernel, num_kernel)
#     return kernel

# def resize_img_by_percentage(img: cv.Mat, percent=60):
#     width = int(img.shape[1] * percent / 100)
#     height = int(img.shape[0] * percent / 100)
#     dim = (width, height)
#     return cv.resize(img, dim, interpolation=cv.INTER_AREA)

# def auto_canny(img: cv.Mat, sigma=0.33) -> cv.Mat:
#     # compute the median of the single channel pixel intensities
#     v = np.median(img)
#     # apply automatic Canny edge detection using the computed median
#     lower = int(max(0, (1.0 - sigma) * v))
#     upper = int(min(255, (1.0 + sigma) * v))
#     edged = cv.Canny(img, lower, upper)
#     # return the edged image
#     return edged

# def manipulate_img(img: cv.Mat, kernel=(5,5), sigma=0.5):
#     gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#     blur = cv.GaussianBlur(gray, kernel, 0)
#     canny = auto_canny(blur, sigma)
#     return canny

# def cut_warp_image(img: cv.Mat, contour: list):
#     points = np.multiply(contour.reshape(4,2), img.shape[0]/504)
#     input_points = np.zeros((4, 2), dtype="float32")

#     points_sum = points.sum(axis=1)
#     input_points[0] = points[np.argmin(points_sum)]
#     input_points[3] = points[np.argmax(points_sum)]

#     points_diff = np.diff(points, axis=1)
#     input_points[1] = points[np.argmin(points_diff)]
#     input_points[2] = points[np.argmax(points_diff)]

#     (top_left, top_right, bottom_right, bottom_left) = input_points
#     bottom_width = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
#     top_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
#     right_height = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
#     left_height = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))
#     # Output image size
#     max_width = max(int(bottom_width), int(top_width))
#     max_height = max(int(right_height), int(left_height))
#     # Desired points values in the output image
#     converted_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])
#     # Perspective transformation
#     matrix = cv.getPerspectiveTransform(input_points, converted_points)
#     img_output = cv.warpPerspective(img, matrix, (max_width, max_height))
#     return img_output

# def remove_edge_percent(img, percentage=2):
#     height = img.shape[0]
#     width = img.shape[1]
#     diff_w = int(width*percentage/200)
#     diff_h = int(height*percentage/200)
#     return img[diff_h:height-diff_h, diff_w:width-diff_w]

# def cut_spots(image, dim=[6,3]):
#     spot_array = list()
#     y_size = int(image.shape[0]/dim[0])
#     x_size = int(image.shape[1]/dim[1])
#     for i in range(dim[0]):
#         for j in range(dim[1]) :
#             row_start = y_size*i
#             row_end = y_size*(i+1)
#             col_start = x_size*j
#             col_end = x_size*(j+1)
#             spot_array.append(image[row_start:row_end, col_start:col_end])
#     return spot_array

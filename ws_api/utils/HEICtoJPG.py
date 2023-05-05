import numpy as np
import cv2
import pillow_heif

image = "../"

heif_file = pillow_heif.open_heif(
    "images/rgb12.heif", convert_hdr_to_8bit=False)
heif_file.convert_to("BGRA;16" if heif_file.has_alpha else "BGR;16")
np_array = np.asarray(heif_file)
cv2.imwrite("rgb16.png", np_array)

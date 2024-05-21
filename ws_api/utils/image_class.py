import base64
import cv2
import numpy as np

# import matplotlib.pyplot as plt


class Image:
    def __init__(self, file):
        self.image = self._read_input(file)
        self.h = self.image.shape[0]
        self.w = self.image.shape[1]
        self.dim = (self.h, self.w)
        self.ratio = self.h / self.w

    def get_image(self):
        return self.image

    def _read_input(self, file):
        if isinstance(file, np.ndarray):
            return file
        elif isinstance(file, Image):
            return file.image
        elif isinstance(file, str):
            return self._read_image(file)
        elif isinstance(file, bytes):
            return self._readb64(file)
        else:
            raise ValueError(
                "Unsupported input type. Supported types: numpy array, file path, base64 string"
            )

    def _read_image(self, file):
        image = cv2.imread(file)
        if image is None:
            raise ValueError("Image input address not suported")
        return image

    def _readb64(self, file):
        #  encoded_data = file.split(',')[1]
        #  nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        nparr = np.fromstring(file, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    def _encode64(self, img):
        retval, buffer = cv2.imencode(".jpg", img)
        if not retval:
            raise Exception("Failed to encode the image to Base64.")
        base64_string = "data:image/jpeg;base64," + base64.b64encode(buffer).decode(
            "utf-8"
        )
        return base64_string

    # def display(self):
    #   if len(self.image.shape) > 2:
    #     plt.imshow(self.image[:,:,::-1])
    #   else:
    #     plt.imshow(self.image, cmap='gray')

    def save(self, name: str):
        cv2.imwrite(name, self.image)

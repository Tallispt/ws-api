import cv2 as cv
import numpy as np
import base64

def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv.imdecode(nparr, cv.IMREAD_COLOR)
   return img

def encode64(img):
   retval, buffer = cv.imencode('.jpg', img)
   if not retval:
      raise Exception("Failed to encode the image to Base64.")

   base64_string = 'data:image/jpeg;base64,' + base64.b64encode(buffer).decode('utf-8')
   return base64_string
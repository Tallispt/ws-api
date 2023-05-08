from matplotlib import pyplot as plt
import cv2 as cv

# def BW_hist(img):
#   hist = cv.calcHist([img],[0],None,[256],[0,256])
#   plot = plt.plot(hist)
#   return plot

def plot_BW_hist(img):
  hist = cv.calcHist([img],[0],None,[256],[0,256])
  plt.plot(hist)
  plt.show() 

# def RGB_hist(img):
#   color = ('b','g','r')
#   plot = plt.subplot()
#   for i,col in enumerate(color):
#       histr = cv.calcHist([img],[i],None,[256],[0,256])
#       plot.plot(histr,color = col)
#       plot.xlim([0,256])
#   return plot

def plot_RGB_hist(img):
  color = ('b','g','r')
  for i,col in enumerate(color):
      histr = cv.calcHist([img],[i],None,[256],[0,256])
      plt.plot(histr,color = col)
      plt.xlim([0,256])
  plt.show()
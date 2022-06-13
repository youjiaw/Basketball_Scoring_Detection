import cv2
import numpy as np
from scipy.interpolate import UnivariateSpline
import os
from django.conf import settings


input_video_dir = settings.MEDIA_ROOT

def _LookupTable(x, y):
    spline = UnivariateSpline(x, y)
    return spline(range(256))

# ------------------------------------------------------------------------------------------------------------

# RGB img -> gray img
def grayscale(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img

# pixel value = pixel value + beta
def bright(img, beta):
    img = cv2.convertScaleAbs(img, beta=beta)
    return img

# sharpen image
def sharpen(img):
    kernel = np.array([ [-1, -1, -1],
                        [-1, 9.5, -1],
                        [-1, -1, -1]])
    sharpen_img = cv2.filter2D(img, -1, kernel)
    return sharpen_img

# retro style
def sepia(img):
   img_sepia = np.array(img, dtype=np.float64) # converting to float to prevent loss
   img_sepia = cv2.transform(img_sepia, np.matrix([ [0.272, 0.534, 0.131],
                                                    [0.349, 0.686, 0.168],
                                                    [0.393, 0.769, 0.189]])) # multipying image with special sepia matrix
   img_sepia[np.where(img_sepia > 255)] = 255 # normalizing values greater than 255 to 255
   img_sepia = np.array(img_sepia, dtype=np.uint8)
   return img_sepia

# pencil style
# return value: gray_img, color_img
def pencil_sketch(img):
   sk_gray, sk_color = cv2.pencilSketch(img, sigma_s=10, sigma_r=0.1, shade_factor=0.03)
   return  sk_gray, sk_color

#HDR effect
def HDR(img):
   hdr = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
   return hdr

# 鬼片
def invert(img):
   inv = cv2.bitwise_not(img)
   return inv

#summer effect
def summer(img):
   increaseLookupTable = _LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
   decreaseLookupTable = _LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
   blue_channel, green_channel,red_channel  = cv2.split(img)
   red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
   blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
   sum= cv2.merge((blue_channel, green_channel, red_channel))
   return sum

#winter effect
def winter(img):
   increaseLookupTable = _LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
   decreaseLookupTable = _LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
   blue_channel, green_channel,red_channel = cv2.split(img)
   red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
   blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
   win= cv2.merge((blue_channel, green_channel, red_channel))
   return win

# if __name__=="__main__":
def main(filter, filename):

   path = os.path.join(input_video_dir, 'filter_imgs/')
   img = cv2.imread(path + 'origin.png')
   out_name = "filtered.png"



   if filter == 1:
      cv2.imwrite(path + out_name, grayscale(img))
   elif filter == 2:
      cv2.imwrite(path + out_name, HDR(img))
   elif filter == 3:
      cv2.imwrite(path + out_name, bright(img, 60))
   elif filter == 4:
      gray, colorful = pencil_sketch(img)
      cv2.imwrite(path + out_name, gray)
   elif filter == 5:
      gray, colorful = pencil_sketch(img)
      cv2.imwrite(path + out_name, colorful)
   elif filter == 6:
      cv2.imwrite(path + out_name, sepia(img))
   elif filter == 7:
      cv2.imwrite(path + out_name, sharpen(img))
   elif filter == 8:
      cv2.imwrite(path + out_name, summer(img))
   elif filter == 9:
      cv2.imwrite(path + out_name, winter(img))
   elif filter == 10:
      cv2.imwrite(path + out_name, invert(img))


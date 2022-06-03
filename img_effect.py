import cv2
import numpy as np
from scipy.interpolate import UnivariateSpline
def LookupTable(x, y):
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
   increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
   decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
   blue_channel, green_channel,red_channel  = cv2.split(img)
   red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
   blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
   sum= cv2.merge((blue_channel, green_channel, red_channel))
   return sum

#winter effect
def winter(img):
   increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
   decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
   blue_channel, green_channel,red_channel = cv2.split(img)
   red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
   blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
   win= cv2.merge((blue_channel, green_channel, red_channel))
   return win



if __name__=="__main__":
   
   import os

   OUTPUT_DIR = '.' + os.sep + 'filter_imgs'

   img = cv2.imread(OUTPUT_DIR + os.sep + 'origin.png')
   cv2.imwrite(OUTPUT_DIR + os.sep + 'grayscale.png', grayscale(img))
   cv2.imwrite(OUTPUT_DIR + os.sep + 'brighter.png', bright(img, 60))
   cv2.imwrite(OUTPUT_DIR + os.sep + 'sharpen.png', sharpen(img))
   cv2.imwrite(OUTPUT_DIR + os.sep + 'retro.png', sepia(img))

   gray, colorful = pencil_sketch(img)
   cv2.imwrite(OUTPUT_DIR + os.sep + 'pencil_RGB.png', colorful)
   cv2.imwrite(OUTPUT_DIR + os.sep + 'pencil_gray.png', gray)

   cv2.imwrite(OUTPUT_DIR + os.sep + 'hdr.png', HDR(img))
   cv2.imwrite(OUTPUT_DIR + os.sep + 'ghost.png', invert(img))
   cv2.imwrite(OUTPUT_DIR + os.sep + 'summer.png', summer(img))
   cv2.imwrite(OUTPUT_DIR + os.sep + 'winter.png', winter(img))
import os
import matplotlib.colors as colors
import numpy as np
import math
import scipy.ndimage
import pickle
from scipy import misc
import multiprocessing as mp
import pandas as pd
import cv2

class Coin:
    #class for storing info about a single coin
    def __init__(self, img = None, rad = None, cr = None):
        '''
        img is imread image (RGB)
        rad is radially transformmed img
        '''
        self.cr = cr
        self.img = img
        self.rad = rad

    def make_from_image(self, file_name, size = (64,64)):
        #creates a new coin from filename
        #if crop is true then we attempt to find the cirlce and crop out the rest
        #if something doesn't work then it returns false
        self.img = misc.imread(file_name, mode = 'RGB')
        self.cr = _resize_image(_find_circle(self.img),size)
        self.img = misc.imresize(self.img,size)/256.0
        self.rad = _convert_to_radian(self.cr)
        self.dct = {'img': self.img, 'rad' : self.rad, 'cr':self.cr}
        return self

    def __getitem__(self, key):
        if key == 'rad':
            return self.rad
        elif key == 'cr':
            return self.cr
        else:
            return self.img

    def binarize_coin(self, filename, coin_prop, grade_lbl = -1, name_lbl = -1):
        np.append(self[coin_prop].flatten(),[grade_lbl,name_lbl]).tofile(filename)

'''
HELPER FUNCTIONS
'''
SEARCH_MIN = 1.0
SEARCH_MAX = 500.0
MIN_RADIUS = 50

def _find_circle(img):
    #Takes the image and tries to find circles in it
    #plays around with sensitivity until exactly one circle is found
    #Colors everything outside of that circle white
    #returns false if we don't find a circle
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100, param2 = SEARCH_MIN, minRadius = MIN_RADIUS)
    if circles is None:
        return False
    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100, param2 = SEARCH_MAX, minRadius = MIN_RADIUS)
    g_1 = SEARCH_MAX
    g_0 = SEARCH_MIN
    counter = 0
    while circles is None or len(circles[0])>1:
        if counter >= 20:
            raise False
        param2 = (g_1+g_0)/2
        circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100, param2 = param2, minRadius = MIN_RADIUS)
        if circles is None:
            # guess higher
            g_1 =  param2
        else:
            #guess loawer
            g_0 = param2
        counter += 1
    x, y, r = np.round(circles[0,0]).astype(int)
    cv2.circle(img, center = (x, y), radius = r+120, color= (255, 255, 255), thickness = 240)
    return img

def _resize_image(img, size = (128,128)):
    #takes an image (length x width x 3 with rgb colors)
    #and a tuple of size in pixels
    #returns the image normalized in hsv coloring
    #which cuts out whitespace and centers the image
    #returns false if something doesn't work
    if img.shape[-1] != 3:
        return False
    hsv = colors.rgb_to_hsv(img)
    w = np.nonzero((hsv[:,:,2] < 160) & (hsv[:,:,1] < 160))
    min_x, min_y = np.min(w,axis=1)
    max_x, max_y = np.max(w,axis=1)
    ims = misc.imresize(img[min_x:max_x,min_y:max_y,:],size)/256.0
    return ims

def _convert_to_radian(img):
    #transforms the image radially
    max=(2.0, img.shape[1]/(2*math.pi), 1)
    mid=(img.shape[0]/2.0,img.shape[1]/2.0,0)
    def polar_to_euclidean(pos):
        pos = (pos[0]/max[0],pos[1]/max[1],pos[2])
        nPos = (pos[0]*math.cos(pos[1]) + mid[0], pos[0]*math.sin(pos[1]) + mid[1],pos[2])
        return nPos
    rImg = scipy.ndimage.interpolation.geometric_transform(img,polar_to_euclidean, img.shape)
    return rImg

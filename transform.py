import numpy as np
import cv2

def order_points(pts):
    #Create a list that is ordered in such a way so that the first entry is the top-left corner, the second is the top-right, the third is the bottom-right and the fourth is the bottom-left.
    rect = np.zeros((4, 2), dtype = "float32")

    #the top-left will have the smallest sum and the bottom-right will have the highest sum.
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    #the difference between the points
    diff = np.diff(pts, axis = 1)

    #top-right will have the smallest diff and bottom-left will have the largest diff
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    #return the coordinates
    return rect


def four_point_transformation(image, pts):

    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    WidthA = np.sqrt(((br[0] - bl[0]) **2) + ((br[1] - bl[1]) **2))
    WidthB = np.sqrt(((tr[0] - tl[0]) **2) + ((tr[1] - tl[1]) **2))
    maxWidth = max(int(WidthA), int(WidthB))
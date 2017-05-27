import numpy as np
import cv2

if __name__=='__main__':
	img = cv2.imread('inst_000010.pgm',0)
	cv2.imshow('image',img)
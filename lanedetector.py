# -*- coding: utf-8 -*-

# Import the required libraries 
import numpy as np 
import matplotlib.pyplot as plt 
import cv2 
from google.colab.patches import cv2_imshow
import os
import math

def edgedetection(img): 
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) 
	clr = cv2.GaussianBlur(gray, (5, 5), 0) 
	Canny = cv2.Canny(clr, 50, 150) 
	return Canny

def interestregion(img): 
	heigh = img.shape[0] 
	polygon = np.array([ 
		[(200, heigh), (1100, heigh), (550, 250)] 
		]) 
	mask = np.zeros_like(img)
	
	if (len(img.shape) > 2):
		channel_count = img.shape[2]  
		ignoremask = (255,) * channel_count
	else:
		ignoremask = 255


	cv2.fillPoly(mask, polygon, ignoremask) 
	

	masked_image = cv2.bitwise_and(img, mask) 
	return masked_image

def coordinates(img, line_parameters): 
	slope, intercept = line_parameters 
	y1 = img.shape[0] 
	y2 = int(y1 * (3 / 5)) 
	x1 = int((y1 - intercept) / slope) 
	x2 = int((y2 - intercept) / slope) 
	return np.array([x1, y1, x2, y2])

def avslope(img, lines): 
	left_fit = [] 
	right_fit = [] 
	for line in lines: 
		x1, y1, x2, y2 = line.reshape(4) 
		
		parameters = np.polyfit((x1, x2), (y1, y2), 1) 
		slope = parameters[0] 
		intercept = parameters[1] 
		if slope < 0: 
			left_fit.append((slope, intercept)) 
		else: 
			right_fit.append((slope, intercept)) 
			
	left_fit_average = np.average(left_fit, axis = 0) 
	right_fit_average = np.average(right_fit, axis = 0) 
	left_line = coordinates(img, left_fit_average) 
	right_line = coordinates(img, right_fit_average) 
	return np.array([left_line, right_line])

def linedsp(img, lines): 
	line_image = np.zeros_like(img) 
	if lines is not None: 
		for x1, y1, x2, y2 in lines: 
			cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10) 
	return line_image

def driverprg(Test):
    vid_ob = cv2.VideoCapture(Test)
    while(vid_ob.isOpened()):
        frame = vid_ob.read()
        cannyimgdetect = edgedetection(frame)
        tempimg =interestregion(cannyimgdetect)
        lines = cv2.HoughLinesP(tempimg, 2, np.pi / 180, 100,
                                np.array([]), minLineLength = 40,maxLineGap = 5)
        averaged_lines = avslope(frame, lines)
        imagewithlines = linedsp(frame, averaged_lines)
        finalimage = cv2.addWeighted(frame, 0.8, imagewithlines, 1, 1)
        cv2_imshow(finalimage)
    vid_ob.release()
    cv2.destroyAllWindows()

driverprg("/content/test.mp4")

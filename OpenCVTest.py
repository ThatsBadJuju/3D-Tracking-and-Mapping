import cv2
import numpy as np
import time
import math

def init_cam():
    cam = cv2.VideoCapture(0)
    #cam.set(cv2.CAP_PROP_EXPOSURE,40)
    return cam

    # display frames of unfiltered / filtered images
def show_images(frame, mask, blue_filtered, grayscale_filtered, threshold_grayscale, blurred_result):
    #cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    cv2.imshow('frame',frame)
    #cv2.drawContours(blurred_result, contours, -1, (0, 255, 0), 3)
    # cv2.imshow('mask',mask)
    # cv2.imshow('res',blue_filtered)
    # cv2.imshow('grayscale_filtered', grayscale_filtered)
    # cv2.imshow('threshold_grayscale', threshold_grayscale)
    cv2.imshow('blurred_result', blurred_result)


def scan_ball(cam):
    check, frame = cam.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # filter by color
    turqoise_lower = np.array([90,100,25])
    turqoise_upper = np.array([135,255,255])
    mask = cv2.inRange(hsv, turqoise_lower, turqoise_upper)

    # filter by color, then grayscale, then convert to binary (pure black/white image)
    blue_filtered = cv2.bitwise_and(frame,frame, mask= mask)
    grayscale_filtered = cv2.split(blue_filtered)[2]
    blur = cv2.GaussianBlur(grayscale_filtered,(5,5),0)
    ret3, threshold_grayscale = cv2.threshold(blur,5,255,cv2.THRESH_BINARY)

    # try to smooth out the edges in the image
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(threshold_grayscale, cv2.MORPH_CLOSE, kernel)
    blurred_result = cv2.medianBlur(closing, 5)

    # return every contour in the image
    contours, hierarchy = cv2.findContours(blurred_result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # check if image has a contour at all
    try:
        largest_contour = contours[0]
        largest_area = cv2.contourArea(largest_contour)
    except:
        return

    ran_contour_loop = False
    circle_ratio = 0.5

    # iterate over every contour in image (probably really slow)
    for contour in contours:
        (x,y),radius = cv2.minEnclosingCircle(contour)
        #contour_circumference = cv2.arcLength(largest_contour, True)
        center = (int(x),int(y))
        radius = int(radius)
        area = cv2.contourArea(contour)
        if radius > 0:
            area_to_radius_ratio = float(area) / radius

        # run multiple checks to see if contour is roughly in the shape of a circle
        if x > 100 and y > 100 and radius > 30 and radius < 150 and area_to_radius_ratio > math.pi*radius*circle_ratio and area > 10:
            if largest_area < area:
                largest_contour = contour
                largest_area = area
                ran_contour_loop = True

    # if the previous loop found a circle-shaped contour
    if ran_contour_loop:
        # make a best-fit circle around the contour edges
        (x,y),radius = cv2.minEnclosingCircle(largest_contour)
        center = (int(x),int(y))
        radius = int(radius)
        print(center, radius, area_to_radius_ratio - math.pi*radius*circle_ratio)
        cv2.circle(frame,center,radius,(0,255,0),2)
        cv2.circle(blurred_result,center,radius,100,2)
        show_images(frame, mask, blue_filtered, grayscale_filtered, threshold_grayscale, blurred_result)
        return center, radius

    else:
        show_images(frame, mask, blue_filtered, grayscale_filtered, threshold_grayscale, blurred_result)
        return (-1, -1), -1


# checks for escape key pressed
def check_for_end():
    key = cv2.waitKey(1)
    time.sleep(1.0/30)
    if key == 27:
        return False
    else: return True


def stop_cam(cam):
    cam.release()
    cv2.destroyAllWindows()

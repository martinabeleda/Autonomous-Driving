# Lane detection using OpenCV on Raspberry Pi
# Author: Martin Abeleda
# Date: 19/05/2017
from picamera.array import PiRGBArray
from picamera import PiCamera
import atexit
import time
import cv2
import numpy as np
import os
cmd = 'sudo pigpiod'
os.system(cmd)

from motor_control.drive import drive_feedback, turn_decide
from motor_control.motors import motor_setup, calibrate_motors, forwards_hard, forwards_lane_follow, stop 
from lane_follow.lane_detect import lane_detect
from intersection.intersection import is_red_line

def exit_handler():
    stop()

atexit.register(exit_handler)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (800, 600)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(800, 600))
camera.vflip = True
camera.hflip = True

RED = 1
leftDuty = 120
rightDutyInit = calibrate_motors(leftDuty)
rightDuty = rightDutyInit

# wait for user to say GO
print "Waiting for you to press g"
while(1):
	inkey = raw_input()
	if inkey is "g": break
	
motor_setup()

# allow the camera to warmup
time.sleep(1)

# main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	
    try:
	
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # gaussian blur
        kernelSize = 5
        blur = cv2.GaussianBlur(image, (kernelSize,kernelSize), 0)

        # check if we are at the red line
        masked, line = is_red_line(blur)

        if line is RED:

            print "red"
            """
            # display raw input
            img = image

            # store the number of barcode lines
            barcode = read_barcode(masked)

            # move forwards to the line
            forwards_hard(leftDuty, rightDuty, distance=200)
      
            # wait for the light to turn green
            check_light()

            # execute a random turn based on barcode
            turn_decide(leftDuty, barcode)
            """
        else:
            # detect lanes in the image
            (img, angle, topDisplacement, bottomDisplacement) = lane_detect(blur)

            # execute lane following algorithm
            rightDuty = drive_feedback(angle, topDisplacement, rightDuty, leftDuty, rightDutyInit)

            forwards_lane_follow(leftDuty, rightDuty)

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

    except KeyboardInterrupt:
        pi.stop()

#imports
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

from intersection import is_red_line, read_barcode, check_light, turn_decide

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (800, 600)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(800, 600))
camera.vflip = True
camera.hflip = True

# allow the camera to warmup
time.sleep(0.1)

#defines
RED = 1
cv2.namedWindow('Main Frame', cv2.WINDOW_NORMAL)
# Main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    	# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		image = frame.array

		# gaussian blur
	    	kernelSize = 5
	    	blur = cv2.GaussianBlur(image, (kernelSize,kernelSize), 0)

		#Check to see  if red line is present - enter intersection module 
		maskedImage, line = is_red_line(blur)

		if line is RED:
			print("RED LINE!!!")

			#if at intersection 
			turnCode = read_barcode(maskedImage)
			print("Turn Code", turnCode)

			#Move forwards
			print("Move Forwards")

			#wait and exit on green light
			check_light()
			print("Light is green")

			turn_decide(turnCode)

		else:
			print("Not an intersection")
			#delay frame rate - maybs remove?
			time.sleep(0.1)


		# show the frame
		# display all data to screen 

		cv2.imshow('Main Frame', image)
                key = cv2.waitKey(1) & 0xFF

		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			cv2.destroyAllWindows()
			break





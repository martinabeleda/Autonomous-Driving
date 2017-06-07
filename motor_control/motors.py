#import RPi.GPIO as GPIO
#import os
#cmd = 'sudo pigpiod'
#os.system(cmd)
from time import sleep
import pigpio

pi = pigpio.pi()

#GPIO.setmode(GPIO.BOARD)

#motorL1A = 16
#motorL2A = 18

motorL1A = 23
motorL2A = 24

#motorR3A = 11
#motorR4A = 13

motorR3A = 17
motorR4A = 27

#motorEN = 12

motorLEN = 18
motorREN = 22

#GPIO.setup(motorEN, GPIO.OUT)
#pwm = GPIO.PWM(motorEN,100) # 100 Hz frequency

def motor_setup():
	print "Setup motor GPIO"
	pi.set_mode(motorL1A, pigpio.OUTPUT)
	pi.set_mode(motorL2A, pigpio.OUTPUT)
	pi.set_mode(motorR3A, pigpio.OUTPUT)
	pi.set_mode(motorR4A, pigpio.OUTPUT)
	pi.set_mode(motorLEN, pigpio.OUTPUT)
	pi.set_mode(motorREN, pigpio.OUTPUT)
	pi.set_PWM_frequency(motorLEN, 1000) # 100 Hz frequency
	pi.set_PWM_frequency(motorREN, 1000)
#	GPIO.setup(motorL1A, GPIO.OUT)
#	GPIO.setup(motorL2A, GPIO.OUT)
#	GPIO.setup(motorR3A, GPIO.OUT)
#	GPIO.setup(motorR4A, GPIO.OUT)
#	GPIO.setup(motorEN, GPIO.OUT)

def calibrate_motors(dcL, dcR):
	MAX_DUTY = 255
	MIN_DUTY = 48
	

        print "Adjust right duty <p> <i>. When finished <q>" 
	
	while 1:
		forwards_lane_follow(dcL,dcR)
		inkey = raw_input()
		if inkey is "i" and dcR < MAX_DUTY:
			dcR += 0.1
			print "right duty %f" % (dcR)
		elif inkey is "p" and dcR > MIN_DUTY:
			dcR -= 0.1
			print "right duty %f" % (dcR)
		elif inkey is "q": break
	return dcR

def forwards_hard(dcL,dcR,distance):
	print "Forwards"
	SPEED = 39 # mm/s
#	GPIO.output(motorL1A, GPIO.HIGH)
#	GPIO.output(motorL2A, GPIO.LOW)
#	GPIO.output(motorR3A, GPIO.HIGH)
#	GPIO.output(motorR4A, GPIO.LOW)
	pi.write(motorL1A, True)
	pi.write(motorL2A, False)
	pi.write(motorR3A, True)
	pi.write(motorR4A, False)
	pi.set_PWM_dutycycle(motorLEN,dcL)
	pi.set_PWM_dutycycle(motorREN,dcR)
	time = distance/SPEED
	sleep(time)
	
def forwards_lane_follow(dcL,dcR):
	pi.write(motorL1A, True)
	pi.write(motorL2A, False)
	pi.write(motorR3A, True)
	pi.write(motorR4A, False)
	pi.set_PWM_dutycycle(motorLEN,dcL)
	pi.set_PWM_dutycycle(motorREN,dcR)
	# maybe set sleep time ay

def reverse(distance):
	# fix
	print "Reverse"
	SPEED = 39 # mm/s
	pi.write(motorL1A, False)
	pi.write(motorL2A, True)
	pi.write(motorR3A, False)
	pi.write(motorR4A, True)
	pi.set_PWM_dutycycle(motorLEN,dc)
	dcR = calibrate_motors(dc)
	pi.set_PWM_dutycycle(motorREN,dcR)
	print dcR
	time = distance/SPEED
	sleep(time)

def turn_clockwise(angle):
	print "Turn clockwise by", angle, "degrees"
	TURN_RATE = 100
	pi.set_PWM_dutycycle(motorREN,0)
	pi.write(motorL1A, True)
	pi.write(motorL2A, False)
	pi.set_PWM_dutycycle(motorLEN,255)
	time = angle/TURN_RATE
	sleep(time)
	
def turn_anti_clockwise(angle):
	print "Turn anti-clockwise by", angle, "degrees"
	TURN_RATE = 500
	pi.set_PWM_dutycycle(motorLEN,0)
	pi.write(motorR3A, True)
	pi.write(motorR4A, False)
	pi.set_PWM_dutycycle(motorREN,255)
	time = angle/TURN_RATE
	sleep(time)

def left_turn(dcL,dcR):
	"Left turn"
	forwards_hard(dcL,dcR,210)
	turn_anti_clockwise(90)
	forwards_hard(dcL,dcR,210)

def right_turn():
	"Left turn"
	forwards_hard(dcL,dcR,210)
	self.turn_clockwise(90)
	forwards_hard(dcL,dcR,210)

def straight(leftDuty, rightDuty):
    print "straight"
    pi.write(motorL1A, True)
    pi.write(motorL2A, False)
    pi.write(motorR3A, True)
    pi.write(motorR4A, False)
    pi.set_PWM_dutycycle(motorLEN,leftDuty)
    pi.set_PWM_dutycycle(motorREN,rightDuty)

def left(rightDuty):
    print "left"
    pi.write(motorL1A, True)
    pi.write(motorL2A, False)
    pi.set_PWM_dutycycle(motorLEN,0)
    pi.set_PWM_dutycycle(motorREN,60)

def right(leftDuty):
    print "right"
    pi.write(motorR3A, True)
    pi.write(motorR4A, False)
    pi.set_PWM_dutycycle(motorLEN,60)
    pi.set_PWM_dutycycle(motorREN,0)


def stop():
	print "Stop"
	#pwm.stop()
	pi.set_PWM_dutycycle(motorLEN, 0)
	pi.set_PWM_dutycycle(motorREN, 0)

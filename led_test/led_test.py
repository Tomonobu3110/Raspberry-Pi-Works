# LED Test

import RPi.GPIO as GPIO
import time

COUNT = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)

for _ in xrange(COUNT):
	GPIO.output(3, True)
	time.sleep(1)
	GPIO.output(3, False)
	time.sleep(1)

GPIO.cleanup()


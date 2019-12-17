# -*- coding: utf-8 -*-
import io
import time
import picamera
import cv2 as cv
import numpy as np

import RPi.GPIO as GPIO

import httplib
import requests

# counter
face_count = 0
eye_count  = 0

# LED setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)


while True:
	stream = io.BytesIO()
	with picamera.PiCamera() as camera:

		# resolution
		camera.resolution = (640, 480)

		# take photo
		camera.start_preview()
		time.sleep(1)
		camera.capture(stream, format='jpeg')

		# RGB to GRAY
		data = np.fromstring(stream.getvalue(), dtype=np.uint8)
		img = cv.imdecode(data, 1)
		grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

		# face detection
		face_cascade = cv.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
		facerect = face_cascade.detectMultiScale(grayimg, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
		print "face rectangle"
		print(facerect)
		if len(facerect) > 0:
			face_count += 1
			for rect in facerect:
				cv.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0, 255), thickness=3)

			# Post to WebAPI
			url_items = 'https://powerful-plateau-47488.herokuapp.com/faces/create'
			proxies = {
				'http': 'http://proxy.kanto.sony.co.jp:10080',
				'https': 'http://proxy.kanto.sony.co.jp:10080'
			}
			payload = { 'pi_id': '1', 'number': len(facerect) }
			r = requests.post(url_items, data = payload, proxies = proxies)
			# r = requests.post(url_items, data = payload)
			print (r.text)

		else:
			face_count = 0

		# LED
		if 10 < face_count:
			GPIO.output(3, True)
		else:
			GPIO.output(3, False)

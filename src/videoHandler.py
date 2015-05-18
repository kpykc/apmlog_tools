try:
	import time
	import numpy as np
	import cv2
	import rospy
	import rosbag
	from sensor_msgs.msg import Image
	from cv_bridge import CvBridge, CvBridgeError
except ImportError:
	print "Can't load ROS dependencies"

class videoFileHandler:
	'''Handle video file data'''
	def __init__(self):
		name = 'none'
		self.showFrames = False

	def setVerbose(self, showFrames):
		self.showFrames = showFrames

	def setName(self, name):
		self.name = name
		self.topic = self.name+'/image_raw'

	def setSource(self, srcname):
		self.srcname = srcname
		self.capture = cv2.VideoCapture(self.srcname)

		if self.capture.isOpened() == True:
			print("Input file is opened. Ready to perform convertion.")
		else:
			print("ERROR: Unable to open given video file!")

	def convertData(self, bagfile):
		seq = 0
		bridge = CvBridge()
		while(True):
			# Capture frame-by-frame
			ret, cvImage = self.capture.read()
			try:
				imageMsg = bridge.cv2_to_imgmsg(cvImage, "bgr8") # TODO: format spec as cmd option?
			except CvBridgeError, e:
				print e

			# creating ros message
			seq = seq + 1

			imageMsg.header.seq = seq
			# TODO: temporary hack, time sync/source is needed
			imageMsg.header.stamp =  rospy.Time.from_sec(time.time()) 
			# TODO: try
			# коли запустився скрипт, взяти поточний TS системи за перший TS video і перший TS IMU
			# наступні TS IMU рахуємо так: next_ts = prev_ts + imu[current] - imu[prev];

			# write message to bag file
			bagfile.write(self.topic, imageMsg, imageMsg.header.stamp)

			# this is not so important for conversion
			if self.showFrames == True:
				cv2.imshow('frame', cvImage)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break

		# Our operations on the frame come here
		# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# # Display the resulting frame
		# cv2.imshow('frame',gray)
		# if cv2.waitKey(1) & 0xFF == ord('q'):
		# 	break
		# When everything done, release the capture
		self.capture.release()
		cv2.destroyAllWindows()


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
	def __init__(self, bagfile):
		name = 'none'
		self.showFrames = False
		self.bag = bagfile

	def __del__(self):
		self.capture.release()
		cv2.destroyAllWindows()

	def setVerbose(self, showFrames):
		self.showFrames = showFrames

	def setName(self, name):
		self.name = name
		self.topic = self.name+'/image_raw'

	def setInitialStamp(self, initial_stamp=0.0, fps=30.0 ):
		self.stamp = initial_stamp
		self.initial_stamp = initial_stamp
		self.fps = fps

	def setSource(self, srcname):
		self.srcname = srcname
		self.capture = cv2.VideoCapture(self.srcname)

		if self.capture.isOpened() == True:
			print("Input file is opened. Ready to perform convertion.")
		else:
			print("ERROR: Unable to open given video file!")

		self.bridge = CvBridge()

		self.seq = 0

	def getTimestamp(self):
		return self.stamp

	def convertData(self):
		
		# Capture frame-by-frame
		ret, cvImage = self.capture.read()
		try:
			msg = self.bridge.cv2_to_imgmsg(cvImage, "bgr8") # TODO: format spec as cmd option?
		except CvBridgeError, e:
			print e

		# creating ros message
		self.seq = self.seq + 1

		msg.header.seq = self.seq
		# TODO: temporary hack, time sync/source is needed
		self.stamp = self.initial_stamp + self.seq*(1.0/self.fps)

		msg.header.stamp = rospy.Time.from_sec(self.stamp)
		# rospy.Time.from_sec(time.time()) 
		# TODO: try
		# at script start, take a current TS (system time) as first TS of the video and first TS of IMU
		# next TS IMU calculate as: next_ts = prev_ts + imu[current] - imu[prev];

		#print "publish image", msg.header.stamp
		# write message to bag file
		self.bag.write(self.topic, msg, msg.header.stamp)

		# this is not so important for conversion
		# if self.showFrames == True:
		# 	cv2.imshow('frame', cvImage)
		# 	if cv2.waitKey(1) & 0xFF == ord('q'):
		# 		break

		# Our operations on the frame come here
		# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# # Display the resulting frame
		# cv2.imshow('frame',gray)
		# if cv2.waitKey(1) & 0xFF == ord('q'):
		# 	break
		# When everything done, release the capture
		



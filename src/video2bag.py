#!/usr/bin/env python

import os, sys
import argparse
import time

import numpy as np
import cv2


# add ros stuff
import rospy
import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


topic = 'camera/image_raw'

try:
	import rospy
	import rosbag
	from apmlog_tools.msg import AHR2
except ImportError:
	print "Can't load ROS dependencies"


class CameraHandler:
	'''Handle camera data'''
	def __init__(self):
		name = 'none'
		self.showFrames = False

	def setVerbose(self, showFrames):
		self.showFrames = showFrames

	def setName(self, name):
		self.name = name
		self.capture = cv2.VideoCapture(self.name)

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

			# write message to bag file
			bagfile.write(topic, imageMsg, imageMsg.header.stamp)

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

def main():

	parser = argparse.ArgumentParser(description='Convert APM Dataflash log to ROSBag format')
	parser.add_argument('logfile', type=argparse.FileType('r'), help='path to Dataflash log file (or - for stdin)')
	parser.add_argument('-s', '--sync_time', metavar='', action='store_const', const=True, help='sync video to logfile') # TODO: add sync time code
	args = parser.parse_args()

	

	cam = CameraHandler()

	# starting conversion
	bag = rosbag.Bag('output_video.bag', 'w')

	cam.setName(args.logfile.name)
	cam.setVerbose(False)
	print("Converting...")
	cam.convertData(bag)

	# handlers finished
	bag.close()
	print("Convesion finished.")


if __name__ == "__main__":
    main()
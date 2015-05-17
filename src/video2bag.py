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

def genVideoBag(capture):
	with rosbag.Bag('output_video.bag', 'w') as outbag:
		seq = 0
		bridge = CvBridge()
		while(True):
			# Capture frame-by-frame
			ret, cvImage = capture.read()
			imageMsg = bridge.cv2_to_imgmsg(cvImage, "bgr8") # TODO: format spec as cmd option?

			cv2.imshow('frame', cvImage)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			seq = seq + 1
			# imuMsg = Imu()
			imageMsg.header.seq = seq
			imageMsg.header.stamp =  rospy.Time.from_sec(time.time()) # TODO: temporary hack

			outbag.write(topic, imageMsg, imageMsg.header.stamp)

	# Our operations on the frame come here
	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# # Display the resulting frame
	# cv2.imshow('frame',gray)
	# if cv2.waitKey(1) & 0xFF == ord('q'):
	# 	break


def main():

	parser = argparse.ArgumentParser(description='Convert APM Dataflash log to ROSBag format')
	parser.add_argument('logfile', type=argparse.FileType('r'), help='path to Dataflash log file (or - for stdin)')
	parser.add_argument('-s', '--sync_time', metavar='', action='store_const', const=True, help='sync video to logfile') # TODO: add sync time code
	args = parser.parse_args()

	cap = cv2.VideoCapture(args.logfile.name)

	if cap.isOpened() == True:
		genVideoBag(cap)

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

	print()


if __name__ == "__main__":
    main()
#!/usr/bin/env python

import os, sys
import argparse
import time

# from https://github.com/diydrones/ardupilot/tree/master/Tools/LogAnalyzer
import DataflashLog

# add ros stuff
import rospy
import rosbag
from sensor_msgs.msg import Imu


def genIMUBagFile(logdata):

	imu1 = logdata.channels["IMU"]
	imu1_timems = imu1["TimeMS"].listData
	imu1_accx = imu1["AccX"].listData
	imu1_accy = imu1["AccY"].listData
	imu1_accz = imu1["AccZ"].listData

	imu1_gyrx = imu1["GyrX"].listData
	imu1_gyry = imu1["GyrY"].listData
	imu1_gyrz = imu1["GyrZ"].listData

	topic = logdata.vehicleType+'/imu'

	with rosbag.Bag('output.bag', 'w') as outbag:
		for msgid in range(0,len(imu1_timems)):
			imuMsg = Imu()
			imuMsg.header.seq = imu1_timems[msgid][0]
			imuMsg.header.stamp =  rospy.Time.from_sec(float(long(imu1_timems[msgid][1])/1e6)) # TODO: check if conversion is correct 
			imuMsg.angular_velocity.x = imu1_gyrx[msgid][1]
			imuMsg.angular_velocity.y = imu1_gyry[msgid][1]
			imuMsg.angular_velocity.z = imu1_gyrz[msgid][1]
			imuMsg.linear_acceleration.x = imu1_accx[msgid][1]
			imuMsg.linear_acceleration.y = imu1_accy[msgid][1]
			imuMsg.linear_acceleration.z = imu1_accz[msgid][1]
			outbag.write(topic, imuMsg, imuMsg.header.stamp)


def main():

	parser = argparse.ArgumentParser(description='Convert APM Dataflash log to ROSBag format')
	parser.add_argument('logfile', type=argparse.FileType('r'), help='path to Dataflash log file (or - for stdin)')
	parser.add_argument('-f', '--format',  metavar='', type=str, action='store', choices=['bin','log','auto'], default='auto', help='log file format: \'bin\',\'log\' or \'auto\'')
	parser.add_argument('-s', '--skip_bad', metavar='', action='store_const', const=True, help='skip over corrupt dataflash lines')
	parser.add_argument('-p', '--profile', metavar='', action='store_const', const=True, help='output performance profiling data')
	parser.add_argument('-e', '--empty',  metavar='', action='store_const', const=True, help='run an initial check for an empty log')
	args = parser.parse_args()

	# test DataflashLog reading 1
	startTime = time.time()
	logdata = DataflashLog.DataflashLog()
	logdata.read(args.logfile.name, format=args.format, ignoreBadlines=args.skip_bad)
	endTime = time.time()

	if args.profile:
		print "Log file read time: %.2f seconds" % (endTime-startTime)

	# check for empty log if requested
	if args.empty:
		emptyErr = DataflashLog.DataflashLogHelper.isLogEmpty(logdata)
		if emptyErr:
			sys.stderr.write("Empty log file: %s, %s" % (logdata.filename, emptyErr))
			sys.exit(1)


	genIMUBagFile(logdata)


if __name__ == "__main__":
    main()
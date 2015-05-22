#!/usr/bin/env python

import os, sys
import argparse
import time

# from https://github.com/diydrones/ardupilot/tree/master/Tools/LogAnalyzer
import DataflashLog

# add ros stuff
try:
	import rospy
	import rosbag
except ImportError:
	print "Can't load ROS dependencies"

try:
	from imuHandler import IMUHandler
	from ahrHandler import AHRHandler
	from attHandler import ATTHandler
	from magHandler import MAGHandler
	from baroHandler import BAROHandler
	from powrHandler import POWRHandler
	from gpsHandler import GPSHandler
	from radHandler import RADHandler
	from currHandler import CURRHandler
	from videoHandler import videoFileHandler
	# from handlers.imuHandler import IMUHandler
	# from handlers.ahrHandler import AHRHandler
except ImportError:
	print "Can't load handlers"

def main():

	parser = argparse.ArgumentParser(description='Convert APM Dataflash log to ROSBag format')
	parser.add_argument('logfile', type=argparse.FileType('r'), help='path to Dataflash log file (or - for stdin)')
	parser.add_argument('-v','--video', type=argparse.FileType('r'), help='path to video file (or - for stdin)')
	parser.add_argument('-t', '--time_sync', metavar='', action='store_const', const=True, help='sync video to logfile') # TODO: add sync time code
	parser.add_argument('-f', '--format',  metavar='', type=str, action='store', choices=['bin','log','auto'], default='auto', help='log file format: \'bin\',\'log\' or \'auto\'')
	parser.add_argument('-s', '--skip_bad', metavar='', action='store_const', const=True, help='skip over corrupt dataflash lines')
	parser.add_argument('-p', '--profile', metavar='', action='store_const', const=True, help='output performance profiling data')
	parser.add_argument('-e', '--empty',  metavar='', action='store_const', const=True, help='run an initial check for an empty log')
	args = parser.parse_args()

	# test DataflashLog reading 1
	print("Loading log file...")
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

	# starting conversion
	print("Converting...")
	bag = rosbag.Bag('test.bag', 'w')

	# load all handlers and call them

	channelNames = logdata.channels.keys()
	types=['IMU','IMU2','AHR2','ATT','MAG','MAG2','BARO','POWR','CURR','RAD','GPS']
	# import threading
	# for channel in logdata.channels.keys():
	# 	#print channel
	# 	hnd = getattr(importlib.import_module("handlers."+channel+"Handler"), channel+"Handler")
	# 	# handlers path e.g.: ${PKG}/src/handlers/ATTHandler.py
	# 	t = threading.Thread(target=hnd, args = (q,u)) # set correct args
	# 	t.daemon = True
	#  	t.start()

	#import importlib
	#atth = importlib.import_module("attHandler")
	#atth = (importlib.import_module("attHandler")).ATTHandler
	#In [1]: import importlib
	#In [2]: ah = importlib.import_module("handlers.attHandler")
	#In [3]: atth = ah.ATTHandler()
	#cn = logdata.channels.keys()
	#ah = importlib.import_module("handlers."+cn[2]+"Handler")
	#mymethod = getattr(importlib.import_module("abc.def.ghi.jkl.myfile"), "mymethod")
	##hnd = getattr(importlib.import_module("handlers."+cn[2]+"Handler"), cn[2]+"Handler")

	# IMU
	print("IMU...")
	imu_h = IMUHandler()

	imu_h.setName("IMU")
	imu_h.convertData(logdata, bag)

	imu_h.setName("IMU2")
	imu_h.convertData(logdata, bag)

	# AHR
	print("AHR...")
	ahr_h = AHRHandler()

	ahr_h.setName("AHR2")
	ahr_h.convertData(logdata, bag)

	# ATT
	print("ATT...")
	att_h = ATTHandler()

	att_h.setName("ATT")
	att_h.convertData(logdata, bag)

	# MAG
	print("MAG...")
	mag_h = MAGHandler()

	mag_h.setName("MAG")
	mag_h.convertData(logdata, bag)

	mag_h.setName("MAG2")
	mag_h.convertData(logdata, bag)

	# BARO
	print("BARO...")
	baro_h = BAROHandler()

	baro_h.setName("BARO")
	baro_h.convertData(logdata, bag)

	# POWR
	print("POWR...")
	powr_h = POWRHandler()

	powr_h.setName("POWR")
	powr_h.convertData(logdata, bag)

	# CURR
	print("CURR...")
	CURR_h = CURRHandler()

	CURR_h.setName("CURR")
	CURR_h.convertData(logdata, bag)

	# GPS
	print("GPS...")
	GPS_h = GPSHandler()

	GPS_h.setName("GPS")
	GPS_h.convertData(logdata, bag)

	# RAD
	print("RAD...")
	RAD_h = RADHandler()

	RAD_h.setName("RAD")
	RAD_h.convertData(logdata, bag)

	# camera
	if args.video != None:
		print("Converting video...")
		cam = videoFileHandler()
		cam.setName('camera')
		cam.setSource(args.video.name)
		cam.setVerbose(False)
		print("Converting...")
		cam.convertData(bag)

	# handlers finished
	bag.close()
	print("Convesion finished.")


if __name__ == "__main__":
    main()
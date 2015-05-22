#!/usr/bin/env python

import os, sys
import argparse
import time
import math

# from https://github.com/diydrones/ardupilot/tree/master/Tools/LogAnalyzer
import DataflashLog

# add ros stuff
try:
	import rospy
	import rosbag
except ImportError:
	print "Can't load ROS dependencies"

try:
	from genericHandler import GenericHandler
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
	parser.add_argument('-v','--video', type=argparse.FileType('r'), help='path to video file')
	parser.add_argument('-t', '--time_sync', default='0', type=float)
	parser.add_argument('--fps', default='30', type=float)
	# parser.add_argument('-t', '--time_sync', metavar='', action='store_const', const=True, help='sync video to logfile') # TODO: add sync time code
	parser.add_argument('-f', '--format',  metavar='', type=str, action='store', choices=['bin','log','auto'], default='auto', help='log file format: \'bin\',\'log\' or \'auto\'')
	parser.add_argument('-s', '--skip_bad', metavar='', action='store_const', const=True, help='skip over corrupt dataflash lines')
	parser.add_argument('-p', '--profile', metavar='', action='store_const', const=True, help='output performance profiling data')
	parser.add_argument('-e', '--empty',  metavar='', action='store_const', const=True, help='run an initial check for an empty log')
	args = parser.parse_args()

	# test DataflashLog reading 1
	print "Loading log file: ", args.logfile.name
	print "Delay of first video frame is set to: ", args.time_sync, " seconds."
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

	handlers = []
	for msgType in types:
		if msgType in types:
			#print msgType
			if (msgType == 'IMU') or (msgType == 'IMU2'):
				handlers.append( IMUHandler(msgType, logdata, bag) )
			if (msgType == 'MAG') or (msgType == 'MAG2'):
				handlers.append( MAGHandler(msgType, logdata, bag) )
			if (msgType == 'AHR2'):
				handlers.append( AHRHandler(msgType, logdata, bag) )
			if (msgType == 'ATT'):
				handlers.append( ATTHandler(msgType, logdata, bag) )
			if (msgType == 'BARO'):
				handlers.append( BAROHandler(msgType, logdata, bag) )
			if (msgType == 'POWR'):
				handlers.append( POWRHandler(msgType, logdata, bag) )
			if (msgType == 'CURR'):
				handlers.append( CURRHandler(msgType, logdata, bag) )
			if (msgType == 'RAD'):
				handlers.append( RADHandler(msgType, logdata, bag) )
			if (msgType == 'GPS'):
				handlers.append( GPSHandler(msgType, logdata, bag) )

	# camera
	if args.video != None:
		print("WARNING! Adding uncompressed video frames to bag. Be carefull the file can grow rapidly over few Gb.")
		cam = videoFileHandler(bag)
		cam.setName(logdata.vehicleType+'/camera')
		cam.setSource(args.video.name)
		cam.setVerbose(False)
		#cam.setInitialStamp(args.time_sync, args.fps)
		#handlers.append(cam)
		#print("Converting...")
		#cam.convertData(bag)

	earliest_timestamp = True
	# next_timestamp = 0.0
	while(True):
		timestamps = [] # current set of timestamps from spawned handlers
		if not handlers:
  			print "No handles exist anymore"
  			break

  		# remove inactive handlers
		for h in handlers: 
			if h.getTimestamp() is None:
				handlers.remove(h)

		# collect timestamps from currently active handlers
		for h in handlers: 
			timestamps.append( h.getTimestamp() )

		if handlers: # request handler with earliest message to save it
			# print len(handlers), len(ts)
			next_stamp = min(timestamps)
			handlers[timestamps.index(next_stamp)].convertData()
			#print help(min(timestamps))

			if earliest_timestamp is True:
				earliest_timestamp = False # save earliest timestamp for video syncronisation with log data
				cam.setInitialStamp( args.time_sync+next_stamp , args.fps)
				handlers.append(cam)

			# if fabs( next_timestamp - cam.getTimestamp() ) <= (1.0/30.0)/2.0:
			# 	print "Publish image"
			# 	cam.convertData()
			# if not ts:
			# 	handlers[ts.index(min(ts))].convertData()
			# else:
			# 	print "No timestamps?"
			# 	break


	# import threading
	# for channel in logdata.channels.keys():
	# 	#print channel
	# 	hnd = getattr(importlib.import_module("handlers."+channel+"Handler"), channel+"Handler")
	# 	# handlers path e.g.: ${PKG}/src/handlers/ATTHandler.py
	# 	t = threading.Thread(target=hnd, args = (q,u)) # set correct args
	# 	t.daemon = True
	#  	t.start()


	# handlers finished
	bag.close()
	print("Convesion finished.")


if __name__ == "__main__":
    main()
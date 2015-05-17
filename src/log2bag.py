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

from apmlog_tools.msg import AHR2

#AHR2Msg = AHR2()

# class TestSuite(object):
#     '''registers test classes, loading using a basic plugin architecture, and can run them all in one run() operation'''
#     def __init__(self):
#         self.tests   = []
#         self.logfile = None
#         self.logdata = None  
#         # dynamically load in Test subclasses from the 'tests' folder
#         # to prevent one being loaded, move it out of that folder, or set that test's .enable attribute to False
#         dirName = os.path.dirname(os.path.abspath(__file__))
#         testScripts = glob.glob(dirName + '/tests/*.py')
#         testClasses = []
#         for script in testScripts:
#             m = imp.load_source("m",script)
#             for name, obj in inspect.getmembers(m, inspect.isclass):
#                 if name not in testClasses and inspect.getsourcefile(obj) == script:
#                     testClasses.append(name)
#                     self.tests.append(obj())

#         # and here's an example of explicitly loading a Test class if you wanted to do that
#         # m = imp.load_source("m", dirName + '/tests/TestBadParams.py')
#         # self.tests.append(m.TestBadParams())

#     def run(self, logdata, verbose):
#         '''run all registered tests in a single call, gathering execution timing info'''
#         self.logdata = logdata
#         self.logfile = logdata.filename
#         for test in self.tests:
#             # run each test in turn, gathering timing info
#             if test.enable:
#                 startTime = time.time()
#                 test.run(self.logdata, verbose)  # RUN THE TEST
#                 endTime = time.time()
#                 test.execTime = 1000 * (endTime-startTime)

from imuHandler import IMUHandler
from ahrHandler import AHRHandler
# from handlers.imuHandler import IMUHandler
# from handlers.ahrHandler import AHRHandler

def main():

	parser = argparse.ArgumentParser(description='Convert APM Dataflash log to ROSBag format')
	parser.add_argument('logfile', type=argparse.FileType('r'), help='path to Dataflash log file (or - for stdin)')
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
	hndl = IMUHandler()

	hndl.setName("IMU")
	hndl.convertData(logdata, bag)
	hndl.setName("IMU2")
	hndl.convertData(logdata, bag)

	# handlers finished
	bag.close()
	print("Convesion finished.")


if __name__ == "__main__":
    main()
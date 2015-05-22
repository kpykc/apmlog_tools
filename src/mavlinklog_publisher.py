#!/usr/bin/env python

import sys, time, os, struct, json
from pymavlink import mavutil
#from pymavlink.rotmat import Vector3

src = mavutil.mavlink_connection('2.bin', dialect="pixhawk", planner_format=False, robust_parsing=True, notimestamps=True)
sink = mavutil.mavlink_connection('udp::5000', dialect="pixhawk", input=False, notimestamps=False)
#sink = mavutil.mavlink_connection('udp::14555', input=False)

while(True):
	msg = src.recv_msg()
	#msg = src.recv_match(type=['RAW_IMU','SCALED_IMU2','IMU','IMU2','PARM','PARAM_VALUE','GPS'])
	if msg is None:
		print("End of log?")
		break
		
	timestamp = getattr(msg, '_timestamp')
	now = time.strftime("%H:%M:%S", time.localtime(timestamp))
	if msg.get_type() == "GPS_RAW":
		print msg.lat
	if msg.get_type() == "ATTITUDE":
		print msg.roll
	#if msg.get_type() == "RAW_IMU":
	#	#mag = Vector3(msg.xmag, msg.ymag, msg.zmag)
	#	print now, "RAW_IMU"
	#elif msg.get_type() == "IMU":
	#	#mag = Vector3(msg.xmag, msg.ymag, msg.zmag)
	#	print now, "IMU"
	#else:
	#	print now, msg.get_type()

	print now, msg.get_type()
	#data = msg.to_dict()
	#data = msg.__dict__
	#outMsg = {"meta": {"msgId": "unk", "type": msg.get_type(), "timestamp": timestamp}, "data": data}

	# Now print out this object with stringified properly.
	#print(json.dumps(outMsg))
	
	#print("%s", now)
	sink.write(msg.get_msgbuf())
	



try:
	import rospy
	import rosbag
	from apmlog_tools.msg import GPS
except ImportError:
	print "Can't load ROS dependencies"


class GPSHandler:
	'''GPS channel handler'''
	def __init__(self):
		name = 'none'
		
	def setName(self, name):
		self.name = name

	def convertData(self, logdata, bagfile):

		self.topic = logdata.vehicleType+'/'+self.name

		channel = logdata.channels[self.name]
		timestamp_ms = channel["TimeMS"].listData
		
		# TODO: there are iterators, use them?
		for msgid in range(0,len(timestamp_ms)):

			msg = GPS()

			msg.header.seq = timestamp_ms[msgid][0]
			msg.header.stamp = rospy.Time.from_sec(float(long(timestamp_ms[msgid][1])/1e6)) # TODO: check if conversion is correct

			msg.Alt = channel["Alt"].listData[msgid][1]
			msg.GCrs = channel["GCrs"].listData[msgid][1]
			msg.HDop = channel["HDop"].listData[msgid][1]
			msg.Lat = channel["Lat"].listData[msgid][1]
			msg.Lng = channel["Lng"].listData[msgid][1]
			msg.NSats = channel["NSats"].listData[msgid][1]
			msg.RelAlt = channel["RelAlt"].listData[msgid][1]
			msg.Spd = channel["Spd"].listData[msgid][1]
			msg.Status = channel["Status"].listData[msgid][1]
			msg.T = channel["T"].listData[msgid][1]
			msg.VZ = channel["VZ"].listData[msgid][1]
			msg.Week = channel["Week"].listData[msgid][1]

			bagfile.write(self.topic, msg, msg.header.stamp)


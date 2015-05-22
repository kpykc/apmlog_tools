
try:
	import rospy
	import rosbag
	from apmlog_tools.msg import GPS
except ImportError:
	print "Can't load ROS dependencies"


class GPSHandler:
	'''GPS channel handler'''
	def __init__(self, name, logdata, bagfile):
		self.name = name
		self.logdata = logdata
		self.bag = bagfile

		self.msgid = 0
		self.topic = logdata.vehicleType+'/'+self.name

		self.channel = logdata.channels[self.name]
		self.timestamp_ms = self.channel["TimeMS"].listData

		self.stamp = rospy.Time.from_sec(float(long(self.timestamp_ms[self.msgid][1])/1e6)) # TODO: check if conversion is correct 
		self.msgs_len = len(self.timestamp_ms)

	def getTimestamp(self):
		if self.msgid < self.msgs_len:
			self.stamp = rospy.Time.from_sec(float(long(self.timestamp_ms[self.msgid][1])/1e6)) # TODO: check if conversion is correct 
			return self.stamp
		else:
			return None

	def convertData(self):

		if self.msgid < self.msgs_len:

			msg = GPS()

			msg.header.seq = self.timestamp_ms[self.msgid][0]
			msg.header.stamp = self.stamp

			msg.Alt = self.channel["Alt"].listData[self.msgid][1]
			msg.GCrs = self.channel["GCrs"].listData[self.msgid][1]
			msg.HDop = self.channel["HDop"].listData[self.msgid][1]
			msg.Lat = self.channel["Lat"].listData[self.msgid][1]
			msg.Lng = self.channel["Lng"].listData[self.msgid][1]
			msg.NSats = self.channel["NSats"].listData[self.msgid][1]
			msg.RelAlt = self.channel["RelAlt"].listData[self.msgid][1]
			msg.Spd = self.channel["Spd"].listData[self.msgid][1]
			msg.Status = self.channel["Status"].listData[self.msgid][1]
			msg.T = self.channel["T"].listData[self.msgid][1]
			msg.VZ = self.channel["VZ"].listData[self.msgid][1]
			msg.Week = self.channel["Week"].listData[self.msgid][1]

			self.bag.write(self.topic, msg, msg.header.stamp)
			self.msgid = self.msgid + 1



try:
	import rospy
	import rosbag
	from apmlog_tools.msg import CURR
except ImportError:
	print "Can't load ROS dependencies"


class CURRHandler:
	'''CURR channel handler'''
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

			msg = CURR()

			msg.header.seq = self.timestamp_ms[self.msgid][0]
			msg.header.stamp = self.stamp

			msg.Curr = self.channel["Curr"].listData[self.msgid][1]
			msg.CurrTot = self.channel["CurrTot"].listData[self.msgid][1]
			msg.ThrInt = self.channel["ThrInt"].listData[self.msgid][1]
			msg.ThrOut = self.channel["ThrOut"].listData[self.msgid][1]
			msg.Vcc = self.channel["Vcc"].listData[self.msgid][1]
			msg.Volt = self.channel["Volt"].listData[self.msgid][1]

			self.bag.write(self.topic, msg, msg.header.stamp)
			self.msgid = self.msgid + 1


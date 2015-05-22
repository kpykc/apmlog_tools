
try:
	import rospy
	import rosbag
	from apmlog_tools.msg import RAD
	from genericHandler import GenericHandler
except ImportError:
	print "Can't load ROS dependencies"


class RADHandler(GenericHandler):
	'''RAD channel handler'''

	def convertData(self):

		if self.msgid < self.msgs_len:

			msg = RAD()

			msg.header.seq = self.timestamp_ms[self.msgid][0]
			msg.header.stamp = rospy.Time.from_sec(self.stamp)

			msg.Fixed = self.channel["Fixed"].listData[self.msgid][1]
			msg.Noise = self.channel["Noise"].listData[self.msgid][1]
			msg.RSSI = self.channel["RSSI"].listData[self.msgid][1]
			msg.RemNoise = self.channel["RemNoise"].listData[self.msgid][1]
			msg.RemRSSI = self.channel["RemRSSI"].listData[self.msgid][1]
			msg.RxErrors = self.channel["RxErrors"].listData[self.msgid][1]
			msg.TxBuf = self.channel["TxBuf"].listData[self.msgid][1]

			self.bag.write(self.topic, msg, msg.header.stamp)
			self.msgid = self.msgid + 1


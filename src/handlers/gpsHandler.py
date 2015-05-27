
try:
	import rospy
	import rosbag
	from apmlog_tools.msg import GPS
	from genericHandler import GenericHandler
except ImportError:
	print "Can't load ROS dependencies"


class GPSHandler(GenericHandler):
	'''GPS channel handler'''
	def convertData(self):

		if self.msgid < self.msgs_len:

			msg = GPS()

			msg.header.seq = self.timestamp_ms[self.msgid][0]
			msg.header.stamp = rospy.Time.from_sec(self.stamp)

			msg.Alt = self.getMsgValue("Alt")
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


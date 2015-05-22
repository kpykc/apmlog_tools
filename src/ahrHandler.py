try:
	import rospy
	import rosbag
	from apmlog_tools.msg import AHR
	from genericHandler import GenericHandler
except ImportError:
	print "Can't load ROS dependencies"

class AHRHandler(GenericHandler):
	'''AHR Handler'''

	def convertData(self):

		if self.msgid < self.msgs_len:

			msg = AHR()
			msg.header.seq = self.timestamp_ms[self.msgid][0]
			msg.header.stamp = rospy.Time.from_sec(self.stamp)

			msg.Alt = self.channel["Alt"].listData[self.msgid][1]
			msg.Lat = self.channel["Lat"].listData[self.msgid][1]
			msg.Lng = self.channel["Lng"].listData[self.msgid][1]
			msg.Roll = self.channel["Pitch"].listData[self.msgid][1]
			msg.Pitch = self.channel["Roll"].listData[self.msgid][1]
			msg.Yaw = self.channel["Yaw"].listData[self.msgid][1]

			self.bag.write(self.topic, msg, msg.header.stamp)
			self.msgid = self.msgid + 1


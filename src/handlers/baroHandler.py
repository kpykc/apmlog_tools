
try:
	import rospy
	import rosbag
	from apmlog_tools.msg import BARO
	from genericHandler import GenericHandler
except ImportError:
	print "Can't load ROS dependencies"


class BAROHandler(GenericHandler):
	'''BARO channel handler'''

	def convertData(self):

		if self.msgid < self.msgs_len:

			msg = BARO()

			msg.header.seq = self.timestamp_ms[self.msgid][0]
			msg.header.stamp = rospy.Time.from_sec(self.stamp)

			msg.Alt = self.channel["Alt"].listData[self.msgid][1]
			msg.CRt = self.channel["CRt"].listData[self.msgid][1]
			msg.Press = self.channel["Press"].listData[self.msgid][1]
			msg.Temp = self.channel["Temp"].listData[self.msgid][1]

			self.bag.write(self.topic, msg, msg.header.stamp)
			self.msgid = self.msgid + 1


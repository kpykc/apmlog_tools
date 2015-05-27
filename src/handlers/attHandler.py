try:
	import rospy
	import rosbag
	from apmlog_tools.msg import ATT
	from genericHandler import GenericHandler
except ImportError:
	print "Can't load ROS dependencies"


class ATTHandler(GenericHandler):
	'''ATT handler'''
	def convertData(self):

		if self.msgid < self.msgs_len:
			msg = ATT()

			msg.header.seq = self.timestamp_ms[self.msgid][0]
			msg.header.stamp = rospy.Time.from_sec(self.stamp)

			msg.DesRoll = self.channel["DesRoll"].listData[self.msgid][1]
			msg.DesYaw = self.channel["DesYaw"].listData[self.msgid][1]
			msg.ErrRP = self.channel["ErrRP"].listData[self.msgid][1]
			msg.ErrYaw = self.channel["ErrYaw"].listData[self.msgid][1]
			msg.Pitch = self.channel["Pitch"].listData[self.msgid][1]
			msg.Roll = self.channel["Roll"].listData[self.msgid][1]
			msg.Yaw = self.channel["Yaw"].listData[self.msgid][1]

			self.bag.write(self.topic, msg, msg.header.stamp)
			self.msgid = self.msgid + 1

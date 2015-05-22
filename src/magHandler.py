

try:
	import rospy
	import rosbag
	from apmlog_tools.msg import MAG
	from genericHandler import GenericHandler
except ImportError:
	print "Can't load ROS dependencies"


class MAGHandler(GenericHandler):
	'''MAG channel handler'''

	def convertData(self):

		if self.msgid < self.msgs_len:

			msg = MAG()

			msg.header.seq = self.timestamp_ms[self.msgid][0]
			msg.header.stamp = self.stamp

			msg.MOfsX = self.channel["MOfsX"].listData[self.msgid][1]
			msg.MOfsY = self.channel["MOfsY"].listData[self.msgid][1]
			msg.MOfsZ = self.channel["MOfsZ"].listData[self.msgid][1]
			msg.MagX = self.channel["MagX"].listData[self.msgid][1]
			msg.MagY = self.channel["MagY"].listData[self.msgid][1]
			msg.MagZ = self.channel["MagZ"].listData[self.msgid][1]
			msg.MagX = self.channel["OfsX"].listData[self.msgid][1]
			msg.MagY = self.channel["OfsY"].listData[self.msgid][1]
			msg.MagZ = self.channel["OfsZ"].listData[self.msgid][1]

			self.bag.write(self.topic, msg, msg.header.stamp)
			self.msgid = self.msgid + 1


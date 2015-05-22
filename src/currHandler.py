
try:
	import rospy
	import rosbag
	from apmlog_tools.msg import CURR
	from genericHandler import GenericHandler
except ImportError:
	print "Can't load ROS dependencies"


class CURRHandler(GenericHandler):
	'''CURR channel handler'''

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


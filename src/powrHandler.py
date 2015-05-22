
try:
	import rospy
	import rosbag
	from apmlog_tools.msg import POWR
	from genericHandler import GenericHandler
except ImportError:
	print "Can't load ROS dependencies"


class POWRHandler(GenericHandler):
	'''POWR channel handler'''
	def convertData(self):

		if self.msgid < self.msgs_len:

			msg = POWR()

			msg.header.seq = self.timestamp_ms[self.msgid][0]
			msg.header.stamp = self.stamp

			msg.VServo = self.channel["VServo"].listData[self.msgid][1]
			msg.Vcc = self.channel["Vcc"].listData[self.msgid][1]

			self.bag.write(self.topic, msg, msg.header.stamp)
			self.msgid = self.msgid + 1


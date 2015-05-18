try:
	import rospy
	import rosbag
	from apmlog_tools.msg import ATT
except ImportError:
	print "Can't load ROS dependencies"


class ATTHandler:
	'''registers test classes, loading using a basic plugin architecture, and can run them all in one run() operation'''
	def __init__(self):
		name = 'none'
		
	def setName(self, name):
		self.name = name

	def convertData(self, logdata, bagfile):

		self.topic = logdata.vehicleType+'/'+self.name

		att = logdata.channels[self.name]
		timestamp_ms = att["TimeMS"].listData
		
		# TODO: there are iterators, use them?
		for msgid in range(0,len(timestamp_ms)):

			attMsg = ATT()

			attMsg.header.seq = timestamp_ms[msgid][0]
			self.stamp = rospy.Time.from_sec(float(long(timestamp_ms[msgid][1])/1e6)) # TODO: check if conversion is correct
			attMsg.header.stamp = self.stamp

			attMsg.DesRoll = att["DesRoll"].listData[msgid][1]
			attMsg.DesYaw = att["DesYaw"].listData[msgid][1]
			attMsg.ErrRP = att["ErrRP"].listData[msgid][1]
			attMsg.ErrYaw = att["ErrYaw"].listData[msgid][1]
			attMsg.Pitch = att["Pitch"].listData[msgid][1]
			attMsg.Roll = att["Roll"].listData[msgid][1]
			attMsg.Yaw = att["Yaw"].listData[msgid][1]

			bagfile.write(self.topic, attMsg, self.stamp)


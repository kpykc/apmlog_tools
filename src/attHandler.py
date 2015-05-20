try:
	import rospy
	import rosbag
	from apmlog_tools.msg import ATT
except ImportError:
	print "Can't load ROS dependencies"


class ATTHandler:
	'''ATT handler'''
	def __init__(self):
		name = 'none'
		
	def setName(self, name):
		self.name = name

	def convertData(self, logdata, bagfile):

		self.topic = logdata.vehicleType+'/'+self.name

		channel = logdata.channels[self.name]
		timestamp_ms = channel["TimeMS"].listData
		
		# TODO: there are iterators, use them?
		for msgid in range(0,len(timestamp_ms)):

			msg = ATT()

			msg.header.seq = timestamp_ms[msgid][0]
			msg.header.stamp = rospy.Time.from_sec(float(long(timestamp_ms[msgid][1])/1e6)) # TODO: check if conversion is correct

			msg.DesRoll = channel["DesRoll"].listData[msgid][1]
			msg.DesYaw = channel["DesYaw"].listData[msgid][1]
			msg.ErrRP = channel["ErrRP"].listData[msgid][1]
			msg.ErrYaw = channel["ErrYaw"].listData[msgid][1]
			msg.Pitch = channel["Pitch"].listData[msgid][1]
			msg.Roll = channel["Roll"].listData[msgid][1]
			msg.Yaw = channel["Yaw"].listData[msgid][1]

			bagfile.write(self.topic, msg, msg.header.stamp)


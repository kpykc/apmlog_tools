try:
	import rospy
	import rosbag
	from apmlog_tools.msg import AHR
except ImportError:
	print "Can't load ROS dependencies"


class AHRHandler:
	'''registers test classes, loading using a basic plugin architecture, and can run them all in one run() operation'''
	def __init__(self):
		name = 'none'
		
	def setName(self, name):
		self.name = name

	def convertData(self, logdata, bagfile):

		self.topic = logdata.vehicleType+'/'+self.name

		ahr = logdata.channels[self.name]
		timestamp_ms = ahr["TimeMS"].listData
		ahr_alt = ahr["Alt"].listData
		ahr_lat = ahr["Lat"].listData
		ahr_lng = ahr["Lng"].listData
		ahr_pitch = ahr["Pitch"].listData
		ahr_roll = ahr["Roll"].listData
		ahr_yaw = ahr["Yaw"].listData
		
		# TODO: there are iterators, use them?
		for msgid in range(0,len(timestamp_ms)):

			ahrMsg = AHR()
			ahrMsg.header.seq = timestamp_ms[msgid][0]
			self.stamp = rospy.Time.from_sec(float(long(timestamp_ms[msgid][1])/1e6)) # TODO: check if conversion is correct
			ahrMsg.header.stamp = self.stamp
			ahrMsg.Alt = ahr_alt[msgid][1]
			ahrMsg.Lat = ahr_lat[msgid][1]
			ahrMsg.Lng = ahr_lng[msgid][1]
			ahrMsg.Roll = ahr_pitch[msgid][1]
			ahrMsg.Pitch = ahr_roll[msgid][1]
			ahrMsg.Yaw = ahr_yaw[msgid][1]

			bagfile.write(self.topic, ahrMsg, self.stamp)


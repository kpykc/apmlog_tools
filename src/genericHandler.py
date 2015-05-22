try:
	import rospy
	import rosbag
except ImportError:
	print "Can't load ROS dependencies"

class GenericHandler:
	'''Generic channel handler'''
	def __init__(self, name, logdata, bagfile):
		self.name = name
		self.logdata = logdata
		self.bag = bagfile

		self.msgid = 0
		self.topic = logdata.vehicleType+'/'+self.name

		self.channel = logdata.channels[self.name]
		self.timestamp_ms = self.channel["TimeMS"].listData

		self.stamp = rospy.Time.from_sec(float(long(self.timestamp_ms[self.msgid][1])/1e6)) # TODO: check if conversion is correct 
		self.msgs_len = len(self.timestamp_ms)

	def getTimestamp(self):
		if self.msgid < self.msgs_len:
			#self.stamp = rospy.Time.from_sec(float(long(self.timestamp_ms[self.msgid][1])/1e6)) # TODO: check if conversion is correct 
			self.stamp = float(long(self.timestamp_ms[self.msgid][1])/1e6)
			return self.stamp
		else:
			return None

	def getMsgValue(self, fieldName):
		return self.channel[fieldName].listData[self.msgid][1]

	def convertData(self):

		print "Define conversion routine"

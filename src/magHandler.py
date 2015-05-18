

try:
	import rospy
	import rosbag
	from apmlog_tools.msg import MAG
except ImportError:
	print "Can't load ROS dependencies"


class MAGHandler:
	'''MAG channel handler'''
	def __init__(self):
		name = 'none'
		
	def setName(self, name):
		self.name = name

	def convertData(self, logdata, bagfile):

		self.topic = logdata.vehicleType+'/'+self.name

		mag = logdata.channels[self.name]
		timestamp_ms = mag["TimeMS"].listData
		
		# TODO: there are iterators, use them?
		for msgid in range(0,len(timestamp_ms)):

			magMsg = MAG()

			magMsg.header.seq = timestamp_ms[msgid][0]
			self.stamp = rospy.Time.from_sec(float(long(timestamp_ms[msgid][1])/1e6)) # TODO: check if conversion is correct
			magMsg.header.stamp = self.stamp

			magMsg.MOfsX = mag["MOfsX"].listData[msgid][1]
			magMsg.MOfsY = mag["MOfsY"].listData[msgid][1]
			magMsg.MOfsZ = mag["MOfsZ"].listData[msgid][1]
			magMsg.MagX = mag["MagX"].listData[msgid][1]
			magMsg.MagY = mag["MagY"].listData[msgid][1]
			magMsg.MagZ = mag["MagZ"].listData[msgid][1]
			magMsg.MagX = mag["OfsX"].listData[msgid][1]
			magMsg.MagY = mag["OfsY"].listData[msgid][1]
			magMsg.MagZ = mag["OfsZ"].listData[msgid][1]

			bagfile.write(self.topic, magMsg, self.stamp)




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

		channel = logdata.channels[self.name]
		timestamp_ms = channel["TimeMS"].listData
		
		# TODO: there are iterators, use them?
		for msgid in range(0,len(timestamp_ms)):

			msg = MAG()

			msg.header.seq = timestamp_ms[msgid][0]
			msg.header.stamp = rospy.Time.from_sec(float(long(timestamp_ms[msgid][1])/1e6)) # TODO: check if conversion is correct

			msg.MOfsX = channel["MOfsX"].listData[msgid][1]
			msg.MOfsY = channel["MOfsY"].listData[msgid][1]
			msg.MOfsZ = channel["MOfsZ"].listData[msgid][1]
			msg.MagX = channel["MagX"].listData[msgid][1]
			msg.MagY = channel["MagY"].listData[msgid][1]
			msg.MagZ = channel["MagZ"].listData[msgid][1]
			msg.MagX = channel["OfsX"].listData[msgid][1]
			msg.MagY = channel["OfsY"].listData[msgid][1]
			msg.MagZ = channel["OfsZ"].listData[msgid][1]

			bagfile.write(self.topic, msg, msg.header.stamp)


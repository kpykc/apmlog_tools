
try:
	import rospy
	import rosbag
	from apmlog_tools.msg import RAD
except ImportError:
	print "Can't load ROS dependencies"


class RADHandler:
	'''RAD channel handler'''
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

			msg = RAD()

			msg.header.seq = timestamp_ms[msgid][0]
			msg.header.stamp = rospy.Time.from_sec(float(long(timestamp_ms[msgid][1])/1e6)) # TODO: check if conversion is correct

			msg.Fixed = channel["Fixed"].listData[msgid][1]
			msg.Noise = channel["Noise"].listData[msgid][1]
			msg.RSSI = channel["RSSI"].listData[msgid][1]
			msg.RemNoise = channel["RemNoise"].listData[msgid][1]
			msg.RemRSSI = channel["RemRSSI"].listData[msgid][1]
			msg.RxErrors = channel["RxErrors"].listData[msgid][1]
			msg.TxBuf = channel["TxBuf"].listData[msgid][1]

			bagfile.write(self.topic, msg, msg.header.stamp)


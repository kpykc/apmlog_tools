

try:
	import rospy
	import rosbag
	from apmlog_tools.msg import BARO
except ImportError:
	print "Can't load ROS dependencies"


class BAROHandler:
	'''BARO channel handler'''
	def __init__(self):
		name = 'none'
		
	def setName(self, name):
		self.name = name

	def convertData(self, logdata, bagfile):

		self.topic = logdata.vehicleType+'/'+self.name

		baro = logdata.channels[self.name]
		timestamp_ms = baro["TimeMS"].listData
		
		# TODO: there are iterators, use them?
		for msgid in range(0,len(timestamp_ms)):

			baroMsg = BARO()

			baroMsg.header.seq = timestamp_ms[msgid][0]
			self.stamp = rospy.Time.from_sec(float(long(timestamp_ms[msgid][1])/1e6)) # TODO: check if conversion is correct
			baroMsg.header.stamp = self.stamp

			baroMsg.Alt = baro["Alt"].listData[msgid][1]
			baroMsg.CRt = baro["CRt"].listData[msgid][1]
			baroMsg.Press = baro["Press"].listData[msgid][1]
			baroMsg.Temp = baro["Temp"].listData[msgid][1]

			bagfile.write(self.topic, baroMsg, self.stamp)




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

		channel = logdata.channels[self.name]
		timestamp_ms = channel["TimeMS"].listData
		
		# TODO: there are iterators, use them?
		for msgid in range(0,len(timestamp_ms)):

			msg = BARO()

			msg.header.seq = timestamp_ms[msgid][0]
			self.stamp = rospy.Time.from_sec(float(long(timestamp_ms[msgid][1])/1e6)) # TODO: check if conversion is correct
			msg.header.stamp = self.stamp

			msg.Alt = channel["Alt"].listData[msgid][1]
			msg.CRt = channel["CRt"].listData[msgid][1]
			msg.Press = channel["Press"].listData[msgid][1]
			msg.Temp = channel["Temp"].listData[msgid][1]

			bagfile.write(self.topic, msg, self.stamp)


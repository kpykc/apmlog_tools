
try:
	import rospy
	import rosbag
	from apmlog_tools.msg import CURR
except ImportError:
	print "Can't load ROS dependencies"


class CURRHandler:
	'''CURR channel handler'''
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

			msg = CURR()

			msg.header.seq = timestamp_ms[msgid][0]
			msg.header.stamp = rospy.Time.from_sec(float(long(timestamp_ms[msgid][1])/1e6)) # TODO: check if conversion is correct

			msg.Curr = channel["Curr"].listData[msgid][1]
			msg.CurrTot = channel["CurrTot"].listData[msgid][1]
			msg.ThrInt = channel["ThrInt"].listData[msgid][1]
			msg.ThrOut = channel["ThrOut"].listData[msgid][1]
			msg.Vcc = channel["Vcc"].listData[msgid][1]
			msg.Volt = channel["Volt"].listData[msgid][1]

			bagfile.write(self.topic, msg, msg.header.stamp)


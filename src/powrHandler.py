
try:
	import rospy
	import rosbag
	from apmlog_tools.msg import POWR
except ImportError:
	print "Can't load ROS dependencies"


class POWRHandler:
	'''POWR channel handler'''
	def __init__(self):
		name = 'none'
		
	def setName(self, name):
		self.name = name

	def convertData(self, logdata, bagfile):

		self.topic = logdata.vehicleType+'/'+self.name

		powr = logdata.channels[self.name]
		timestamp_ms = powr["TimeMS"].listData
		
		# TODO: there are iterators, use them?
		for msgid in range(0,len(timestamp_ms)):

			powrMsg = POWR()

			powrMsg.header.seq = timestamp_ms[msgid][0]
			self.stamp = rospy.Time.from_sec(float(long(timestamp_ms[msgid][1])/1e6)) # TODO: check if conversion is correct
			powrMsg.header.stamp = self.stamp

			powrMsg.VServo = powr["VServo"].listData[msgid][1]
			powrMsg.Vcc = powr["Vcc"].listData[msgid][1]

			bagfile.write(self.topic, powrMsg, self.stamp)


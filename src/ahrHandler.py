try:
	import rospy
	import rosbag
	from apmlog_tools.msg import AHR2
except ImportError:
	print "Can't load ROS dependencies"


class AHRHandler:
	'''registers test classes, loading using a basic plugin architecture, and can run them all in one run() operation'''
	def __init__(self):
		name = 'none'
		
	def setName(self, name):
		self.name = name

	def convertData(self, logdata, bagfile):

		imu1 = logdata.channels[self.name]
		imu1_timems = imu1["TimeMS"].listData
		imu1_accx = imu1["AccX"].listData
		imu1_accy = imu1["AccY"].listData
		imu1_accz = imu1["AccZ"].listData

		imu1_gyrx = imu1["GyrX"].listData
		imu1_gyry = imu1["GyrY"].listData
		imu1_gyrz = imu1["GyrZ"].listData

		topic = logdata.vehicleType+'/'+self.name

		for msgid in range(0,len(imu1_timems)):

			imuMsg = self.Imu()
			imuMsg.header.seq = imu1_timems[msgid][0]
			imuMsg.header.stamp =  rospy.Time.from_sec(float(long(imu1_timems[msgid][1])/1e6)) # TODO: check if conversion is correct 
			imuMsg.angular_velocity.x = imu1_gyrx[msgid][1]
			imuMsg.angular_velocity.y = imu1_gyry[msgid][1]
			imuMsg.angular_velocity.z = imu1_gyrz[msgid][1]
			imuMsg.linear_acceleration.x = imu1_accx[msgid][1]
			imuMsg.linear_acceleration.y = imu1_accy[msgid][1]
			imuMsg.linear_acceleration.z = imu1_accz[msgid][1]
			# Header header
			# float32 Lat # [deg]?
			# float32 Lng
			# float32 Pitch
			# float32 Roll
			# float32 Yaw
			# TODO: This is not enough for ROS IMU msg, add cov matrices and calculate orientation

			bagfile.write(topic, imuMsg, imuMsg.header.stamp)


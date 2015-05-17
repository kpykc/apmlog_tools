try:
	import rospy
	import rosbag
except ImportError:
	print "Can't load ROS dependencies"


class IMUHandler:
	'''registers test classes, loading using a basic plugin architecture, and can run them all in one run() operation'''
	def __init__(self):
		try:
			from sensor_msgs.msg import Imu
		except ImportError:
			self.Imu = None
		else:
			self.Imu = Imu
		
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
			# TODO: This is not enough for ROS IMU msg, add cov matrices and calculate orientation

			# simple complementary filter for orientation
			#pitch += ((float)omega_x / GYROSCOPE_SENSITIVITY) * dt; // Angle around the X-axis
    		#roll -= ((float)omega_y / GYROSCOPE_SENSITIVITY) * dt; // Angle around the Y-axis
			#// Turning around the X axis results in a vector on the Y-axis
			#pitchAcc = atan2(a_x, ( sqrt(pow(a_y,2.0) + pow(a_z,2.0)) )) * 180.0 / M_PI;
			#pitch = pitch * 0.98 + pitchAcc * 0.02;

			#// Turning around the Y axis results in a vector on the X-axis
			#rollAcc = atan2(a_y, (sqrt(pow(a_x,2.0) + pow(a_z,2.0)) )) * 180.0 / M_PI;
			#roll = roll * 0.98 + rollAcc * 0.02;

			#yaw =  ((float)omega_z / GYROSCOPE_SENSITIVITY) * dt;

			#rpy_msg.vector.x = roll;
			#rpy_msg.vector.y = pitch;
			#rpy_msg.vector.z = yaw;
			#rpy_msg.header.seq = seq;
			#rpy_msg.header.frame_id = frame_id_imu_link;
			#rpy_msg.header.stamp = time;

			#orientation.setRPY(roll, pitch, yaw);
			#tf::quaternionTFToMsg(orientation, orientation_msg);

			#//build imu_msg
			#imu_msg->header.frame_id = frame_id_imu_link;
			#//imu_msg.orientation_covariance
			#for (sensor_msgs::Imu::_orientation_covariance_type::iterator it = imu_msg->orientation_covariance.begin();
			#    it != imu_msg->orientation_covariance.end(); ++it)
			#  *it = 0;
			#//imu_msg.angular_velocity_covariance
			#for (sensor_msgs::Imu::_angular_velocity_covariance_type::iterator it =
			#    imu_msg->angular_velocity_covariance.begin(); it != imu_msg->angular_velocity_covariance.end(); ++it)
			#  *it = 0;
			#//imu_msg.linear_acceleration_covariance
			#for (sensor_msgs::Imu::_linear_acceleration_covariance_type::iterator it =
			#    imu_msg->linear_acceleration_covariance.begin(); it != imu_msg->linear_acceleration_covariance.end();
			#    ++it)
			#  *it = 0;

			#imu_transform.setRotation(orientation);
			imuMsg.angular_velocity_covariance = [0, 0, 0, 0, 0, 0, 0, 0, 1]
			imuMsg.orientation_covariance = [0.001, 0, 0, 0, 0.001, 0, 0, 0, 0.1]
			#self.orientation += imu.angular_velocity.z * (imu.header.stamp - self.prev_time).to_sec()
			#self.prev_time = imu.header.stamp
			#(imu.orientation.x, imu.orientation.y, imu.orientation.z, imu.orientation.w) = Rotation.RotZ(self.orientation).GetQuaternion()
			bagfile.write(topic, imuMsg, imuMsg.header.stamp)


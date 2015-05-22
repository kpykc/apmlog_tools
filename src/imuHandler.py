try:
	import rospy
	import rosbag
	from sensor_msgs.msg import Imu
	from genericHandler import GenericHandler
except ImportError:
	print "Can't load ROS dependencies"


class IMUHandler(GenericHandler):
	'''IMU handler'''
	def convertData(self):

		if self.msgid < self.msgs_len:

			msg = Imu()

			msg.header.seq = self.timestamp_ms[self.msgid][0]
			msg.header.stamp = self.stamp 

			msg.angular_velocity.x = self.channel["GyrX"].listData[self.msgid][1]
			msg.angular_velocity.y = self.channel["GyrY"].listData[self.msgid][1]
			msg.angular_velocity.z = self.channel["GyrZ"].listData[self.msgid][1]
			msg.linear_acceleration.x = self.channel["AccX"].listData[self.msgid][1]
			msg.linear_acceleration.y = self.channel["AccY"].listData[self.msgid][1]
			msg.linear_acceleration.z = self.channel["AccZ"].listData[self.msgid][1]
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

			#orientation.setRPY(roll, pitch, yaw);
			#tf::quaternionTFToMsg(orientation, orientation_msg);

			#//build imu_msg
			#imu_msg->header.frame_id = frame_id_imu_link;
			#imu_transform.setRotation(orientation);
			msg.angular_velocity_covariance = [0, 0, 0, 0, 0, 0, 0, 0, 1]
			msg.orientation_covariance = [0.001, 0, 0, 0, 0.001, 0, 0, 0, 0.1]
			#self.orientation += imu.angular_velocity.z * (imu.header.stamp - self.prev_time).to_sec()
			#self.prev_time = imu.header.stamp
			#(imu.orientation.x, imu.orientation.y, imu.orientation.z, imu.orientation.w) = Rotation.RotZ(self.orientation).GetQuaternion()
			self.bag.write(self.topic, msg, msg.header.stamp)
			self.msgid = self.msgid + 1
			#print (self.msgs_len - self.msgid), " msgs left"


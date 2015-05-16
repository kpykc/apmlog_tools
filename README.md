# APM log tools


# Fetching class for dealing with logs 

If you want say update class from `ardupilot` source:

	wget https://raw.githubusercontent.com/diydrones/ardupilot/master/Tools/LogAnalyzer/DataflashLog.py

# running

	0/LogAnalyzer> python log2bag.py 
	0/LogAnalyzer> rosbag info output.bag 
	path:        output.bag
	version:     2.0
	duration:    0.1s
	start:       Jan 01 1970 01:00:00.01 (0.01)
	end:         Jan 01 1970 01:00:00.08 (0.08)
	size:        12.3 MB
	messages:    34756
	compression: none [16/16 chunks]
	types:       sensor_msgs/Imu [6a62c6daae103f4ff57a132d6f95cec2]
	topics:      /imu   34756 msgs    : sensor_msgs/Imu


# running in ros

~~~{.bash}
	rosrun apmlog_tools log2bag.py src/sandbox/apmlog_tools/sample/2.bin
~~~

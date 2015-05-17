# APM log tools


# Fetching class for dealing with logs 

If you want say update class from `ardupilot` source:

	wget https://raw.githubusercontent.com/diydrones/ardupilot/master/Tools/LogAnalyzer/DataflashLog.py

# running in ros

~~~{.bash}
	rosrun apmlog_tools log2bag.py src/sandbox/apmlog_tools/sample/2.bin

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
~~~


Usage: `log2bag.py [-h] [-f] [-s] [-p] [-e] logfile`

Convert APM Dataflash log to ROSBag format

positional arguments:
  logfile         path to Dataflash log file (or - for stdin)

optional arguments:
  -h, --help      show this help message and exit
  -f , --format   log file format: 'bin','log' or 'auto'
  -s, --skip_bad  skip over corrupt dataflash lines
  -p, --profile   output performance profiling data
  -e, --empty     run an initial check for an empty log


~~~{.bash}
	rosrun apmlog_tools  video2bag.py video_and_telemetry/DCIM/100HDDVR/REC_0001.MOV

	0/apmlog_tools> rosbag info output_video.bag 
	path:        output_video.bag
	version:     2.0
	duration:    1:33s (93s)
	start:       May 17 2015 13:56:53.35 (1431863813.35)
	end:         May 17 2015 13:58:26.44 (1431863906.44)
	size:        2.0 GB
	messages:    350
	compression: none [350/350 chunks]
	types:       sensor_msgs/Image [060021388200f6f0f447d0fcd9c64743]
	topics:      camera/image_raw   350 msgs    : sensor_msgs/Image
~~~~

# misc

	git archive -o apmlog_tools-latest.zip HEAD


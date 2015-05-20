# APM log tools


# Fetching class for dealing with logs 

If you want say update class from `ardupilot` source:

	wget https://raw.githubusercontent.com/diydrones/ardupilot/master/Tools/LogAnalyzer/DataflashLog.py


# Notes on installation

**Deps**: `python`, `opencv` python wrappers, `numpy`, `rospy`, `cvbridge`, `rosbag`, etc.

~~~{.xml}
	<build_depend>sensor_msgs</build_depend>
	<build_depend>geometry_msgs</build_depend>
	<build_depend>nav_msgs</build_depend>
	<build_depend>std_msgs</build_depend>
	<build_depend>rospy</build_depend>
	<build_depend>message_generation</build_depend>
	<run_depend>rospy</run_depend>
	<run_depend>sensor_msgs</run_depend>
	<run_depend>geometry_msgs</run_depend>
	<run_depend>nav_msgs</run_depend>
	<run_depend>std_msgs</run_depend>
	<run_depend>message_runtime</run_depend>
~~~

# Running in ROS environment

**Important**: do not forget to `source /opt/ros/setup.bash` (path depends on your install), and `source devel/setup.bash` in your catkin workspace. 


Usage: `log2bag.py [-h] [-f] [-s] [-p] [-e] logfile`:

~~~
positional arguments:

  logfile         path to Dataflash log file (or - for stdin)

optional arguments:

  -h, --help      show this help message and exit
  -f , --format   log file format: 'bin','log' or 'auto'
  -s, --skip_bad  skip over corrupt dataflash lines
  -p, --profile   output performance profiling data
  -e, --empty     run an initial check for an empty log
~~~

~~~{.bash}
	rosrun apmlog_tools log2bag.py src/sandbox/apmlog_tools/sample/2.bin

	Loading log file...
	Converting...
	IMU...
	AHR...
	ATT...
	MAG...
	BARO...
	POWR...
	CURR...
	GPS...
	RAD...
	Convesion finished.
	0/src> rosbag info test.bag 
	path:        test.bag
	version:     2.0
	duration:    6:27s (387s)
	start:       Jan 01 1970 01:00:00.07 (0.07)
	end:         Jan 01 1970 01:06:27.68 (387.68)
	size:        35.2 MB
	messages:    180136
	compression: none [45/45 chunks]
	types:       apmlog_tools/AHR  [9d012171d83de74acfa0a894540f0986]
	             apmlog_tools/ATT  [f4f099f3e1046a4bcb57cb9d663574ae]
	             apmlog_tools/BARO [297cf70f0c733e3d5f4861d33d57bc18]
	             apmlog_tools/CURR [44a9fcd586b2ac9da1c02b9fb035dced]
	             apmlog_tools/GPS  [c9e6f5d789bd12e12f9e207f2162f8fb]
	             apmlog_tools/MAG  [103fdaa79527522ab1187d8e39f937bd]
	             apmlog_tools/POWR [5263f14fb2dbb65f2b01248a7305d537]
	             apmlog_tools/RAD  [e5ef9ca46853629e0794b8064dbeb8da]
	             sensor_msgs/Imu   [6a62c6daae103f4ff57a132d6f95cec2]
	topics:      ArduCopter/AHR2   41707 msgs    : apmlog_tools/AHR 
	             ArduCopter/ATT    41709 msgs    : apmlog_tools/ATT 
	             ArduCopter/BARO    6953 msgs    : apmlog_tools/BARO
	             ArduCopter/CURR     695 msgs    : apmlog_tools/CURR
	             ArduCopter/GPS     3573 msgs    : apmlog_tools/GPS 
	             ArduCopter/IMU    34756 msgs    : sensor_msgs/Imu  
	             ArduCopter/IMU2   34754 msgs    : sensor_msgs/Imu  
	             ArduCopter/MAG     6953 msgs    : apmlog_tools/MAG 
	             ArduCopter/MAG2    6953 msgs    : apmlog_tools/MAG 
	             ArduCopter/POWR     695 msgs    : apmlog_tools/POWR
	             ArduCopter/RAD     1388 msgs    : apmlog_tools/RAD
~~~


Converting video to ROSBag file:

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

~~~
rosrun apmlog_tools log2bag.py sample/2.bin -v ~/Downloads/pixhack/video_and_telemetry/DCIM/100HDDVR/REC_0001.MOV
~~~

# misc

**TODO**:  Note that types in the streams `*.msg` are chosen by voluntaristic decision. They may be wrong.


	git archive -o apmlog_tools-latest.zip HEAD


Just note:

	# class TestSuite(object):
	#     '''registers test classes, loading using a basic plugin architecture, and can run them all in one run() operation'''
	#     def __init__(self):
	#         self.tests   = []
	#         self.logfile = None
	#         self.logdata = None  
	#         # dynamically load in Test subclasses from the 'tests' folder
	#         # to prevent one being loaded, move it out of that folder, or set that test's .enable attribute to False
	#         dirName = os.path.dirname(os.path.abspath(__file__))
	#         testScripts = glob.glob(dirName + '/tests/*.py')
	#         testClasses = []
	#         for script in testScripts:
	#             m = imp.load_source("m",script)
	#             for name, obj in inspect.getmembers(m, inspect.isclass):
	#                 if name not in testClasses and inspect.getsourcefile(obj) == script:
	#                     testClasses.append(name)
	#                     self.tests.append(obj())

	#         # and here's an example of explicitly loading a Test class if you wanted to do that
	#         # m = imp.load_source("m", dirName + '/tests/TestBadParams.py')
	#         # self.tests.append(m.TestBadParams())

	#     def run(self, logdata, verbose):
	#         '''run all registered tests in a single call, gathering execution timing info'''
	#         self.logdata = logdata
	#         self.logfile = logdata.filename
	#         for test in self.tests:
	#             # run each test in turn, gathering timing info
	#             if test.enable:
	#                 startTime = time.time()
	#                 test.run(self.logdata, verbose)  # RUN THE TEST
	#                 endTime = time.time()
	#                 test.execTime = 1000 * (endTime-startTime)

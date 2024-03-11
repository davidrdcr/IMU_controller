
# Installation

1. Clone the package into the **src** directory of your workspace
	
	    git clone https://github.com/davidrdcr/imu_controller.git
	    
2. Compile the package

		 colcon build
		
3. Source the setup file to set up the environment

		echo "source ~/robot_ws/install/setup.sh" >> ~/.bashrc
		source ~/.bashrc
	
4. Install pip and add the directory to path

		sudo apt install python3-pip
		`export PATH=$PATH:/home/<user>/.local/bin`

5. Install the required dependencies 

	    pip install pyserial modbus_tk transforms3d
		
6. Check the port where the device is located and grant permissions if needed.

		ls /dev/ttyUSB*
		sudo chmod 777 /dev/ttyUSB0

# Usage
 
1. Run the package node

		ros2 run imu_controller imu_node

2. Alternatively, launch the package using the launch file.

		ros2 launch imu_controller _imu_launch.py

3. View the data by echoing the topic.

		ros2 topic echo /imu

## Visualizing in Rviz2

1. Install imu-tools if not already installed

		sudo apt-get install ros-<DISTRO>-imu-tools
		
2. Open Rviz2

		rviz2

3. Open the rviz configuration 

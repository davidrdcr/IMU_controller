
# Installation

1. Clone the package into the **src** directory of your workspace
	
	    git clone https://github.com/davidrdcr/imu_controller.git
	    
2. Compile the package

		 colcon build --symlink-install
		
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

Note:

 - It is crucial to verify that the IMU has the same address (0x50) and is connected to the same serial port (/dev/ttyUSB0) as in the example. If not, it is necessary to modify the corresponding file in the imu_controller directory and rebuild the package. 
 - The IMU address can be changed using the WitMotion software, which is available for download from their official [website](https://drive.google.com/drive/u/0/folders/1TLutidDBd_tDg5aTXgjvkz63OVt5_8ZZ). 
 
1. Launch the command you need.

| Command                                           | Function                                                                                           |
|---------------------------------------------------|----------------------------------------------------------------------------------------------------|
| `ros2 launch imu_controller _imu_node_launch.py`      | Publishes IMU data (with address `0x50` and serial port `/dev/ttyUSB0` by default) to the topic `imu`|
| `ros2 launch imu_controller _two_imu_nodes_launch.py`  | Publishes data from IMUs with addresses `0x50` and `0x51` to topics `imu1` and `imu2` respectively. Utilizes the default serial port `/dev/ttyUSB0`|
| `ros2 launch imu_controller _test_imu_node_launch.py` | Controls motor speed based on IMU pitch. This command employs the [vesc package](https://github.com/f1tenth/vesc)|

2. View the data by echoing a topic.

		ros2 topic echo /imu

## Visualizing in Rviz2

1. Install imu-tools if not already installed

		sudo apt-get install ros-<DISTRO>-imu-tools
		
2. Launch the command. If no visualization appears, manually open the file located at `imu_controller/config/config2.rviz` in rviz2.

   		ros2 launch imu_controller _imu_rviz_launch.py

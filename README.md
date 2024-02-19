# Installation

1. Inside the **src** folder of your workspace clone the package.

  git clone https://github.com/davidrdcr/imu_controller.git

4. With the terminal open in the workspace, compile the package.

colcon build

5. Configure environment variables.

echo "source ~/robot_ws/install/setup.sh" >> ~/.bashrc
source ~/.bashrc

7. Install pip

sudo apt install python3-pip

8. Add the directory to the PATH

`export PATH=$PATH:/home/USERNAME/.local/bin`

9. Install dependencies.

pip install pyserial modbus_tk transforms3d

10. Check which port the device is on.

ls /dev/ttyUSB*

11. Grant permissions to the port.

sudo chmod 777 /dev/ttyUSB0
 

12. Run the package.

ros2 run imu_controller imu_node

13. It can also be run from launch files.

ros2 launch imu_controller _imu_launch.py

16. The data can be seen echoing the topic.

ros2 topic echo /imu


## To view in Rviz

1. If you do not have rviz2 installed

sudo apt-get install ros-<distribution>-imu-tools

2. Run

ros2 launch imu_controller _imu_rviz_launch.py

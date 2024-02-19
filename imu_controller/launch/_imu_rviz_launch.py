from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
        
        launch_description = LaunchDescription()

        launch_description.add_action(
                Node(
                    package='imu_controller',
                    executable='imu_node',
                    name="imu_node",
                    output='screen'
                ),
        )
        
        launch_description.add_action(
                Node(
                    package='rviz2',
                    executable='rviz2',
                    name="rviz2",
                    output='screen',
                    arguments=['-d', str('/imu_controller/config/config2.rviz')]
                ),
        )

        return launch_description

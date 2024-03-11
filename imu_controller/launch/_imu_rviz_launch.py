import os
import launch
import launch_ros.actions

def generate_launch_description():
    package_path = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(package_path, 'config', 'config2.rviz')
    
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='imu_controller',
            executable='imu_node',
            name='imu_node',
        ),
        launch_ros.actions.Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', config_file],
        ),
    ])

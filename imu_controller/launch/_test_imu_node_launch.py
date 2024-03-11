import os
from ament_index_python.packages import get_package_share_directory
import launch
import launch_ros.actions

def generate_launch_description():
    imu_node = launch_ros.actions.Node(
        package='imu_controller',
        executable='imu_node',
        name='imu_node',
    )

    test_node = launch_ros.actions.Node(
        package='imu_controller',
        executable='test_node',
        name='test_node',
    )

    vesc_driver_node_launch = os.path.join(
        get_package_share_directory('vesc_driver'),
        'launch',
        'vesc_driver_node.launch.py'
    )

    vesc_driver_node = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(vesc_driver_node_launch)
    )

    return launch.LaunchDescription([
        imu_node,
        test_node,
        vesc_driver_node,
    ])

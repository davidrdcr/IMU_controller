import launch
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='imu_controller',
            executable='two_imu_nodes',
            name='two_imu_nodes',)
  ])

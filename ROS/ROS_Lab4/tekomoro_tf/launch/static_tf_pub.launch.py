from launch import LaunchDescription

import launch.actions
import launch_ros.actions


def generate_launch_description():    
    return LaunchDescription([
        
        launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            output='screen',
            arguments=['0.5', '0', '0', '0', '0', '0', 'base_link', 'imu_link'],
            ),

        launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            output='screen',
            arguments=['2.0', '2.0', '0', '0', '0', '0', 'map', 'base_link'],
            ),

    ])

import os

from launch import LaunchDescription, LaunchContext

from ament_index_python.packages import get_package_share_directory

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import LaunchConfigurationEquals
from launch_ros.actions import Node


def generate_launch_description():
    package_dir = get_package_share_directory("crazyflies")

    webots_dir = get_package_share_directory("crazyflie_webots_gateway")
    hardware_dir = get_package_share_directory("crazyflie_hardware_gateway")

    crazyflies_dir = get_package_share_directory("crazyflies")

    backend_arg = DeclareLaunchArgument(
        "backend",
        default_value="webots",
        description="Select used backend, currently only 'webots' or 'hardware' supported.",
    )

    webots_gateway = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([webots_dir, "/launch/gateway.launch.py"]),
        condition=LaunchConfigurationEquals("backend", "webots"),
    )

    hardware_gateway = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [hardware_dir, "/launch/crazyflie_hardware_gateway.launch.py"]
        ),
        condition=LaunchConfigurationEquals("backend", "hardware"),
    )

    motion_capture = Node(
        condition=LaunchConfigurationEquals("backend", "hardware"),
        package="ros_motioncapture",
        executable="motioncapture_node",
        name="node",
        output="screen",
        parameters=[
        	{
			"type": "optitrack",
			"hostname": "192.168.1.220"        	
        	}
        ],  # OPTITRACK PARAMETERS COMMING SOON
    )

    config = os.path.join(
        get_package_share_directory("object_tracker"), "launch", "tracker_config.yaml"
    )

    object_tracker = Node(
        condition=LaunchConfigurationEquals("backend", "hardware"),
        package="object_tracker",
        # namespace='object_tracker',
        executable="tracker",
        name="tracker",
        parameters=[config],
    )

    safeflie = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([crazyflies_dir, "/launch/safeflie.launch.py"]),
        launch_arguments={
            "id": "1",
            "channel": "80",
            "initial_position": "[0.0, 0.0, 0.0]",
            "type": "2", # Hardware: 1, Webots: 2
        }.items(),
    )

    return LaunchDescription(
        [
            backend_arg,
            webots_gateway,
            hardware_gateway,
            motion_capture,
            object_tracker,
            safeflie,
        ]
    )

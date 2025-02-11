"""
Module: ROSDroneInterface
Provides an implementation of the DroneInterface using ROS 2.

This class acts as a bridge between the drone control system and the ROS 2 framework,
allowing the drone to be controlled via ROS topics and services. It handles commands
such as takeoff, landing, sending target positions, retrieving telemetry data,
and managing range sensor callbacks.
"""

from typing import List, Callable, Optional

import rclpy
from crazyflie_interfaces_python.client import LoggingClient
from crazyflie_interfaces_python.client.logblock import LogBlockClient
from crazyflies_interfaces.msg import SendTarget
from rclpy.node import Node
from rclpy.publisher import Publisher
from std_msgs.msg import Empty
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from .DroneInterface import DroneInterface
from ..config import Config


class ROSDroneInterface(DroneInterface, Node):
    """
    ROS 2 implementation of the DroneInterface.

    This class integrates with ROS 2 to publish drone commands and retrieve telemetry data.
    It inherits from both DroneInterface (for abstract drone methods) and Node (to enable ROS 2 functionality).

    Attributes:
        takeoff_pub (Publisher): Publisher for takeoff commands.
        land_pub (Publisher): Publisher for landing commands.
        send_target_pub (Publisher): Publisher for sending target positions.
        tf_buffer (Buffer): Buffer for transform lookups.
        tf_listener (TransformListener): Listener for tracking drone position using transforms.
        logBlock (Optional[LogBlockClient]): Stores the logging block instance for range sensor data.
    """

    def __init__(self) -> None:
        """
        Initializes the ROS 2 drone interface.

        Sets up ROS publishers for takeoff, landing, and target movement commands,
        and initializes the transform listener for retrieving drone position.
        """
        super().__init__(Config.Flie.NODE_NAME)

        self.takeoff_pub: Publisher = self.create_publisher(msg_type=Empty, topic=Config.Topic.TAKEOFF,
            qos_profile=Config.Flie.QOS_PROFILE)

        self.land_pub: Publisher = self.create_publisher(msg_type=Empty, topic=Config.Topic.LAND,
            qos_profile=Config.Flie.QOS_PROFILE)

        self.send_target_pub: Publisher = self.create_publisher(msg_type=SendTarget, topic=Config.Topic.SEND_TARGET,
            qos_profile=Config.Flie.QOS_PROFILE)

        self.tf_buffer: Buffer = Buffer()
        self.tf_listener: TransformListener = TransformListener(self.tf_buffer, self)
        self.logBlock: Optional[LogBlockClient] = None

    def takeoff(self) -> None:
        """
        Commands the drone to take off by publishing to the ROS takeoff topic.
        """
        self.takeoff_pub.publish(Empty())

    def land(self) -> None:
        """
        Commands the drone to land by publishing to the ROS landing topic.
        """
        self.land_pub.publish(Empty())

    def send_target(self, position: List[float]) -> None:
        """
        Sends a target position (x, y, z) for the drone to move to.

        Parameters:
            position (List[float]): The target position.
        """
        msg = SendTarget()
        msg.target.x, msg.target.y, msg.target.z = position
        msg.base_frame = Config.Flie.BASE_FRAME
        self.send_target_pub.publish(msg)

    def get_range(self) -> float:
        """
        Retrieves the current range sensor value.

        Returns:
            float: The measured distance from the range sensor.
        """
        # TODO: Implement range retrieval from ROS logger data
        pass

    def set_range_callback(self, callback: Callable[[dict], None]) -> None:
        """
        Sets up a callback function for receiving range sensor data.

        This method creates a logging client and starts a log block to receive
        range sensor data periodically.

        Parameters:
            callback (Callable[[dict], None]): Function to be called with range data.
        """
        prefix = f"/cf{Config.Flie.ID}"
        logging_client = LoggingClient(self, prefix)
        log_block: LogBlockClient = logging_client.create_log_block(["range.zrange"], "range", callback)
        log_block.start_log_block(1)  # Log every 1 ms
        self.logBlock = log_block

    def stop_range_callback(self) -> None:
        """
        Stops the range sensor callback and disables the logging block.
        """
        if self.logBlock:
            self.logBlock.stop_log_block()

    def get_position(self) -> Optional[List[float]]:
        """
        Retrieves the current position of the drone using the ROS transform system.

        Returns:
            Optional[List[float]]: The current (x, y, z) position if available, otherwise None.
        """
        try:
            transform = self.tf_buffer.lookup_transform(Config.Flie.BASE_FRAME, Config.Flie.TF_NAME, rclpy.time.Time())
            return [transform.transform.translation.x, transform.transform.translation.y,
                    transform.transform.translation.z]
        except Exception:
            return None

    def get_time(self) -> float:
        """
        Retrieves the current system time in seconds.

        Returns:
            float: The current ROS time in seconds.
        """
        return self.get_clock().now().nanoseconds / 1e9

    def sleep(self, duration: float) -> None:
        """
        Sleeps for a specified duration while allowing ROS callbacks to process.

        This ensures that transform buffers remain updated while waiting.

        Parameters:
            duration (float): Duration in seconds to sleep.
        """
        start = self.get_time()
        end = start + duration

        while self.get_time() < end:
            rclpy.spin_once(self, timeout_sec=0)

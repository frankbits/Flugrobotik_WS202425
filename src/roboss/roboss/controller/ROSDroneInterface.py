from typing import List

import rclpy
from crazyflies_interfaces.msg import SendTarget
from rclpy.node import Node
from rclpy.publisher import Publisher
from std_msgs.msg import Empty
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from crazyflie_interfaces_python.client import LoggingClient
from crazyflie_interfaces_python.client.logblock import LogBlockClient

from .DroneInterface import DroneInterface
from ..config import Config


class ROSDroneInterface(DroneInterface, Node):
    def __init__(self):
        super().__init__(Config.Flie.NODE_NAME)

        self.takeoff_pub: Publisher = self.create_publisher(
            msg_type=Empty,
            topic=Config.Topic.TAKEOFF,
            qos_profile=Config.Flie.QOS_PROFILE
        )

        self.land_pub: Publisher = self.create_publisher(
            msg_type=Empty,
            topic=Config.Topic.LAND,
            qos_profile=Config.Flie.QOS_PROFILE
        )

        self.send_target_pub: Publisher = self.create_publisher(
            msg_type=SendTarget,
            topic=Config.Topic.SEND_TARGET,
            qos_profile=Config.Flie.QOS_PROFILE
        )

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def takeoff(self) -> None:
        self.takeoff_pub.publish(Empty())

    def land(self) -> None:
        self.land_pub.publish(Empty())

    def send_target(self, position) -> None:
        msg = SendTarget()
        msg.target.x, msg.target.y, msg.target.z = position
        msg.base_frame = Config.Flie.BASE_FRAME
        self.send_target_pub.publish(msg)

    def get_range(self) -> float:
        # TODO: get range from ROS-Logger logging data from the range sensor
        pass

    def set_range_callback(self, callback):
        prefix = "/cf{}".format(Config.Flie.ID)
        loggingClient = LoggingClient(self, prefix)
        logBlock: LogBlockClient = loggingClient.create_log_block(["range.zrange"], "range", callback)
        logBlock.start_log_block(10) #Alle 10ms messen
        self.logBlock = logBlock

    def stop_range_callback(self):
        self.logBlock.stop_log_block()

    def get_position(self) -> tuple[float] | None:
        try:
            t = self.tf_buffer.lookup_transform(Config.Flie.BASE_FRAME, Config.Flie.TF_NAME, rclpy.time.Time())
            return tuple([t.transform.translation.x, t.transform.translation.y, t.transform.translation.z])
        except Exception:
            return None

    def get_time(self) -> float:
        return self.get_clock().now().nanoseconds / 1e9

    # MUST BE CALLED to update the TF_BUFFER and thus POSITION of the drone
    def sleep(self, duration: float) -> None:
        start = self.get_time()
        end = start + duration

        while self.get_time() < end:
            rclpy.spin_once(self, timeout_sec=0)

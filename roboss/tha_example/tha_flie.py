import rclpy
from rclpy.node import Node
from rclpy.publisher import Publisher

from std_msgs.msg import Empty
from crazyflies_interfaces.msg import SendTarget

from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from typing import List


class THAFlie(Node):
    def __init__(self):
        super().__init__("tha_flie")

        cf_id = 0

        safeflie_name = f"safeflie{cf_id}"
        self.tf_name = f"cf{cf_id}"
        qos_profile = 10

        self.takeoff_pub: Publisher = self.create_publisher(
            msg_type=Empty, topic=safeflie_name + "/takeoff", qos_profile=qos_profile
        )

        self.land_pub: Publisher = self.create_publisher(
            msg_type=Empty, topic=safeflie_name + "/land", qos_profile=qos_profile
        )

        self.send_target_pub: Publisher = self.create_publisher(
            msg_type=SendTarget,
            topic=safeflie_name + "/send_target",
            qos_profile=qos_profile,
        )

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self._sleep(1)

        self.takeoff()

        self._sleep(4)

        HOME = self.get_position()
        if HOME is None:
            self.get_logger().info("Couldn't find HOME position!")

        self.send_target([0.0, 1.0, 1.0])

        self._sleep(4)

        self.send_target(HOME)

        self._sleep(4)

        self.land()

    def land(self):
        self.land_pub.publish(Empty())

    def takeoff(self):
        self.takeoff_pub.publish(Empty())

    def send_target(self, position):
        msg = SendTarget()
        msg.target.x, msg.target.y, msg.target.z = position
        msg.base_frame = "world"
        self.send_target_pub.publish(msg)

    def get_position(self) -> List[float]:
        try:
            t = self.tf_buffer.lookup_transform(
                "world", self.tf_name, rclpy.time.Time()
            )
            return [
                t.transform.translation.x,
                t.transform.translation.y,
                t.transform.translation.z,
            ]
        except Exception as ex:
            return None

    def _sleep(self, duration: float) -> None:
        """Sleeps for the provided duration in seconds."""
        start = self.__time()
        end = start + duration
        while self.__time() < end:
            rclpy.spin_once(self, timeout_sec=0)

    def __time(self) -> "Time":
        """Return current time in seconds."""
        return self.get_clock().now().nanoseconds / 1e9


def main():
    rclpy.init()
    flie = THAFlie()
    try:
        while rclpy.ok():
            rclpy.spin_once(flie, timeout_sec=0)
        flie.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

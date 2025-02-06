class DroneController:
    def __init__(self, interface):
        self.controller = interface
        self.ranges = []
        self.positions = []

    def save_positions(self, current_pos):
        """
        Callback method to save the current position and range data.

        Args:
            :param current_pos: The current [x: float, y: float, z: float] position of the drone.

        Returns:
            bool: True if the position was saved, False otherwise.
        """
        self.positions.append(current_pos)
        self.ranges.append(current_pos[2] * 1000 - self.controller.get_range())
        return True

    def move_to(self, pos, callback=None, callback_time=None):
        """
        Moves the Crazyflie drone to the specified position.

        Args:
            :param pos: The target [x: float, y: float, z: float] position.
            :param callback: (optional) A callback function to be called during the movement.
            :param callback_time: (optional) The time interval between callback calls. (if None, callback is called when the position is reached)
        """
        self.controller.send_target(pos)
        moving = True
        last_time = self.controller.get_time()

        while moving:
            current_pos = self.controller.get_position()
            current_time = self.controller.get_time()
            delta_time = current_time - last_time

            if callback is not None and callback_time is not None and delta_time >= callback_time:
                callback(delta_time, current_pos)
                last_time = current_time

            if ((abs(pos[0] - current_pos[0]) < .1) and (abs(pos[1] - current_pos[1]) < .1) and (
                    abs(pos[2] - current_pos[2]) < .1)):
                moving = False
                print("arrived: ", current_pos)
                if callback is not None and callback_time is None:
                    callback(delta_time, current_pos)

    def get_position(self):
        """
        Gets the current position of the drone.

        Returns:
            list: The current [x: float, y: float, z: float] position of the drone.
        """
        return self.controller.get_position()

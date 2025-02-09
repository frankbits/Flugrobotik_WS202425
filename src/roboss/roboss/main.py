import rclpy
from .arena.Arena import Arena
from .config import Config
from .controller.DroneController import DroneController
from .controller.ROSDroneInterface import ROSDroneInterface
from .render.Renderer import draw_board
from .route.F2CRoute import F2CRoute


def main():
    print("Running")

    arena = Arena(Config.Arena.PATH)
    draw_board(arena.get_mapped_arena())

    print("Calculating path")

    path = F2CRoute.getRoute(arena.get_obstacles())

    rclpy.init()

    interface = ROSDroneInterface()
    drone = DroneController(interface)

    print("Takeoff")

    drone.controller.takeoff()
    drone.controller.sleep(4)

    print("Flying path")

    for state in path.getStates():
        drone.move_to([state.point.X(), state.point.Y(), 1.0])

    print("Resetting and landing")

    drone.move_to([0.0, 0.0, 0.0])
    drone.controller.land()
    drone.controller.sleep(4)

    print("Finished")

    try:
        while rclpy.ok():
            rclpy.spin_once(interface, timeout_sec=0)
        interface.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

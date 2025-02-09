import math
from typing import List
import fields2cover as f2c

from ..config import Config


class F2CRoute:
    def getRoute(obstacles: List[List[float]]):
        """
        Calculates and returns the path that also avoids the specified obstacles.
        The path is optimized for field coverage and is calculated by bruteforcing the best swaths and curves are optimized using Dubin's curves.

        :param index: List containing the top left coordinates of obstacles
        :return: Path
        """
        robot = f2c.Robot(Config.Drone.WIDTH, Config.Drone.OPERATIONAL_WIDTH)
        robot.setMinTurningRadius(Config.Drone.MIN_TURNING_RADIUS)
        robot.setMaxDiffCurv(Config.Drone.MIN_TURNING_RADIUS)

        print(
            f"Setup robot ({robot.getWidth()}, {robot.getCovWidth()}) ({robot.getMinTurningRadius()}, {robot.getMaxDiffCurv()})"
        )

        field = [
            (-Config.Arena.SIZE, -Config.Arena.SIZE),
            (Config.Arena.SIZE, -Config.Arena.SIZE),
            (Config.Arena.SIZE, Config.Arena.SIZE),
            (-Config.Arena.SIZE, Config.Arena.SIZE),
            (-Config.Arena.SIZE, Config.Arena.SIZE),
        ]

        print(f"Setup flight area ({Config.Arena.SIZE}x{Config.Arena.SIZE})")

        cells = f2c.Cells(f2c.Cell(_createLinearRing(field)))
        obstacle_rings = []

        for obstacle in obstacles:
            obstacle_rings.append(
                [
                    (obstacle[0], obstacle[1]),
                    (obstacle[0] + Config.Arena.SEGMENT_SIZE, obstacle[1]),
                    (
                        obstacle[0] + Config.Arena.SEGMENT_SIZE,
                        obstacle[1] - Config.Arena.SEGMENT_SIZE,
                    ),
                    (obstacle[0], obstacle[1] - Config.Arena.SEGMENT_SIZE),
                    (obstacle[0], obstacle[1]),
                ]
            )

        for ring in obstacle_rings:
            cells.addRing(0, _createLinearRing(ring))

        print(
            f"Added {len(obstacle_rings)} obstacles to be considered during path compuation"
        )

        # decomposer = f2c.DECOMP_TrapezoidalDecomp()
        # decomposer.setSplitAngle(0.5 * math.pi)
        # cells = decomposer.decompose(cells)

        headland_generator = f2c.HG_Const_gen()
        midland = headland_generator.generateHeadlands(cells, robot.getWidth() / 2.0)
        # cells = decomposer.decompose(midland)
        mainland = headland_generator.generateHeadlands(cells, 2 * robot.getWidth() / 2.0)

        print(f"Generated headlands using {type(headland_generator)}")

        objective_function = f2c.OBJ_FieldCoverage()
        swath_generator = f2c.SG_BruteForce()

        swaths = swath_generator.generateBestSwaths(
            objective_function, robot.getCovWidth(), mainland
        )

        print(
            f"Generated swaths using {type(objective_function)} and {type(swath_generator)}"
        )

        # swath_sorter = f2c.RP_Spiral(6)
        # swaths = swath_sorter.genSortedSwaths(swaths)

        route_planner = f2c.RP_RoutePlannerBase()
        route_planner.setStartAndEndPoint(
            f2c.Point(Config.Drone.INITIAL_X, Config.Drone.INITIAL_Y)
        )
        route = route_planner.genRoute(midland, swaths)

        print(
            f"Generated route using planner: {type(route_planner)} and start point: ({route.startPoint().X()}, {route.startPoint().Y()}) and end point: ({route.endPoint().X()}, {route.endPoint().Y()})"
        )

        turning_base = f2c.PP_DubinsCurves()
        path_planner = f2c.PP_PathPlanning()
        path = path_planner.planPath(robot, route, turning_base)

        print(
            f"Planned path using planner: {type(path_planner)} and turning base: {type(turning_base)}"
        )

        f2c.Visualizer.figure()
        f2c.Visualizer.plot(cells)
        f2c.Visualizer.plot(mainland)
        f2c.Visualizer.plot(path)
        f2c.Visualizer.save(
            "/home/rosrunner/Documents/Flugrobotik/TeamRoboss/Flugrobotik_WS202425/path.png"
        )
        
        print("Saved visualization")

        return path


def _createLinearRing(field):
    points = f2c.VectorPoint()
    for x, y in field:
        points.push_back(f2c.Point(x, y))
    return f2c.LinearRing(points)

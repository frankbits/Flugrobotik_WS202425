import math

import fields2cover as f2c

from ..config import Config


class F2CRoute:
    def test():
        robot = f2c.Robot(Config.Drone.WIDTH, Config.Drone.OPERATIONAL_WIDTH)
        robot.setMinTurningRadius(Config.Drone.MIN_TURNING_RADIUS)
        robot.setMaxDiffCurv(Config.Drone.MIN_TURNING_RADIUS)

        field = [
            (-Config.Arena.SIZE, -Config.Arena.SIZE),
            (Config.Arena.SIZE, -Config.Arena.SIZE),
            (Config.Arena.SIZE, Config.Arena.SIZE),
            (-Config.Arena.SIZE, Config.Arena.SIZE),
            (-Config.Arena.SIZE, Config.Arena.SIZE),
        ]
        obstacle1 = [(1.0, 1.0), (1.2, 1.0), (1.2, 1.2), (1.0, 1.2), (1.0, 1.0)]
        obstacle2 = [
            (-1.0, -1.0),
            (-1.2, -1.0),
            (-1.2, -1.2),
            (-1.0, -1.2),
            (-1.0, -1.0),
        ]
        obstacle3 = [
            (-0.75, 0.25),
            (-0.55, 0.25),
            (-0.55, 0.45),
            (-0.75, 0.45),
            (-0.75, 0.25),
        ]

        cells = f2c.Cells(f2c.Cell(_createLinearRing(field)))
        cells.addRing(0, _createLinearRing(obstacle1))
        cells.addRing(0, _createLinearRing(obstacle2))
        cells.addRing(0, _createLinearRing(obstacle3))

        # decomposer = f2c.DECOMP_TrapezoidalDecomp()
        # decomposer.setSplitAngle(0.5 * math.pi)
        # cells = decomposer.decompose(cells)

        headland_generator = f2c.HG_Const_gen()
        midland = headland_generator.generateHeadlands(cells, 0.1)
        # cells = decomposer.decompose(midland)
        mainland = headland_generator.generateHeadlands(cells, 0.2)

        objective_function = f2c.OBJ_FieldCoverage()
        swath_generator = f2c.SG_BruteForce()

        swaths = swath_generator.generateBestSwaths(
            objective_function, robot.getCovWidth(), mainland
        )

        # swath_sorter = f2c.RP_Spiral(6)
        # swaths = swath_sorter.genSortedSwaths(swaths)

        route_planner = f2c.RP_RoutePlannerBase()
        route_planner.setStartAndEndPoint(
            f2c.Point(Config.Drone.INITIAL_X, Config.Drone.INITIAL_Y)
        )
        route = route_planner.genRoute(midland, swaths)

        turning_base = f2c.PP_DubinsCurves()
        path_planner = f2c.PP_PathPlanning()
        path = path_planner.planPath(robot, route, turning_base)

        f2c.Visualizer.figure()
        f2c.Visualizer.plot(cells)
        f2c.Visualizer.plot(mainland)
        f2c.Visualizer.plot(path)
        f2c.Visualizer.save(
            "/home/rosrunner/Documents/Flugrobotik/TeamRoboss/Flugrobotik_WS202425/path_test.png"
        )

        return path


def _createLinearRing(field):
    points = f2c.VectorPoint()
    for x, y in field:
        points.push_back(f2c.Point(x, y))
    return f2c.LinearRing(points)

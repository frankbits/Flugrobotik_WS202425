import math

import fields2cover as f2c

from ..config import Config


class F2CRoute():
    def decomp_cells_nswath_spiral_dubinscurvescc(start=None) -> F2CPath:
        if start is None:
            start = [0.0, 0.0, 0.0]

        start_point = f2c.Point(start[0], start[1], start[2])
        robot = f2c.Robot(Config.Drone.WIDTH, Config.Drone.OPERATIONAL_WIDTH)
        cells = f2c.Cells(f2c.Cell(f2c.LinearRing(f2c.VectorPoint(
            [
                f2c.Point(0, 0),
                f2c.Point(1, 0),
                f2c.Point(0, 1),
                f2c.Point(1, 1),
            ]
        ))))

        # robot.setMinTurningRadius(2)  # m
        # robot.setMaxDiffCurv(0.1);  # 1/m^2

        # Cellular Decompisition
        decomp = f2c.DECOMP_TrapezoidalDecomp()
        decomp.setSplitAngle(0.5 * math.pi)
        decomp_cell = decomp.decompose(cells)

        # Generate Headlands from decomposed cells
        const_hl = f2c.HG_Const_gen()
        no_hl = const_hl.generateHeadlands(decomp_cell, 0.0)

        # Generate the best swaths by brute forcing through all possible computations and minimizing turns
        n_swath = f2c.OBJ_NSwath()
        bf = f2c.SG_BruteForce()
        swaths = bf.generateBestSwaths(n_swath, robot.getCovWidth(), no_hl.getGeometry(0))

        # Sort the swaths in a spiral pattern
        sorter = f2c.RP_Spiral(Config.Drone.SPIRAL_SIZE)
        swaths = sorter.genSortedSwaths(swaths)

        # Plan the route
        route_planner = f2c.RP_RoutePlannerBase()
        route_planner.setStartAndEndPoint(start_point)
        route = route_planner.genRoute(const_hl, swaths)

        # Plan the path and apply Dubin's curves with continuous curvature
        path_planner = f2c.PP_PathPlanning()
        dubins_cc = f2c.PP_DubinsCurvesCC()
        path = path_planner.planPath(robot, route, dubins_cc)

        return path
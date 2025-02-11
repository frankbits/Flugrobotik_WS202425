"""
Module: F2CRoutePlanner
Provides functionality to generate an optimized field coverage path using Fields2Cover.

This module defines the `F2CRoutePlanner` class, which:
- Sets up a `Robot` with specific movement constraints.
- Defines a flight area while considering obstacles.
- Computes an optimized path using brute-force swath generation and Dubins curves.
- Visualizes and saves the computed path.

Dependencies:
    - Fields2Cover (f2c)
    - Matplotlib for visualization (via Fields2Cover)
"""

from typing import List, Tuple

import fields2cover as f2c

from .RoutePlanner import RoutePlanner
from ..config import Config
import math

class F2CRoutePlanner(RoutePlanner):
    """
    Computes an optimized coverage path while avoiding obstacles.

    This class uses Fields2Cover to generate an optimized flight path
    for a robot (e.g., a drone) using brute-force swath generation and
    Dubins curves for smooth turning.

    Methods:
        get_route(obstacles: List[List[float]]) -> f2c.Path
            Computes and returns an optimized field coverage path while avoiding obstacles.
    """

    def plan_route(self, obstacles: List[List[float]]) -> f2c.Path:
        """
        Calculates and returns the path while avoiding specified obstacles.

        The path is optimized for field coverage by:
        - Using brute-force swath selection to determine the best coverage lines.
        - Applying Dubins curves for smooth transitions between swaths.

        Parameters:
            obstacles (List[List[float]]): List of obstacle positions (x, y).

        Returns:
            f2c.Path: The computed optimized path.
        """
        robot = f2c.Robot(Config.Drone.WIDTH, Config.Drone.OPERATIONAL_WIDTH)
        robot.setMinTurningRadius(Config.Drone.MIN_TURNING_RADIUS)
        robot.setMaxDiffCurv(Config.Drone.MIN_TURNING_RADIUS)

        print(f"Setup robot with width: {robot.getWidth()}, coverage width: {robot.getCovWidth()}")
        print(f"Min turning radius: {robot.getMinTurningRadius()}, max curvature change: {robot.getMaxDiffCurv()}")

        # Define field boundaries
        field = [(-Config.Arena.SIZE, -Config.Arena.SIZE), (Config.Arena.SIZE, -Config.Arena.SIZE),
                 (Config.Arena.SIZE, Config.Arena.SIZE), (-Config.Arena.SIZE, Config.Arena.SIZE),
                 (-Config.Arena.SIZE, Config.Arena.SIZE),  # Closing the loop
                 ]

        print(f"Setup flight area ({Config.Arena.SIZE} x {Config.Arena.SIZE})")

        cells = f2c.Cells(f2c.Cell(_create_linear_ring(field)))
        obstacle_rings = []

        # Define obstacle areas as small squares
        for obstacle in obstacles:
            obstacle_rings.append([
                                    (obstacle[0], obstacle[1]), 
                                    (obstacle[0] + Config.Arena.SEGMENT_SIZE, obstacle[1]),
                                    (obstacle[0] + Config.Arena.SEGMENT_SIZE, obstacle[1] + Config.Arena.SEGMENT_SIZE,),
                                    (obstacle[0], obstacle[1] + Config.Arena.SEGMENT_SIZE),
                                    (obstacle[0], obstacle[1])
                                   ])

        for ring in obstacle_rings:
            cells.addRing(0, _create_linear_ring(ring))

        print(f"Added {len(obstacle_rings)} obstacles for path computation")

        # decomposer = f2c.DECOMP_TrapezoidalDecomp()
        # decomposer.setSplitAngle(0.5 * math.pi)
        # cells = decomposer.decompose(cells)

        # Generate headlands (buffer area around the field)
        headland_generator = f2c.HG_Const_gen()

        midland = headland_generator.generateHeadlands(cells, 0.04)
        # cells = decomposer.decompose(midland)
        mainland = headland_generator.generateHeadlands(cells, 0.02)

        print("Generated headlands for path planning using {type(headland_generator)}")

        # Generate swaths (coverage strips)
        objective_function = f2c.OBJ_NSwath()
        swath_generator = f2c.SG_BruteForce()
        swaths = swath_generator.generateBestSwaths(objective_function, robot.getCovWidth(), mainland)

        print(f"Generated swaths using {type(objective_function)} and {type(swath_generator)}")

        # swath_sorter = f2c.RP_Spiral(6)
        # swaths = swath_sorter.genSortedSwaths(swaths)

        # Plan the route with a defined starting position
        route_planner = f2c.RP_RoutePlannerBase()
        #route_planner.setStartAndEndPoint(f2c.Point(Config.Drone.INITIAL_X, Config.Drone.INITIAL_Y))
        route = route_planner.genRoute(midland, swaths)

        print(
            f"Generated route starting at ({route.startPoint().X()}, {route.startPoint().Y()}) using planner: {type(route_planner)}")

        # Plan smooth transitions using Dubins curves
        turning_base = f2c.PP_DubinsCurves()
        path_planner = f2c.PP_PathPlanning()
        path = path_planner.planPath(robot, route, turning_base)

        print(f"Generated path using planner: {type(path_planner)} and turning base: {type(turning_base)}")

        # Visualization
        f2c.Visualizer.figure()
        f2c.Visualizer.plot(cells)
        f2c.Visualizer.plot(mainland)
        f2c.Visualizer.plot(path)
        f2c.Visualizer.save(Config.Render.PATH_VISUALIZATION_FILEPATH)

        print("Saved visualization of the computed path")

        return path


def _create_linear_ring(points: List[Tuple[float, float]]) -> f2c.LinearRing:
    """
    Creates a Fields2Cover LinearRing from a list of (x, y) coordinates.

    Parameters:
        points (List[Tuple[float, float]]): A list of (x, y) coordinates defining a closed ring.

    Returns:
        f2c.LinearRing: The created linear ring object.
    """
    ring_points = f2c.VectorPoint()
    for x, y in points:
        ring_points.push_back(f2c.Point(x, y))
    return f2c.LinearRing(ring_points)

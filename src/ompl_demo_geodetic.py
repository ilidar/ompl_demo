#!/usr/bin/env python

import argparse
import random

from coordinate_system import *
from ompl_demo import *


def main(args):
    print("Env mesh:\t\t%s" % (args.env_mesh_path))
    print("Robot mesh:\t\t%s" % (args.robot_mesh_path))
    print("Start:\t\t\t%s" % (args.start))
    print("Goal:\t\t\t%s" % (args.goal))
    print("Output File Path:\t%s" % (args.output_file_path))

    config = OMPLDemoConfig(args.env_mesh_path, args.robot_mesh_path)
    handler = OMPLDemoHandler(config)

    start_point = GeodeticPoint(args.start[0], args.start[1], args.goal[2])
    goal_point = GeodeticPoint(args.goal[0], args.goal[1], args.goal[2])

    gcs = GeodeticCoordinateSystem()
    start_point = gcs.convert_to_cartesian(start_point)
    goal_point = gcs.convert_to_cartesian(goal_point)

    path = handler.find_path(start_point, goal_point)
    if path:
        OMPLPathSaver.save(path, args.output_file_path)
    else:
        print("Path not found")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OMPL demo for Geodetic coordinate system')
    parser.add_argument('--start',
            nargs='+',
            type=float,
            default=[random.uniform(-90, 90), random.uniform(-180, 180), random.uniform(0, 9000)],
            help='Start point in a format `lat, lon, alt`')
    parser.add_argument('--goal',
            nargs='+',
            type=float,
            required=True,
            help='Goal point in a format `lat, lon, alt`')
    parser.add_argument('--output_file_path',
            default="/ompl_demo/path.txt",
            help='Path to a .txt file for further visualization')
    parser.add_argument('--env_mesh_path',
            default="3D/cubicles_env.dae",
            help='Path to environement .dae file')
    parser.add_argument('--robot_mesh_path',
            default="3D/cubicles_robot.dae",
            help='Path to robot .dae file')
    args = parser.parse_args()

    main(args)


#!/usr/bin/env python

import sys
import argparse
import random


ompl_app_root = "/ompl/omplapp-1.5.2-Source"

try:
    from ompl import base as ob
    from ompl import app as oa
except ImportError:
    sys.path.insert(0, join(ompl_app_root, 'ompl/py-bindings'))
    from ompl import base as ob
    from ompl import app as oa

from coordinate_system import *

class OMPLDemoConfig(object):
    def __init__(self, env_mesh_path, robot_mesh_path):
        self.env_mesh_path = env_mesh_path
        self.robot_mesh_path = robot_mesh_path


class OMPLDemoHandler(object):
    def __init__(self, config):
        self.setup = oa.SE3RigidBodyPlanning()
        self.setup.setRobotMesh(config.robot_mesh_path)
        self.setup.setEnvironmentMesh(config.env_mesh_path)

    def find_path(self, start_point, goal_point):
        start = ob.State(self.setup.getSpaceInformation())
        start().setX(start_point.x)
        start().setY(start_point.y)
        start().setZ(start_point.z)
        start().rotation().setIdentity()

        goal = ob.State(self.setup.getSpaceInformation())
        goal().setX(goal_point.x)
        goal().setY(goal_point.y)
        goal().setZ(goal_point.z)
        goal().rotation().setIdentity()

        self.setup.setStartAndGoalStates(start, goal)
        self.setup.getSpaceInformation().setStateValidityCheckingResolution(0.01)
        self.setup.setup()

        if self.setup.solve(10):
            self.setup.simplifySolution()
            path = self.setup.getSolutionPath()
            path.interpolate(10)
            return path

        return None


class OMPLPathSaver(object):
    @classmethod
    def save(cls, path, file_path):
        with open(file_path, 'w') as file:
            file.write(path.printAsMatrix())

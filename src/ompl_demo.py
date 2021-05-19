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

class SphericalPoint(object):
	def __init__(self, lat, lon, alt):
		self.lat = lat
		self.lon = lon
		self.alt = alt

class Point(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

class SphericalCoordinateSystem(object):
	def	__init__(self):
		pass

	def convert_to_cartesian(self, spherical_point):
        # TODO: write coordinate system convertion
		return Point(spherical_point.lat, spherical_point.lon, spherical_point.alt)


class OMPLDemoConfig(object):
	def __init__(self, env_mesh_path, robot_mesh_path):
		self.env_mesh_path = env_mesh_path
		self.robot_mesh_path = robot_mesh_path


class OMPLDemoHandler(object):
	def	__init__(self, config):
		self.setup = oa.SE3RigidBodyPlanning()
		self.setup.setRobotMesh(config.robot_mesh_path)
		self.setup.setEnvironmentMesh(config.env_mesh_path)

	def find_path(self, start_point, goal_point):
		start = ob.State(self.setup.getSpaceInformation())
		start().setX(-4.96)
		start().setY(-40.62)
		start().setZ(70.57)
		start().rotation().setIdentity()

		goal = ob.State(self.setup.getSpaceInformation())
		goal().setX(200.49)
		goal().setY(-40.62)
		goal().setZ(70.57)
		goal().rotation().setIdentity()

		self.setup.setStartAndGoalStates(start, goal)
		self.setup.getSpaceInformation().setStateValidityCheckingResolution(0.01)

		self.setup.setup()
		print(self.setup)

		if self.setup.solve(10):
			self.setup.simplifySolution()
			path = self.setup.getSolutionPath()
			path.interpolate(10)
			print(path.printAsMatrix())
			print(path.check())
			return path
		else:
			return None


class OMPLPathSaver(object):
	@classmethod
	def save(cls, path, file_path):
		with open(file_path, 'w') as file:
			file.write(path.printAsMatrix())


def main(args):
	print("Env mesh:\t\t\t%s" % (args.env_mesh_path))
	print("Robot mesh:\t\t\t%s" % (args.robot_mesh_path))
	print("Start:\t\t\t%s" % (args.start))
	print("Goal:\t\t\t%s" % (args.goal))
	print("Output File Path:\t%s" % (args.output_file_path))

	config = OMPLDemoConfig(args.env_mesh_path, args.robot_mesh_path)
	handler = OMPLDemoHandler(config)

	scs = SphericalCoordinateSystem()
	start_point = SphericalPoint(args.start[0], args.start[1], args.goal[2])
	goal_point = SphericalPoint(args.goal[0], args.goal[1], args.goal[2])
	start_point = scs.convert_to_cartesian(start_point)
	goal_point = scs.convert_to_cartesian(goal_point)

	path = handler.find_path(start_point, goal_point)
	if path:
		OMPLPathSaver.save(path, args.output_file_path)
	else:
		print("Path not found")



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='OMPL demo')
	parser.add_argument('--start',
						nargs='+',
						type=float,
						default=[random.uniform(0, 1.0), random.uniform(0, 1.0), random.uniform(0, 1.0)],
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


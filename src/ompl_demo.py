#!/usr/bin/env python

import sys
import argparse
import random
import math

ompl_app_root = "/ompl/omplapp-1.5.2-Source"

try:
	from ompl import base as ob
	from ompl import app as oa
except ImportError:
	sys.path.insert(0, join(ompl_app_root, 'ompl/py-bindings'))
	from ompl import base as ob
	from ompl import app as oa

class GeodeticPoint(object):
	def __init__(self, lat, lon, alt):
		self.lat = lat
		self.lon = lon
		self.alt = alt

class Point(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

# Geodetic to cartesian convertion
# Reference 1: https://en.wikipedia.org/wiki/Reference_ellipsoid#Coordinates
# Reference 2: https://github.com/purpleskyfall/XYZ2BLH/blob/master/blh2xyz.py

class GeodeticCoordinateSystem(object):
	def convert_to_cartesian(self, geodetic_point):
		A = 6378137.0
		B = 6356752.314245
		latitude = math.radians(geodetic_point.lat)
		longitude = math.radians(geodetic_point.lon)
		height = geodetic_point.alt
		e = math.sqrt(1 - (B**2)/(A**2))
		N = A / math.sqrt(1 - e**2 * math.sin(latitude)**2)
		X = (N + height) * math.cos(latitude) * math.cos(longitude)
		Y = (N + height) * math.cos(latitude) * math.sin(longitude)
		Z = (N * (1 - e**2) + height) * math.sin(latitude)
		return Point(X, Y, Z)


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
		else:
			return None


class OMPLPathSaver(object):
	@classmethod
	def save(cls, path, file_path):
		with open(file_path, 'w') as file:
			file.write(path.printAsMatrix())


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
	parser = argparse.ArgumentParser(description='OMPL demo')
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


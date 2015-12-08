from util import Directions
from util import PriorityQueue
import copy

class AStar:
	EMPTY_VAL = 0
	OBSTACLE_VAL = 1
	ROBOT_VAL = 2
	FINISH_PT_VAL = 3
	ROBOT_OCCUP_VAL = 4


	# the robot position is the upper left corner of the robot rectangle
	# the sizes are in format (width, height)
	# the positions are in format (x,y)
	def __init__(self,grid,robotPos,goalPos, robotSize):
		self.grid = copy.deepcopy(grid)
		self.robotStartPos = robotPos
		self.goalPos = goalPos
		self.robotSize = robotSize
		self.robotId = 4

	# checks if the passed in position will not hit any obstacles
	def isLegalPos(self,currPos):
		numRows = len(self.grid)
		numCols = len(self.grid[0])
		# check if robot will stay in grid
		if(currPos[0] >= 0 and currPos[1] >= 0 and 
			(currPos[0] + self.robotSize[0] + 1 < numCols) and (currPos[1] + self.robotSize[1] + 1 < numRows)):
		
			for y in range(currPos[1],currPos[1] + self.robotSize[1]+1):
				for x in range(currPos[0], currPos[0] + self.robotSize[0]+1):
					if(self.grid[y][x] != AStar.EMPTY_VAL):
						if(self.grid[y][x] == AStar.OBSTACLE_VAL or (self.grid[y][x] != AStar.FINISH_PT_VAL and self.grid[y][x] != self.robotId)):
							return False
			return True
		return False


	# returns the possible new positions for the robot
	# format of return nodes is ((x,y),Direction)

	def getSuccessors(self,currPos):
		nodes = []
		for direct in Directions.DIR_VECT_DICT:
			vect = Directions.DIR_VECT_DICT[direct]
			newPos = (currPos[0]+vect[0], currPos[1]+vect[1])
			if(self.isLegalPos(newPos) == True):
				nodes.append((newPos,direct))
		return nodes

	def isGoalState(self,currPos):
		if(self.getDistToGoal(currPos) < 5):
			return True
		else:
			return False
		'''
		for y in range(currPos[1], currPos[1] + self.robotSize[1]):
			for x in range(currPos[0], currPos[0] + self.robotSize[0]):
				if(self.grid[y][x] == AStar.FINISH_PT_VAL):
					return True
		return False
		'''


	def getDistToGoal(self,currPos):
		x_dist = (currPos[0] - self.goalPos[0])**2
		y_dist = (currPos[1] - self.goalPos[0])**2
		return (x_dist + y_dist) ** 0.5


	def getDirectionsToGoal(self):
		priorityQueue = PriorityQueue()
		# heap data is in the form (position, prevPosition, direction to position, cumul cost)
		priorityQueue.push((self.robotStartPos,(-1,-1),Directions.SOUTH,0),0)
		# dictionary key is in format (x,y)
		# dictionary value is in format ((prev_x,prev_y),Direction)

		visitedNodes = {}
		foundGoalPos = None

		while(priorityQueue.isEmpty() == False):
			currNode = priorityQueue.pop()
			currNodePos = currNode[0]
			if(self.isGoalState(currNodePos)):
				#print "Goal FOUND!!!"
				#rint currNodePos
				foundGoalPos = currNodePos
				visitedNodes[currNodePos] = (currNode[1],currNode[2])
				break
			if(visitedNodes.get(currNodePos) == None):
				visitedNodes[currNodePos] = (currNode[1],currNode[2])
				successors = self.getSuccessors(currNodePos)
				for succ in successors:
					s_node_pos = succ[0]
					s_direction = succ[1]
					cumulCost = currNode[3] + 1 #for now just increment accumulative cost by 1
					heurVal = self.getDistToGoal(s_node_pos)
					priorityQueue.push((s_node_pos,currNodePos,s_direction,cumulCost),cumulCost+heurVal)

		if(foundGoalPos != None):
			directions = []
			currPos = foundGoalPos
			while(currPos != self.robotStartPos):
				currNode = visitedNodes[currPos]
				currPos = currNode[0]
				direction = currNode[1]
				directions.append(direction)
			directions.append(visitedNodes[currPos][1])
			directions.reverse()
			return directions
		else:
			return None

	def fillRobotSpace(self,currPos,grid,val):
		for y in range(currPos[1], currPos[1] + self.robotSize[1]):
			for x in range(currPos[0], currPos[0] + self.robotSize[0]):
				grid[y][x] = val

	def fillGridWithDirections(self,directions,numWayPoints,grid):
		if(directions != None and len(directions) >= numWayPoints):
			#print "FILLING DIRECTIONS!"
			currPos = self.robotStartPos
			for i in range(0,numWayPoints):
				self.fillRobotSpace(currPos,grid,self.robotId)
				vect = Directions.DIR_VECT_DICT[directions[i]]
				currPos = (currPos[0]+vect[0],currPos[1]+vect[1])

			self.fillRobotSpace(currPos,self.grid,self.robotId)
			self.fillRobotSpace(self.robotStartPos,self.grid,AStar.EMPTY_VAL)

			return currPos





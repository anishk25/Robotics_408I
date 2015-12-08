import random
from a_star import AStar

GRID_HEIGHT = 100
GRID_WIDTH  = 100

ROBOT_SIZE = (4,4)
OBSTACLE_SIZE = (2,2)
FINISH_PT_SIZE = (2,2)


def printGrid(grid):
	for y in range(0,len(grid)):
		for x in range(0,len(grid[y])):
			if(grid[y][x] == AStar.EMPTY_VAL):
				print "  ",
			else:
				print str(grid[y][x]) + " ",
		print ""



def fillRobotSpace(grid, rCornPos,robotSize,robotVal):
	for y in range (rCornPos[1], rCornPos[1] + robotSize[1]):
		for x in range(rCornPos[0], rCornPos[0] + robotSize[1]):
			grid[y][x] = robotVal

# l is top left of rect, r is bottom right of rect
def rectIntersect(l1,r1,l2,r2):
	if(l1[0] > r2[0] or l2[0] > r1[0]):
		return False
	if(l1[1] < r2[1] or l2[1] < r1[1]):
		return False
	return True

def insertObtsacles(numObstacles, grid, obstacleSize, obstacleVal):
	numRows = len(grid) 
	numCols = len(grid[0])
	for i in range(0,numObstacles):
		found = False
		while(found == False):
			rand_y = random.randint(0,numRows-obstacleSize[1] - 1)
			rand_x = random.randint(0,numCols-obstacleSize[0] - 1)
			squareGood = True
			for y in range(rand_y,rand_y+obstacleSize[1]):
				for x in range(rand_x, rand_x + obstacleSize[0]):
					if(grid[y][x] != 0):
						squareGood = False
			if(squareGood):
				found = True
				for y in range(rand_y,rand_y+obstacleSize[1]):
					for x in range(rand_x, rand_x + obstacleSize[0]):
						grid[y][x] = obstacleVal

def insertFinishPt(finishPtVal,grid,finishPtSize):
	numRows = len(grid) 
	numCols = len(grid[0])
	found = False
	while(found == False):
		rand_y = random.randint(3*(numRows/4),numRows-finishPtSize[1] - 1)
		rand_x = random.randint(3*(numCols/4),numCols-finishPtSize[0] - 1)
		squareGood = True
		for y in range(rand_y,rand_y+finishPtSize[1]):
			for x in range(rand_x, rand_x + finishPtSize[0]):
				if(grid[y][x] != 0):
					squareGood = False
		if(squareGood == True):
			found = True
			for y in range(rand_y,rand_y+finishPtSize[1]):
				for x in range(rand_x, rand_x + finishPtSize[1]):
					grid[y][x] = finishPtVal
			return (rand_x,rand_y)



gridValues = [[0 for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
currentRobotPositions = [(1,1,),(5,20),(10,40)]
numRobots = len(currentRobotPositions)

for r in range(0,numRobots):
	fillRobotSpace(gridValues,currentRobotPositions[r],ROBOT_SIZE,r+4)

insertObtsacles(40, gridValues, OBSTACLE_SIZE, AStar.OBSTACLE_VAL)
goalPos = insertFinishPt(AStar.FINISH_PT_VAL, gridValues,FINISH_PT_SIZE)


aStarProb = AStar(gridValues,currentRobotPositions[0],goalPos,ROBOT_SIZE)

NUM_STEPS = 10
NUM_ITERATIONS = 12

for i in range(0,NUM_ITERATIONS):
	for r in range(0,numRobots):
		if(currentRobotPositions[r] != None):
			aStarProb.robotStartPos = currentRobotPositions[r]
			aStarProb.robotId = r + 4
			directions = aStarProb.getDirectionsToGoal()
			#print directions
			nextPos = aStarProb.fillGridWithDirections(directions,NUM_STEPS,gridValues)
			#print nextPos
			currentRobotPositions[r] = nextPos

printGrid(gridValues)

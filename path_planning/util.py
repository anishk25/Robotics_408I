import heapq

class PriorityQueue:
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0


class Directions:
  NORTH     = "N"
  SOUTH     = "S"
  EAST      = "E"
  WEST      = "W"
  NORTH_EAST = "NE"
  NORTH_WEST = "NW"
  SOUTH_EAST = "SE"
  SOUTH_WEST = "SW"

  DIR_VECT_DICT = {
    NORTH:(0,-1), 
    SOUTH:(0,1),
    EAST:(1,0),
    WEST:(-1,0),
    NORTH_EAST:(1,-1),
    NORTH_WEST:(-1,-1),
    SOUTH_EAST:(1,1),
    SOUTH_WEST:(-1,1)
  }
from maze import *
from exception import *
from stack import *
class PacMan:
    def __init__(self, grid):
        self.navigator_maze = grid.grid_representation
    def find_path(self, start, end ):
        dir = [(-1,0),(1,0),(0,-1),(0,1)]
        rows = len(self.navigator_maze)
        columns = len(self.navigator_maze[0])
        if self.navigator_maze[start[0]][start[1]] == 1 or self.navigator_maze[end[0]][end[1]]:
            raise PathNotFoundException("Ghost at starting or end location")
        covered = [[0] * columns for i in range(rows)]
        covered[start[0]][start[1]] = 1
        s = Stack()
        s.push((start[0],start[1],[(start[0], start[1])]))
        while not s.isempty():
            x, y, p = s.pop()
            #p.append((x,y))
            p2 = p 
            if (x,y) == end:
                return p
            for x1,y1 in dir:
                x2 = x + x1 
                y2 = y + y1
                if 0<= x2 < rows and 0 <= y2 < columns and covered[x2][y2] == 0 and self.navigator_maze[x2][y2] == 0:
                    covered[x2][y2] = 1
                    s.push((x2,y2,p + [(x2, y2)]))
        raise PathNotFoundException

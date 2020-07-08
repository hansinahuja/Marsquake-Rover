from collections import deque
import heapq

# right, left, up, down, right-up, right-down, left-up, left-down

def jumpPointSearch(self, environment, targets):
    self.logs = []

    def valid(x, y):
        return x >= 0 and y >= 0 and x < environment.length and y < environment.breadth
    def setX(direction):
        if direction == 'right':
            dx1 = 0
            dy1 = 1
            dx2 = [1, -1]
            dy2 = [0, 0]
            dx3 = [1, -1]
            dy3 = [1, 1]
        if direction == 'left':
            dx1 = 0
            dy1 = -1
            dx2 = [1, -1]
            dy2 = [0, 0]
            dx3 = [1, -1]
            dy3 = [-1, -1]
        if direction == 'up':
            dx1 = -1
            dy1 = 0
            dx2 = [0, 0]
            dy2 = [1, -1]
            dx3 = [-1, -1]
            dy3 = [1, -1]
        if direction == 'down':
            dx1 = 1
            dy1 = 0
            dx2 = [0, 0]
            dy2 = [1, -1]
            dx3 = [1, 1]
            dy3 = [1, -1]
        if direction == 'right-up':
            dx1 = -1
            dy1 = 1
            dx2 = [0, 1]
            dy2 = [-1, 0]
            dx3 = [-1, 1]
            dy3 = [-1, 1]
        if direction == 'left-up':
            dx1 = -1
            dy1 = -1
            dx2 = [1, 0]
            dy2 = [0, 1]
            dx3 = [1, -1]
            dy3 = [-1, 1]
        if direction == 'right-down':
            dx1 = 1
            dy1 = 1
            dx2 = [-1, 0]
            dy2 = [0, -1]
            dx3 = [-1, 1]
            dy3 = [1, -1]
        if direction == 'left-down':
            dx1 = 1
            dy1 = -1
            dx2 = [-1, 0]
            dy2 = [0, 1]
            dx3 = [-1, 1]
            dy3 = [-1, 1]
        return dx1, dy1, dx2, dy2, dx3, dy3


    def nonDiagonal (nextCell, direction, weight, directionFrom):
        x , y = nextCell.location.x, nextCell.location.y
        
        dx1 , dy1 , dx2 , dy2, dx3, dy3 = setX(direction)
        Flg1 = 0
        while True:
            if not valid(x, y):
                return
            currentCell = environment.grid[x][y]
            if currentCell.type == 'wall':
                return
            if Flg1:
                self.path[(currentCell, direction)] = (nextCell, directionFrom)            
            self.logs.append([self, currentCell, 'visited'])
            self.visited.add((currentCell, direction))
            if currentCell.type == 'destination':
                return 
            
            flag = 0
            X1 , Y1 , X2 , Y2 = x+dx2[0] , y+dy2[0] , x+dx3[0] , y+dy3[0] 
            if valid(X1, Y1) and valid(X2, Y2):
                if environment.grid[X1][Y1].type == 'wall' and environment.grid[X2][Y2].type != 'wall':
                    forcedNeighbor = environment.grid[X2][Y2]
                    if direction == 'right':
                        newDirection = 'right-down'
                    if direction == 'left':
                        newDirection = 'left-down'
                    if direction == 'up':
                        newDirection = 'right-up'
                    if direction == 'down':
                        newDirection = 'right-down'
                    if (forcedNeighbor, newDirection) not in self.visited:
                        nxt = (environment.bestHeuristic(forcedNeighbor, targets) + weight + forcedNeighbor.weight, forcedNeighbor , newDirection, direction)
                        heapq.heappush(self.waitList, nxt)
                        self.logs.append([self, forcedNeighbor, 'inQueue'])
                        self.path[(forcedNeighbor, newDirection)] = (environment.grid[x][y], direction)
                        flag = 1

            X1 , Y1 , X2 , Y2 = x+dx2[1] , y+dy2[1] , x+dx3[1] , y+dy3[1]
            if valid(X1, Y1) and valid(X2, Y2):
                if environment.grid[X1][Y1].type == 'wall' and environment.grid[X2][Y2].type != 'wall':
                    forcedNeighbor = environment.grid[X2][Y2]
                    if direction == 'right':
                        newDirection = 'right-up'
                    if direction == 'left':
                        newDirection = 'left-up'
                    if direction == 'up':
                        newDirection = 'left-up'
                    if direction == 'down':
                        newDirection = 'left-down'
         
                    if (forcedNeighbor, newDirection) not in self.visited:
                        nxt = (environment.bestHeuristic(forcedNeighbor, targets) + weight + forcedNeighbor.weight, forcedNeighbor , newDirection, direction)
                        heapq.heappush(self.waitList, nxt)    
                        self.logs.append([self, forcedNeighbor, 'inQueue'])
                        self.path[(forcedNeighbor, newDirection)] = (environment.grid[x][y], direction)                    
                        flag = 1
            
            if flag and valid(x+dx1, y+dy1) and environment.grid[x+dx1][y+dy1].type != 'wall':
                cell = environment.grid[x + dx1][y+dy1]
                if (cell, direction) not in self.visited:
                    nxt = (environment.bestHeuristic(cell, targets) + weight + cell.weight, cell , direction, direction)
                    heapq.heappush(self.waitList, nxt)
                    self.logs.append([self, cell, 'inQueue'])
                    self.path[(cell, direction)] = (nextCell, direction)
                    return
            weight += 1
            y += dy1
            x += dx1
            Flg1 = 1

    def diagonal(nextCell, direction, weight, directionFrom):
        x , y = nextCell.location.x, nextCell.location.y
        dx1, dy1, dx2, dy2, dx3, dy3 = setX(direction)
        
        Flg1 = 0
        while True:
            if not valid(x, y):
                return
            currentCell = environment.grid[x][y]
            if currentCell.type == 'wall':
                return
            if Flg1:
                self.path[(currentCell, direction)] = (nextCell, directionFrom)
            self.logs.append([self, currentCell, 'visited'])
            self.visited.add((currentCell, direction))
            if currentCell.type == 'destination':
                return 
            if direction == 'right-up':
                self.path[(currentCell, 'right')] = (currentCell, direction)
                self.path[(currentCell, 'up')] = (currentCell, direction) 
                nonDiagonal(currentCell,'right', weight, direction)
                nonDiagonal(currentCell,'up', weight, direction)
            if direction == 'left-up':
                self.path[(currentCell, 'left')] = (currentCell, direction)
                self.path[(currentCell, 'up')] = (currentCell, direction) 
                nonDiagonal(currentCell,'left', weight, direction)
                nonDiagonal(currentCell,'up', weight, direction)
            if direction == 'right-down':
                self.path[(currentCell, 'right')] = (currentCell, direction)
                self.path[(currentCell, 'down')] = (currentCell, direction) 
                nonDiagonal(currentCell,'right', weight, direction)
                nonDiagonal(currentCell,'down', weight, direction)
            if direction == 'left-down':
                self.path[(currentCell, 'left')] = (currentCell, direction)
                self.path[(currentCell, 'down')] = (currentCell, direction) 
                nonDiagonal(currentCell,'left', weight, direction)
                nonDiagonal(currentCell,'down', weight, direction)
            
            flag = 0
            X1 , Y1 , X2 , Y2 = x + dx2[0] , y + dy2[0] , x + dx3[0] , y + dy3[0]
            if valid(X1, Y1) and valid(X2, Y2):
                if environment.grid[X1][Y1].type == 'wall' and environment.grid[X2][Y2].type != 'wall':
                    forcedNeighbor = environment.grid[X2][Y2]
                    if direction == 'right-up':
                        newDirection = 'left-up'
                    if direction == 'left-up':
                        newDirection = 'left-down'
                    if direction == 'right-down':
                        newDirection = 'right-up'
                    if direction == 'left-down':
                        newDirection = 'left-up'
                    if (forcedNeighbor, newDirection) not in self.visited:
                        nxt = (environment.bestHeuristic(forcedNeighbor, targets) + weight + forcedNeighbor.weight, forcedNeighbor , newDirection, direction)
                        heapq.heappush(self.waitList, nxt)
                        self.logs.append([self, forcedNeighbor, 'inQueue'])
                        self.path[(forcedNeighbor, newDirection)] = (environment.grid[x][y], direction)
                        flag = 1
            
            X1 , Y1 , X2 , Y2 = x + dx2[1] , y + dy2[1] , x + dx3[1] , y + dy3[1]
            if valid(X1, Y1) and valid(X2, Y2):
                if environment.grid[X1][Y1].type == 'wall' and environment.grid[X2][Y2].type != 'wall':
                    forcedNeighbor = environment.grid[X2][Y2]
                    if direction == 'right-up':
                        newDirection = 'right-down'
                    if direction == 'left-up':
                        newDirection = 'right-up'
                    if direction == 'right-down':
                        newDirection = 'left-down'
                    if direction == 'left-down':
                        newDirection = 'right-down'
                    if (forcedNeighbor, newDirection) not in self.visited:
                        nxt = (environment.bestHeuristic(forcedNeighbor, targets) + weight + forcedNeighbor.weight, forcedNeighbor , newDirection, direction)
                        heapq.heappush(self.waitList, nxt)
                        self.logs.append([self, forcedNeighbor, 'inQueue'])
                        self.path[(forcedNeighbor, newDirection)] = (environment.grid[x][y], direction)
                        flag = 1
            
            if flag and valid(x+dx1, y+dy1) and environment.grid[x+dx1][y+dy1].type != 'wall':
                cell = environment.grid[x+dx1][y+dy1]
                if (cell, direction) not in self.visited:
                    nxt = (environment.bestHeuristic(cell, targets) + weight + cell.weight, cell , direction, direction)
                    heapq.heappush(self.waitList, nxt)
                    self.logs.append([self, cell, 'inQueue'])
                    self.path[(cell, direction)] = (nextCell, direction)
                    return 
            y += dy1
            x += dx1
            weight += 1
            Flg1 = 1


    # First iteration
    if self.waitList == None:
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.visited.add(sourceCell)
        x = sourceCell.location.x
        y = sourceCell.location.y
        self.waitList = []
        directions = [ 'right', 'left', 'up', 'down', 'right-up', 'right-down', 'left-up', 'left-down']
        for direction in directions:
            self.waitList.append ( (environment.bestHeuristic(sourceCell, targets), sourceCell , direction, direction) )
        
        heapq.heapify(self.waitList)

    # Exhausted all possible moves
    if len(self.waitList)==0:
        return

    next = heapq.heappop(self.waitList)
    weight = next[0]
    nextCell = next[1]
    direction = next[2]
    directionFrom = next[3]

    if direction == 'right' or direction == 'left' or direction == 'up' or direction == 'down':
        nonDiagonal(nextCell, direction, weight, directionFrom)
    else:
        diagonal(nextCell, direction, weight, direction)
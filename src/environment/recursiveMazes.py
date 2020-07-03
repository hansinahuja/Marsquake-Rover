import random

def recursiveMaze(self):
        walls = []

        def randomOddNumber(low, high):
            low = low // 2 
            if high % 2:
                high = high // 2
            else:
                high = high // 2 - 1
            return 2 * random.randrange(low, high+1) + 1
        def randomEvenNumber(low, high):
            low = low // 2 + low % 2
            high = high // 2 
            return 2 * random.randrange(low, high+1)

        def generate(left, right, top, bottom):
            if left >= right or top >= bottom:
                return
            if left >= right - 1 and top >= bottom - 1:
                return

            rnd = random.randrange(0, 2)   
            if left >= right - 1:
                rnd = 0
            if top >= bottom - 1:
                rnd = 1
            if(rnd == 0):                                                 # Horizontal division
                row = randomEvenNumber(top, bottom)
                for i in range(left, right + 1):
                    if self.grid[row][i].type != 'source' and self.grid[row][i].type != 'destination':
                        self.grid[row][i].type = 'wall'
                        walls.append(self.grid[row][i].location)
                i = randomOddNumber(left, right)
                if self.grid[row][i].type != 'source' and self.grid[row][i].type != 'destination':
                    self.grid[row][i].type = 'free'              
                    walls.remove(self.grid[row][i].location)           
                generate(left, right, top, row - 1)
                generate(left, right, row + 1, bottom)
            
            else:                                                           # Vertical division
                clm = randomEvenNumber(left, right + 1)
                for i in range(top, bottom + 1):
                    if self.grid[i][clm].type != 'source' and self.grid[i][clm].type != 'destination':
                        self.grid[i][clm].type = 'wall'
                        walls.append(self.grid[i][clm].location)
            
                i = randomOddNumber(top, bottom)
                if self.grid[i][clm].type != 'source' and self.grid[i][clm].type != 'destination':
                    self.grid[i][clm].type = 'free'        
                    walls.remove(self.grid[i][clm].location)   
                generate(left, clm - 1, top, bottom)
                generate(clm + 1, right, top, bottom)

        generate(0, self.length - 1, 0, self.breadth - 1)
        return walls


def randomizedPrim(self) :
    def isValid(x, y):
        return x >=0 and y>=0 and x < self.breadth and y < self.length
    def mid(cellA, cellB):
        return self.grid[ (cellA.location.x + cellB.location.x) // 2][ (cellA.location.y + cellB.location.y) // 2 ]
    def getBlockedCells(cell):
        x = cell.location.x
        y = cell.location.y
        dx = [0, 2, 0, -2]
        dy = [-2, 0, 2, 0]
        ret = set()
        for i in range(4):
            X = x + dx[i]
            Y = y + dy[i]
            if isValid(X, Y) and self.grid[X][Y].type == 'wall':
                ret.add( self.grid[X][Y] )
        return ret
    def getFreeCells(cell):
        x = cell.location.x
        y = cell.location.y
        dx = [0, 2, 0, -2]
        dy = [-2, 0, 2, 0]
        ret = set()
        for i in range(4):
            X = x + dx[i]
            Y = y + dy[i]
            if isValid(X, Y) and self.grid[X][Y].type != 'wall':
                ret.add( self.grid[X][Y] )
        return ret.pop()

    
    for row in self.grid:
        for cell in row:
            if cell.type != 'source' and cell.type != 'destination':
                cell.type = 'wall'
            else:
                src = cell
    
    blocked = getBlockedCells(src)
    
    while len(blocked) :
        cell = blocked.pop()
        free = getFreeCells(cell)
        newFree = mid(free, cell)
        if newFree.type == 'wall':
            newFree.type = 'free'
        if cell.type == 'wall':
            cell.type = 'free'
        S1 = getBlockedCells(cell)
        for i in S1:
            blocked.add(i)
    
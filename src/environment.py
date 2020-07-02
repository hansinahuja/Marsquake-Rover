from utilities import Location, Cell

class Environment:
    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth
        self.grid = [ [Cell(Location(x, y)) for y in range(breadth)] for x in range(length) ]

    def placeAgent(self, agent):
        x = agent.location.x
        y = agent.location.y
        self.grid[x][y].type = agent.type
        if agent.type=='source':
            self.grid[x][y].srcAgent = agent
        else:
            self.grid[x][y].destAgent = agent

    # For debugging
    def print(self):
        for row in self.grid:
            for cell in row:
                print(cell.type[0], end = ' ')
            print()
        print()

    # For debugging
    def printInitial(self):
        for row in self.grid:
            for cell in row:
                if(cell.type == 'wall'):
                    print('#', end = '')
                elif(cell.type == 'destination'):
                    print('X', end = '')
                elif(cell.type == 'source'):
                    print('O', end = '')
                else:
                    print('.', end = '')
            print()
        print()

    def update(self, logs):
        updates = {}
        success = set()
        for log in logs:
            agent, cell, state = log
            if cell not in updates:
                updates[cell] = log
            elif state=='visited' and updates[cell][2]!='visited':
                updates[cell] = log

        for log in updates.values():
            agent, cell, state = log
            if cell.type!='source' and cell.type!='destination':
                cell.type = state

            if agent.type=='source' and cell.srcAgent==None:
                cell.srcAgent = agent

            if agent.type=='destination' and cell.destAgent==None:
                cell.destAgent = agent

            if state=='visited' and cell.srcAgent!=None and cell.destAgent!=None:
                success.add(cell)

        return success

    def getPaths(self, success):
        paths = []

        for cell in success:
            # print(cell.location.x, cell.location.y)
            path1 = []
            agent = cell.srcAgent
            c = cell
            while c in agent.path:
                path1.append([c.location.x, c.location.y])
                c = agent.path[c]
            path1.append([agent.location.x, agent.location.y])
            
            agent = cell.destAgent
            path2 = []
            c = cell
            while c in agent.path:
                path2.append([c.location.x, c.location.y])
                c = agent.path[c]
            path2.append([agent.location.x, agent.location.y])
                
            path1.reverse()
            path = path1 + path2[1:]
            paths.append(path)
        return paths

    def recursiveMaze(self):
        import random

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
                i = randomOddNumber(left, right)
                if self.grid[row][i].type != 'source' and self.grid[row][i].type != 'destination':
                    self.grid[row][i].type = 'free'                         
                generate(left, right, top, row - 1)
                generate(left, right, row + 1, bottom)
            
            else:                                                           # Vertical division
                clm = randomEvenNumber(left, right + 1)
                for i in range(top, bottom + 1):
                    if self.grid[i][clm].type != 'source' and self.grid[i][clm].type != 'destination':
                        self.grid[i][clm].type = 'wall'
            
                i = randomOddNumber(top, bottom)
                if self.grid[i][clm].type != 'source' and self.grid[i][clm].type != 'destination':
                    self.grid[i][clm].type = 'free'                         
                generate(left, clm - 1, top, bottom)
                generate(clm + 1, right, top, bottom)

        generate(0, self.length - 1, 0, self.breadth - 1)

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
from environment.utils import Location, Cell


class Environment:
    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth
        self.grid = [[Cell(Location(x, y)) for y in range(breadth)]
                     for x in range(length)]
        self.heuristic = 'manhattan'
        self.allowDiagonals = False
        self.cutCorners = False

    def placeAgent(self, agent):
        x = agent.location.x
        y = agent.location.y
        self.grid[x][y].type = agent.type
        if agent.type == 'source':
            self.grid[x][y].srcAgent = agent
        else:
            self.grid[x][y].destAgent = agent

    from environment.randomMazes import recursiveMaze, randomizedPrim
    from environment.heuristics import bestHeuristic

    # For debugging
    def print(self):
        for row in self.grid:
            for cell in row:
                if cell.type == 'waitList':
                    print('i', end=' ')
                else:
                    print(cell.type[0], end=' ')
            print()
        print()

    # For debugging
    def printInitial(self):
        for row in self.grid:
            for cell in row:
                if(cell.type == 'wall'):
                    print('#', end='')
                elif(cell.type == 'destination'):
                    print('X', end='')
                elif(cell.type == 'source'):
                    print('O', end='')
                else:
                    print('.', end='')
            print()
        print()

    def update(self, logs):
        updates = {}
        success = set()
        recursiveMode = False
        logs = list(filter(None, logs))

        if len(logs) == 0:
            return success

        if logs[0][2] == 'inRecursion' or logs[0][2] == 'outOfRecursion':
            recursiveMode = True

        for log in logs:
            agent, cell, state = log
            if cell not in updates:
                updates[cell] = log
            elif not recursiveMode and state == 'visited' and updates[cell][2] != 'visited':
                updates[cell] = log
            elif recursiveMode and state == 'inRecursion' and updates[cell][2] != 'inRecursion':
                updates[cell] = log

        for log in updates.values():
            agent, cell, state = log
            if cell.type != 'source' and cell.type != 'destination':
                cell.type = state
                if recursiveMode:
                    if state == 'inRecursion':
                        cell.type = 'visited'
                    else:
                        cell.type = 'free'

            if agent.type == 'source' and cell.srcAgent == None:
                cell.srcAgent = agent

            if agent.type == 'destination' and cell.destAgent == None:
                cell.destAgent = agent

            if not recursiveMode and state == 'visited' and cell.srcAgent != None and cell.destAgent != None:
                success.add(cell)

            if recursiveMode and cell.srcAgent != None and cell.destAgent != None:
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
                print(c.location.x, c.location.y)
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

    def tmpPaths(self, success, weight):                          # For idaStar and ida
        paths = []

        for cell in success:
            # print(cell.location.x, cell.location.y)
            path1 = []
            agent = cell.srcAgent
            c = cell
            wt = weight
            while (c, wt) in agent.path:
                print(c.location.x, c.location.y)
                path1.append([c.location.x, c.location.y])
                X = agent.path[(c, wt)]
                c = X[0]
                wt = X[1]
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

    def getJpsPaths(self, success):
        paths = []

        for cell in success:
            path1 = []
            agent = cell.srcAgent
            c = cell
            directions = ['right', 'left', 'up', 'down',
                          'right-up', 'right-down', 'left-up', 'left-down']
            for direction in directions:
                if (c, direction) in agent.path:
                    s = direction
            while (c, s) in agent.path:
                path1.append([c.location.x, c.location.y])
                tmp = agent.path[(c, s)][0]
                s = agent.path[(c, s)][1]
                c = tmp
            path1.append([agent.location.x, agent.location.y])

            agent = cell.destAgent
            path2 = []
            c = cell
            while c in agent.path:
                path2.append([c.location.x, c.location.y])
                c = agent.path[c]
            path2.append([agent.location.x, agent.location.y])

            path1.reverse()
            path3 = path1 + path2[1:]
            path4 = []
            [path4.append(cell) for cell in path3 if cell not in path4]
            path = []
            for cell in path4:
                if len(path) == 0:
                    path.append(cell)
                else:
                    top = path[len(path) - 1]
                    steps = max(abs(top[0] - cell[0]), abs(top[1] - cell[1]))
                    for j in range(steps):
                        x, y = top[0], top[1]
                        if top[0] > cell[0]:
                            x = top[0] - 1 - j
                        if top[1] > cell[1]:
                            y = top[1] - 1 - j
                        if top[0] < cell[0]:
                            x = top[0] + 1 + j
                        if top[1] < cell[1]:
                            y = top[1] + 1 + j
                        path.append([x, y])
            paths.append(path)
        return paths

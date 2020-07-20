from agent import Agent
from environment.env import Environment
from environment.utils import Location


def nonCheckpointMode(dict):
    algo = int(dict['algo'])
    env = Environment(len(dict['maze']), len(dict['maze'][0]))
    env.cutCorners = int(dict['cutCorners'])
    env.allowDiagonals = int(dict['allowDiagonals'])
    sources = []
    destinations = []

    for source in dict['start']:
        sources.append(Agent(Location(source['x'], source['y']), 'source'))
    for destination in dict['stop']:
        destinations.append(Agent(Location(
            destination['x'], destination['y']), 'destination', int(dict['biDirectional'])))

    for checkpoint in dict['checkpoints']:
        if int(dict['multistart'])==1:
            sources.append(
                Agent(Location(checkpoint['x'], checkpoint['y']), 'source', True))
        else:
            destinations.append(
                Agent(Location(checkpoint['x'], checkpoint['y']), 'destination', int(dict['biDirectional'])))

    for agent in sources + destinations:
        env.placeAgent(agent)

    # print(dict['weights'])
    # print(dict)
    maxWeight = 0
    for row in env.grid:
        for cell in row:
            if dict['maze'][cell.location.x][cell.location.y] == 1:
                cell.type = 'wall'
            else:
                maxWeight = max(maxWeight, 100 - dict['weights'][cell.location.x][cell.location.y])
            # print(dict['weights'][cell.location.x][cell.location.y], end = ' ')
        # print()

    # print(dict['weights'])
    # print("EHy")
    # print(dict)
    for row in env.grid:
        for cell in row:
            if dict['maze'][cell.location.x][cell.location.y] != 1:
                cell.weight = (100 - dict['weights'][cell.location.x][cell.location.y]) / maxWeight
                cell.weight *= 2
            # print(cell.weight, end = ' ')
        # print()


    # Remove if statement later
    if 'wormhole' in dict:
        wormhole = dict['wormhole']
        x1, y1, x2, y2 = wormhole[0]['x'], wormhole[0]['y'], wormhole[1]['x'], wormhole[1]['y']
        if x1!=x2 or y1!=y2:
            wormholeEntry = env.grid[x1][y1]
            wormholeExit = env.grid[x2][y2]
            wormholeEntry.location.neighbours = [[x2, y2]]
            wormholeEntry.type = 'wormholeEntry'
            wormholeExit.type = 'wormholeExit'

    
    maxDepth = 1000
    gridChanges = []
    path = []

    #  ------------- Original Driver
    
    if algo != 6 and algo != 7:
        while True:
            logs = []
            for src in sources:
                if algo == 0:
                    src.aStar(env, destinations)
                if algo == 1:
                    src.staticAStar(env, destinations, float(dict['relaxation']))
                if algo == 2:
                    src.dynamicAStar(env, destinations, float(dict['relaxation']), maxDepth)
                if algo == 3:
                    src.beamSearch(env, destinations, int(dict['beamWidth']))
                if algo == 4:
                    src.bestFirstSearch(env, destinations)
                if algo == 5:
                    src.breadthFirstSearch(env)
                if algo == 8:
                    src.depthFirstSearch(env)
                if algo == 9:
                    src.dijkstra(env)
                if algo == 10:
                    src.jumpPointSearch(env, destinations)
                if algo == 11:
                    src.uniformCostSearch(env)
                logs.extend(src.logs)
            for dest in destinations:
                if dest.isMovingAgent:
                    if algo == 0:
                        dest.aStar(env, sources)
                    if algo == 1:
                        dest.staticAStar(env, sources, float(dict['relaxation']))
                    if algo == 2:
                        dest.dynamicAStar(env, destinations, float(dict['relaxation']), maxDepth)
                    if algo == 3:
                        dest.beamSearch(env, sources, int(dict['beamWidth']))
                    if algo == 4:
                        dest.bestFirstSearch(env, sources)
                    if algo == 5:
                        dest.breadthFirstSearch(env)
                    if algo == 8:
                        dest.depthFirstSearch(env)
                    if algo == 9:
                        dest.dijkstra(env)
                    if algo == 10:
                        dest.jumpPointSearch(env, sources)
                    if algo == 11:
                        dest.uniformCostSearch(env)
                logs.extend(dest.logs)
            success, gridChange = env.update(logs)
            # env.print()
            # print(gridChange)
            gridChanges.extend(gridChange)
            if len(success) > 0:
                intersection = success.pop()
                wrapped = set()
                wrapped.add(intersection)
                if algo == 10:
                    paths = env.getJpsPaths(wrapped)
                else:
                    paths = env.getPaths(wrapped)
                path = paths[0]
                # print('Path:', path)
                break
            if len(src.logs) == 0 and len(dest.logs) == 0:
                break
        # print(path)
        activatedCells = env.getActivatedCells()
        output = {'gridChanges': gridChanges,
                  'path': path, 'activatedCells': activatedCells}
        # print(output)
        # print(path)
        return output

    # ----------------------------- Temporary ida and ida* Driver

    else:
        threshold = env.bestHeuristic(sources[0], destinations)
        newThreshold = 50000         # Large Value
        itrCount = 0                 # IterationCount is necessary for tle
        prevPath = [[]]
        while True and itrCount < 1000:
            logs = []
            for src in sources:
                if algo == 6:
                    X, Y = src.ida(env, threshold, destinations)
                if algo == 7:
                    X, Y = src.idaStar(env, threshold, destinations)
                logs.extend(src.logs)
                if X > threshold :
                    newThreshold = min(X, newThreshold)
                else:
                    success, gridChange, prevPath = env.idaupdate(logs, Y, prevPath)        
            gridChanges.extend(gridChange)
            if len(success) > 0:
                paths = env.idaPaths(success, X)
                break
            if len(src.logs) == 0 and len(sources[0].waitList) == 0:
                if newThreshold == 50000:     # No Path exists
                    break
                threshold = newThreshold
                itrCount += 1
                newThreshold = 50000
                for agent in sources + destinations:
                    agent.visited.clear()
                    agent.waitList = None
                    agent.path = {}
                    agent.logs = []
                    agent.distances = {}

        activatedCells = env.getActivatedCells_IDA(paths[0])
        output = {'gridChanges': gridChanges,
                  'path': paths[0], 'activatedCells': activatedCells}
        # print(gridChanges)
        return output

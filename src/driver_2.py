from agent import Agent
from environment.env import Environment
from environment.utils import Location


def driver(dict):
    # Create environment
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
        destinations.append(
            Agent(Location(checkpoint['x'], checkpoint['y']), 'destination', False))
    for agent in sources + destinations:
        env.placeAgent(agent)

    for row in env.grid:
        for cell in row:
            # print(' ',cell.location.x, cell.location.y)
            if dict['maze'][cell.location.x][cell.location.y] == 1:
                cell.type = 'wall'

    beamWidth = int(dict['beamWidth'])
    gridChanges = []
    path = []

    #  ------------- Original Driver
    algo = int(dict['algo'])
    if algo != 6 and algo != 7:
        while True:
            logs = []
            for src in sources:
                if algo == 0:
                    src.aStar(env, destinations)
                if algo == 1:
                    src.beamSearch(env, destinations, beamWidth)
                if algo == 2:
                    src.bestFirstSearch(env, destinations)
                if algo == 3:
                    src.breadthFirstSearch(env)
                if algo == 4:
                    src.depthFirstSearch(env)
                if algo == 5:
                    src.dijkstra(env)
                if algo == 8:
                    src.jumpPointSearch(env, destinations)
                logs.extend(src.logs)
            for dest in destinations:
                if dest.isMovingAgent:
                    if algo == 0:
                        dest.aStar(env, sources)
                    if algo == 1:
                        dest.beamSearch(env, sources, beamWidth)
                    if algo == 2:
                        dest.bestFirstSearch(env, sources)
                    if algo == 3:
                        dest.breadthFirstSearch(env)
                    if algo == 4:
                        dest.depthFirstSearch(env)
                    if algo == 5:
                        dest.dijkstra(env)
                    if algo == 8:
                        dest.jumpPointSearch(env, sources)
                logs.extend(dest.logs)
            success, gridChange = env.update(logs)
            # env.print()
            # print(gridChange)
            gridChanges.extend(gridChange)
            if len(success) > 0:
                intersection = success.pop()
                wrapped = set()
                wrapped.add(intersection)
                if algo == 8:
                    paths = env.getJpsPaths(wrapped)
                else:
                    paths = env.getPaths(wrapped)
                path = paths[0]
                # print('Path:', path)
                break
            if len(src.logs) == 0 and len(dest.logs) == 0:
                break
        # print(path)
        output = {'gridChanges': gridChanges, 'path': path}
        # print(output)
        return output

    # ----------------------------- Temporary ida and ida* Driver

    else:
        threshold = env.bestHeuristic(sources[0], destinations)
        newThreshold = 50000         # Large Value
        itrCount = 0                 # IterationCount is necessary for tle
        while True and itrCount < 1000:
            logs = []
            for src in sources:
                if algo == 6:
                    X = src.ida(env, threshold, destinations)
                if algo == 7:
                    X = src.idaStar(env, threshold, destinations)
                if type(X) == int and X > threshold:
                    newThreshold = min(X, newThreshold)
                logs.extend(src.logs)
            success = env.update(logs)
            # env.print()
            if len(success) > 0:
                paths = env.tmpPaths(success, threshold)
                # print('Paths:', paths)
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


# dict = {
#     "algo": 2,
#     "start": [{"x": 3, "y": 4}],
#     "stop": [{"x": 3, "y": 23}],
#     "cutCorners": 0,
#     "allowDiagonals": 1,
#     "biDirectional": 0,
#     "beamWidth": 2,
#     "checkpoints": [
#         # {"x":9,"y":7},
#         # {"x":8,"y":7},
#         # {"x":7,"y":7},
#         # {"x":6,"y":7},
#         # {"x":5,"y":7}
#     ],
#     "maze":
#     [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     ]
# }

# driver(dict)

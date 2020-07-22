from agent import Agent
from environment.env import Environment
from environment.utils import Location


def nonCheckpointMode(config):
    
    sources = []
    destinations = []

    for source in config['start']:
        sources.append(Agent(Location(source['x'], source['y']), 'source'))
    for destination in config['stop']:
        destinations.append(Agent(Location(destination['x'], destination['y']), 'destination', int(config['biDirectional'])))

    for checkpoint in config['checkpoints']:
        if int(config['multistart'])==1:
            sources.append(Agent(Location(checkpoint['x'], checkpoint['y']), 'source', True))
        else:
            destinations.append(Agent(Location(checkpoint['x'], checkpoint['y']), 'destination', int(config['biDirectional'])))

    env = Environment(config, sources + destinations)

    
    maxDepth = 1000
    gridChanges = []
    path = []
    algo = int(config['algo'])
    
    if algo != 6 and algo != 7:
        while True:
            logs = []
            for src in sources:
                if algo == 0:
                    src.aStar(env, destinations)
                if algo == 1:
                    src.staticAStar(env, destinations, float(config['relaxation']))
                if algo == 2:
                    src.dynamicAStar(env, destinations, float(config['relaxation']), maxDepth)
                if algo == 3:
                    src.beamSearch(env, destinations, int(config['beamWidth']))
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
                        dest.staticAStar(env, sources, float(config['relaxation']))
                    if algo == 2:
                        dest.dynamicAStar(env, destinations, float(config['relaxation']), maxDepth)
                    if algo == 3:
                        dest.beamSearch(env, sources, int(config['beamWidth']))
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
            intersectionPts, gridChange = env.update(logs)
            # env.print()
            # print(gridChange)
            gridChanges.extend(gridChange)
            if len(intersectionPts) > 0:
                intersectionPt = intersectionPts.pop()
                if algo == 10:
                    path = env.getJpsPath(intersectionPt)
                else:
                    path = env.getPath(intersectionPt)
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

    else:
        threshold = env.bestHeuristic(sources[0], destinations)
        newThreshold = 50000         # Large Value
        itrCount = 0                 # IterationCount is necessary for tle
        prevPath = []
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
                    intersectionPts, gridChange, prevPath = env.idaupdate(logs, Y, prevPath)        
            gridChanges.extend(gridChange)
            if len(intersectionPts) > 0:
                intersectionPt = intersectionPts.pop()
                path = env.getIDAPath(intersectionPt)
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

        activatedCells = env.getActivatedCells_IDA(path)
        print(path)
        output = {'gridChanges': gridChanges,
                  'path': path, 'activatedCells': activatedCells}
        # print(gridChanges)
        return output

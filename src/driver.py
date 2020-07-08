from agent import Agent
from environment.env import Environment
from environment.utils import Location

# Create environment
env = Environment(7, 7)
env.cutCorners = False
env.allowDiagonals = True
sources = [Agent(Location(4, 4), 'source')]
destinations = [Agent(Location(6, 2), 'destination', True)]
# Agent(Location(0, 0), 'destination', False)]
for agent in sources + destinations:
    env.placeAgent(agent)

# walls = env.recursiveMaze()
# env.randomizedPrim()

# env.print()
# for i in range(1,9):
    # env.grid[i][6].type = 'wall'
env.grid[6][1].type = 'wall'
# env.grid[6][8].type = 'wall'
# env.grid[5][9].type = 'wall'
# env.grid[7][9].type = 'wall'
# env.grid[1][8].type = 'wall'
# env.grid[2][1].type = 'wall'
# env.grid[1][1].type = 'wall'
# env.grid[0][1].type = 'wall'

# env.printInitial()
# env.grid[2][0].weight = 100
beamWidth = 2

#  ------------- Original Driver

while True:
    logs = []
    for src in sources:
        # src.depthFirstSearch(env)
        src.breadthFirstSearch(env)
        # src.aStar(env, destinations)
        # src.beamSearch(env, destinations, beamWidth)
        # src.jumpPointSearch(env, destinations)
        logs.extend(src.logs)
    for dest in destinations:
        if dest.isMovingAgent:
            # dest.depthFirstSearch(env)
            dest.breadthFirstSearch(env)
            # src.aStar(env, sources)
            # dest.beamSearch(env, destinations, beamWidth)
            # dest.jumpPointSearch(env, sources)
            logs.extend(dest.logs)
    success = env.update(logs)
    env.print()
    if len(success) > 0:
        # paths = env.getPaths(success)
        paths = env.getPaths(success)
        print('Paths:', paths)
        break
    if len(src.logs) == 0 and len(dest.logs) == 0:
        break


# ----------------------------- Temporary ida and ida* Driver


# threshold = env.bestHeuristic(sources[0], destinations)
# # threshold = 1
# newThreshold = 50000         # Large Value
# itrCount = 0                 # IterationCount is necessary for tle
# while True and itrCount < 1000:
#     logs = []
#     for src in sources:
#         # X = src.idaStar(env, threshold, destinations)
#         X = src.ida(env, threshold, destinations)
#         if type(X) == int and X > threshold :
#             # print(newThreshold)
#             newThreshold = min(X, newThreshold)
#         logs.extend(src.logs)
#     for dest in destinations:
#         if dest.isMovingAgent:
#             dest.depthFirstSearch(env)
#             # dest.bestFirstSearch(env, sources)
#             # src.aStar(env, sources)
#             logs.extend(dest.logs)
#     success = env.update(logs)
#     # env.print()
#     if len(success) > 0:
# #         paths = env.getPaths(success)
#         paths = env.tmpPaths(success, threshold)
#         print('Paths:', paths)
#         break
#     if len(src.logs) == 0 and len(dest.logs) == 0 and len(sources[0].waitList) == 0:
#         if newThreshold == 50000:     # No Path exists
#             break;
#         threshold = newThreshold
#         print('newThreshold', newThreshold)
#         itrCount += 1
#         newThreshold = 50000
#         for agent in sources + destinations:
#             agent.visited.clear()
#             agent.waitList = None
#             agent.path = {}
#             agent.logs = []
#             agent.distances = {}

from agent import Agent
from environment.env import Environment
from environment.utils import Location

# Create environment
env = Environment(10, 10)
sources = [Agent(Location(9, 9), 'source')]
destinations = [Agent(Location(0, 0), 'destination', False)]
                # Agent(Location(0, 0), 'destination', False)]
for agent in sources + destinations:
    env.placeAgent(agent)

walls = env.recursiveMaze()
# env.randomizedPrim()

# env.print()
# for i in range(5):
#     if i == 4:
#         continue
#     env.grid[1][i].type = 'wall'
# env.grid[4][6].type = 'wall'
# env.grid[2][6].type = 'wall'
# env.grid[1][6].type = 'wall'
# env.grid[1][7].type = 'wall'
# env.grid[1][8].type = 'wall'
# env.grid[2][1].type = 'wall'

env.printInitial()
# env.grid[2][0].weight = 100
beamWidth = 2

#  ------------- Original Driver

while True:
    logs = []
    for src in sources:
        # src.depthFirstSearch(env)
        # src.bestFirstSearch(env, destinations)
        # src.aStar(env, destinations)
        # src.beamSearch(env, destinations, beamWidth)
        src.jumpPointSearch(env, destinations)
        logs.extend(src.logs)
    for dest in destinations:
        if dest.isMovingAgent:
            # dest.depthFirstSearch(env)
            # dest.bestFirstSearch(env, sources)
            # src.aStar(env, sources)
            # dest.beamSearch(env, destinations, beamWidth)
            dest.jumpPointSearch(env, sources)
            logs.extend(dest.logs)
    success = env.update(logs)
    # env.print()
    if len(success) > 0:
        # paths = env.getPaths(success)
        paths = env.getJpsPaths(success)
        print('Paths:', paths)
        break
    if len(src.logs) == 0 and len(dest.logs) == 0:
        break


# ----------------------------- Temporary ida* Driver


# threshold = env.bestHeuristic(sources[0], destinations)
# newThreshold = 50000         # Large Value
# itrCount = 0                 # IterationCount is necessary for tle ( also for dfs ? )
# while True and itrCount < 10:
#     logs = []
#     for src in sources:
#         X = src.idaStar(env, threshold, destinations)
#         if type(X) == int and X > threshold :
#             newThreshold = min(X, newThreshold)
#         logs.extend(src.logs)
#     for dest in destinations:
#         if dest.isMovingAgent:
#             dest.depthFirstSearch(env)
#             # dest.bestFirstSearch(env, sources)
#             # src.aStar(env, sources)
#             logs.extend(dest.logs)
#     success = env.update(logs)
#     env.print()
#     if len(success) > 0:
#         paths = env.getPaths(success)
#         print('Paths:', paths)
#         break
#     if len(src.logs) == 0 and len(dest.logs) == 0 and len(sources[0].waitList) == 0:
#         threshold = newThreshold
#         itrCount += 1
#         newThreshold = 50000
#         for agent in sources + destinations:
#             agent.visited.clear()
#             agent.waitList = None
#             agent.path = {}
#             agent.logs = []
#             agent.distances = {}

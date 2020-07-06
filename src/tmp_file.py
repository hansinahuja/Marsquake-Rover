from agent import Agent
from environment.env import Environment
from environment.utils import Location

# Create environment
env = Environment(5, 5)
sources = [Agent(Location(3, 4), 'source')]
destinations = [Agent(Location(3, 0), 'destination', False)]
for agent in sources + destinations:
    env.placeAgent(agent)

# Temporary ida* driver, currently for single node, destination
# Each source has a threshold
threshold = env.bestHeuristic(sources[0], destinations)
newThreshold = 50000
itrCount = 0
while True and itrCount < 10:
    logs = []
    for src in sources:
        X = src.idaStar(env, threshold, destinations)
        if type(X) == int :
            newThreshold = min(src.idaStar(env, threshold, destinations), newThreshold)
        logs.extend(src.logs)
    for dest in destinations:
        if dest.isMovingAgent:
            dest.depthFirstSearch(env)
            # dest.bestFirstSearch(env, sources)
            # src.aStar(env, sources)
            logs.extend(dest.logs)
    success = env.update(logs)
    env.print()
    if len(success) > 0:
        paths = env.getPaths(success)
        print('Paths:', paths)
        break
    if len(src.logs) == 0 and len(dest.logs) == 0:
        threshold = newThreshold
        itrCount += 1
from agent import Agent
from environment.env import Environment
from environment.utils import Location

# Create environment
env = Environment(5, 5)
sources = [Agent(Location(1, 1), 'source')]
destinations = [Agent(Location(4, 4), 'destination', False)]
for agent in sources + destinations:
    env.placeAgent(agent)

# walls = env.recursiveMaze()
# env.randomizedPrim()

# env.printInitial() 
env.grid[2][2].type = 'wall'
# env.grid[2][3].type = 'wall'
# env.grid[2][4].type = 'wall'

while True:
    logs = []
    for src in sources:
        src.dfs(env)
        logs.extend(src.logs)
    for dest in destinations:
        if dest.isMovingAgent:
            dest.dfs(env)
            logs.extend(dest.logs)
    success = env.update(logs)
    env.print()
    if len(success) > 0:
        paths = env.getPaths(success)
        print('Paths:', paths)
        break
    if len(src.logs)==0 and len(dest.logs)==0:
        break
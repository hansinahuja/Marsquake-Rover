import time
from agent import Agent
from environment.env import Environment
from environment.utils import Location


def nonCheckpointMode(config):

    """
    Simulates path-finding in multistart and multidestination mode.
    Args:
        config: Dictionary with all the configuration settings.
    Returns:
        output: Final path taken and list of changes on the grid.
    """

    # Register starting time
    startTime = time.time()

    # Extract all the sources and destinations from config
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

    # Initialise the environment
    env = Environment(config, sources + destinations)

    gridChanges = []
    path = []
    algo = int(config['algo'])
    
    # For all algorithms other than IDA*
    if algo != 6:

        # Run till a path is found
        while True:
            logs = []

            # Run the correct algorithm for all the movable agents and log the changes
            for agent in sources + destinations:
                targets = destinations if agent in sources else sources
                if agent.isMovingAgent: 
                    if algo == 0:
                        agent.aStar(env, targets)
                    if algo == 1:
                        agent.staticAStar(env, targets, float(config['relaxation']))
                    if algo == 2:
                        agent.dynamicAStar(env, targets, float(config['relaxation']), 1000)
                    if algo == 3:
                        agent.beamSearch(env, targets, int(config['beamWidth']))
                    if algo == 4:
                        agent.bestFirstSearch(env, targets)
                    if algo == 5:
                        agent.breadthFirstSearch(env)
                    if algo == 7:
                        agent.depthFirstSearch(env)
                    if algo == 8:
                        agent.dijkstra(env)
                    if algo == 9:
                        agent.jumpPointSearch(env, targets)
                    if algo == 10:
                        agent.uniformCostSearch(env)
                    logs.extend(agent.logs)

            # Update grid and check for intersection points
            intersectionPts, gridChange = env.update(logs)
            gridChanges.extend(gridChange)

            # If intersection point found, get final path and break
            if len(intersectionPts) > 0:
                intersectionPt = intersectionPts.pop()
                if algo == 9:
                    path = env.getJpsPath(intersectionPt)
                else:
                    path = env.getPath(intersectionPt)
                break

            # If no changes being registered, break
            if len(logs) == 0:
                break
        
        # Get currently activated cells for grid cleanup
        activatedCells = env.getActivatedCells()

        # Calculate time taken in milliseconds and return output
        timeTaken = int((time.time() - startTime)*1000)
        output = {'gridChanges': gridChanges,
                  'path': path, 
                  'activatedCells': activatedCells, 
                  'timeTaken': timeTaken}

        # Do not return activated cells if called by findPath()
        if int(config['multistart']) != 0 or int(config['multidest']) != 0:
            del output['activatedCells']

        return output

    # Driver for IDA*
    else:
        
        # Initialize the threshold and other required variables
        threshold = env.bestHeuristic(sources[0], destinations)
        maxThreshold = 2 * env.length * env.breadth
        newThreshold = maxThreshold     
        t_end = time.time() + 1
        prevPath = []
        while time.time() <= t_end:
            logs = []
            # Run the algorithm for all the movable agents and log the changes
            for src in sources:
                X, Y = src.idaStar(env, threshold, destinations)
                logs.extend(src.logs)
                if X > threshold :
                    newThreshold = min(X, newThreshold)
                else:
                    # Update grid and check if destination is reached
                    destinationPts , gridChange, prevPath = env.idaUpdate(logs, Y, prevPath)        
            gridChanges.extend(gridChange)

            # If reached destination, get final path and break
            if len(destinationPts) > 0:
                destinationPt = destinationPts.pop()
                path = env.getIDAPath(destinationPt)
                break

            # Otherwise update threshold if possible
            if len(src.logs) == 0 and len(sources[0].waitList) == 0:

                # Updating threshold not possible, no path exists
                if newThreshold == maxThreshold:     
                    break

                # Update threshold
                threshold = newThreshold
                newThreshold = maxThreshold
                for agent in sources + destinations:
                    agent.visited.clear()
                    agent.waitList = None
                    agent.path = {}
                    agent.logs = []
                    agent.distances = {}

        # Get currently activated cells for grid cleanup
        activatedCells = env.getActivatedCells_IDA(path)

        # Calculate time taken in milliseconds
        timeTaken = int((time.time() - startTime)*1000)


        output = {'gridChanges': gridChanges,
                  'path': path, 
                  'activatedCells': activatedCells, 
                  'timeTaken': timeTaken}

        # Do not return activated cells if called by findPath()
        if int(config['multistart']) != 0 or int(config['multidest']) != 0:
            del output['activatedCells']

        return output
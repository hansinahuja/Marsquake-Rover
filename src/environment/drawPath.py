def getPath(self, intersectionPt):

    """
    Gets the final path from source to destination.
    Args:
        intersectionPt: Point at which the source and destination meet.
    Returns:
        path: Path taken by agents to meet each other.
    """

    # Create path from source to intersection point by following parent cells.
    srcToIntersection = []
    agent = intersectionPt.srcAgent
    curr = intersectionPt
    while curr in agent.path:
        entry = {'x': curr.location.x, 'y': curr.location.y}
        srcToIntersection.append(entry)
        curr = agent.path[curr]
    entry = {'x': agent.location.x, 'y': agent.location.y}
    srcToIntersection.append(entry)

    # Create path from destination to intersection point by following parent cells.
    agent = intersectionPt.destAgent
    destToIntersection = []
    curr = intersectionPt
    while curr in agent.path:
        entry = {'x': curr.location.x, 'y': curr.location.y}
        destToIntersection.append(entry)
        curr = agent.path[curr]
    entry = {'x': agent.location.x, 'y': agent.location.y}
    destToIntersection.append(entry)

    # Join the two paths
    srcToIntersection.reverse()
    path = srcToIntersection + destToIntersection[1:]

    # Find out if a wormhole was taken 
    wormholeOutIndex = -1
    for i in range(1, len(path)):
        x1, y1 = path[i-1]['x'], path[i-1]['y']
        x2, y2 = path[i]['x'], path[i]['y']
        cell1, cell2 = self.grid[x1][y1], self.grid[x2][y2]
        if cell1.type == 'wormholeEntry' and cell2.type == 'wormholeExit':
            wormholeOutIndex = i
            break
        if cell2.type == 'wormholeEntry' and cell1.type == 'wormholeExit':
            wormholeOutIndex = i
            break


    # If wormhole was taken, add an indicator entry
    if wormholeOutIndex != -1:
        srcToIntersection = path[:wormholeOutIndex]
        destToIntersection = path[wormholeOutIndex:]
        buffer = {'x': -1, 'y': -1}
        path = srcToIntersection + [buffer] + destToIntersection

    return path

def getIDAPath(self, destination):                          

    """
    Gets the final path from source to destination for IDA*.
    Args:
        destination: destination point.
    Returns:
        path: Path taken by source agent to get to destination.
    """

    path = []
    agent = destination.srcAgent
    cell = destination
    weight = 0
    
    # Get the weight of the destination cell
    for point in agent.path:
        if point[0] == cell:
            cell = point[0]
            weight = point[1]

    # Create the path by following parent cell
    while (cell, weight) in agent.path:
        entry = {'x': cell.location.x, 'y': cell.location.y}
        path.append(entry)
        nextCell = agent.path[(cell, weight)]
        cell = nextCell[0]
        weight = nextCell[1]

    entry = {'x': agent.location.x, 'y': agent.location.y}
    path.append(entry)
    path.reverse()

    # Find out if a wormhole was taken 
    wormholeOutIndex = -1
    for i in range(1, len(path)):
        x1, y1 = path[i-1]['x'], path[i-1]['y']
        x2, y2 = path[i]['x'], path[i]['y']
        cell1, cell2 = self.grid[x1][y1], self.grid[x2][y2]
        if cell1.type == 'wormholeEntry' and cell2.type == 'wormholeExit':
            wormholeOutIndex = i
            break
        if cell2.type == 'wormholeEntry' and cell1.type == 'wormholeExit':
            wormholeOutIndex = i
            break

    # If wormhole was taken, add an indicator entry
    if wormholeOutIndex != -1:
        srcToIntersection = path[:wormholeOutIndex]
        destToIntersection = path[wormholeOutIndex:]
        buffer = {'x': -1, 'y': -1}
        path = srcToIntersection + [buffer] + destToIntersection

    return path


def getJpsPath(self, intersectionPt): 

    """
    Gets the final path from source to destination for jump point search.
    Args:
        intersectionPt: Point at which the source and destination meet.
    Returns:
        path: Path taken by agents to meet each other.
    """

    srcToIntersection = []
    agent = intersectionPt.srcAgent
    currentCell = intersectionPt

    # Get the current direction
    directions = ['right', 'left', 'up', 'down',
                    'right-up', 'right-down', 'left-up', 'left-down']
    for direction in directions:
        if (currentCell, direction) in agent.path:
            currentDirection = direction

    # Create path from source to intersection point by following parent cells.
    while (currentCell, currentDirection) in agent.path:
        srcToIntersection.append([currentCell.location.x, currentCell.location.y])
        nextCell = agent.path[(currentCell, currentDirection)]
        currentDirection = nextCell[1]
        currentCell = nextCell[0]
    srcToIntersection.append([agent.location.x, agent.location.y])

    # Create path from destination to intersection point by following parent cells.
    destToIntersection = []
    agent = intersectionPt.destAgent
    currentCell = intersectionPt
    for direction in directions:
        if (currentCell, direction) in agent.path:
            currentDirection = direction
    while (currentCell, currentDirection) in agent.path:
        destToIntersection.append([currentCell.location.x, currentCell.location.y])
        nextCell = agent.path[(currentCell, currentDirection)]
        currentDirection = nextCell[1]
        currentCell = nextCell[0]
    destToIntersection.append([agent.location.x, agent.location.y])

    # Join the two paths and remove duplicates
    srcToIntersection.reverse()
    path1 = srcToIntersection + destToIntersection
    path2 = []
    [path2.append(cell) for cell in path1 if cell not in path2]
    path = []

    # Join non adjacent cells
    for cell in path2:
        if len(path) == 0:
            entry = {'x': cell[0], 'y': cell[1]}
            path.append(entry)
        else:
            top = path[len(path) - 1]
            print(top)
            steps = max(abs(top['x'] - cell[0]), abs(top['y'] - cell[1]))
            for j in range(steps):
                x, y = top['x'], top['y']
                if top['x'] > cell[0]:
                    x = top['x'] - 1 - j
                if top['y'] > cell[1]:
                    y = top['y'] - 1 - j
                if top['x'] < cell[0]:
                    x = top['x'] + 1 + j
                if top['y'] < cell[1]:
                    y = top['y'] + 1 + j
                entry = {'x': x, 'y': y}
                path.append(entry)

    return path


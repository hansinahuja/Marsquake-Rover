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

    # If wormhole was taken, add an indicator entry
    if wormholeOutIndex != -1:
        srcToIntersection = path[:wormholeOutIndex]
        destToIntersection = path[wormholeOutIndex:]
        buffer = {'x': -1, 'y': -1}
        path = srcToIntersection + [buffer] + destToIntersection

    return path

def idaPaths(self, success, weight):                          # For idaStar and ida
    paths = []
    for cell in success:
        path1 = []
        agent = cell.srcAgent
        c = cell
        wt = weight
        while (c, wt) in agent.path:
            entry = {'x': c.location.x, 'y': c.location.y}
            path1.append(entry)
            X = agent.path[(c, wt)]
            c = X[0]
            wt = X[1]
        entry = {'x': agent.location.x, 'y': agent.location.y}
        path1.append(entry)
        path1.reverse()
        paths.append(path1)
    return paths

def getJpsPath(self, intersectionPt):

    path1 = []
    agent = intersectionPt.srcAgent
    c = intersectionPt
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

    agent = intersectionPt.destAgent
    path2 = []
    c = intersectionPt
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

    dictPath = []
    for cell in path:
        entry = {'x': cell[0], 'y': cell[1]}
        dictPath.append(entry)
    return dictPath


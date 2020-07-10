def switchLevel(level, beamWidth):
    newLevel = []
    fValues = {}
    for fValue, cell in level:
        if cell not in fValues or fValues[cell] > fValue:
            fValues[cell] = fValue

    for cell, fValue in fValues.items():
        newLevel.append((fValue, cell))

    newLevel.sort()
    newLevel = newLevel[:beamWidth]
    newLevel.reverse()
    return newLevel


def beamSearch(self, environment, targets, beamWidth):

    self.logs = []

    # First iteration
    if self.waitList == None:
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList = [
            [(environment.bestHeuristic(sourceCell, targets), sourceCell)], []]
        self.distances[sourceCell] = 0

    # Exhausted all possible moves
    if len(self.waitList) == 0:
        return

    currentLevel, nextLevel = self.waitList
    if len(currentLevel) == 0:
        currentLevel, nextLevel = switchLevel(nextLevel, beamWidth), []
        for _, cell in currentLevel:
            self.logs.append([self, cell, 'waitList'])
            # print(cell.location.x, cell.location.y, 'waitList')

    if len(currentLevel) == 0:
        self.waitList = [currentLevel, nextLevel]
        return

    minElement = currentLevel.pop()
    nextCell = minElement[1]
    self.visited.add(nextCell)
    self.logs.append([self, nextCell, 'visited'])
    # print(nextCell.location.x, nextCell.location.y, 'visited')

    for nx, ny in nextCell.location.neighbours:
        if not self.isValidMove(environment, nextCell, nx, ny):
            continue
        neighbour = environment.grid[nx][ny]
        newDistance = self.distances[nextCell] + neighbour.weight
        fValue = newDistance + environment.bestHeuristic(neighbour, targets)
        if neighbour in self.distances and self.distances[neighbour] <= newDistance:
            continue
        nextLevel.append((fValue, neighbour))
        self.path[neighbour] = nextCell
        self.distances[neighbour] = newDistance

    self.waitList = [currentLevel, nextLevel]

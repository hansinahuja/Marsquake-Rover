def switchLevel(level, beamWidth):

    """
    Switches the level in focus to the next level
    Args:
        level: The next beam level
        beamWidth: maximum allowable width of beam to limit space complexity
    Returns:
        newLevel: The new beam level in focus.
    """

    newLevel = []

    # Get the smallest heuristics in case of clashes
    fValues = {}
    for fValue, cell in level:
        if cell not in fValues or fValues[cell] > fValue:
            fValues[cell] = fValue

    # Create the new level and limit space complexity
    for cell, fValue in fValues.items():
        newLevel.append((fValue, cell))
    newLevel.sort()
    newLevel = newLevel[:beamWidth]
    newLevel.reverse()
    return newLevel


def beamSearch(self, environment, targets, beamWidth):

    """
    Performs one iteration of beam search based on agent's current state.
    Args:
        environment: The current environment
        targets: The target agents
        beamWidth: maximum allowable width of beam to limit space complexity
    """
    
    # Clean the logs
    self.logs = []

    # First iteration
    if self.waitList == None:
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList = [[(environment.bestHeuristic(sourceCell, targets), sourceCell)], []]
        self.distances[sourceCell] = 0

    # Exhausted all possible moves
    if len(self.waitList) == 0:
        return

    # If current level is exhaustem, switch the levels and log the changes
    currentLevel, nextLevel = self.waitList
    if len(currentLevel) == 0:
        currentLevel, nextLevel = switchLevel(nextLevel, beamWidth), []
        for _, cell in currentLevel:
            self.logs.append([self, cell, 'waitList'])

    # No more possible moves
    if len(currentLevel) == 0:
        self.waitList = [currentLevel, nextLevel]
        return

    # Pop the next element and log the changes
    minElement = currentLevel.pop()
    nextCell = minElement[1]
    self.visited.add(nextCell)
    self.logs.append([self, nextCell, 'visited'])

    # Iterate over valid neighbours
    for nx, ny in nextCell.location.neighbours:

        if not self.isValidMove(environment, nextCell, nx, ny):
            continue

        # Calculate heuristic and check if a better path is possible
        neighbour = environment.grid[nx][ny]
        newDistance = self.distances[nextCell] + environment.distance(nextCell, neighbour)
        fValue = newDistance + environment.bestHeuristic(neighbour, targets)
        if neighbour in self.distances and self.distances[neighbour] <= newDistance:
            continue

        # Add neighbour to the queue and log the changes
        nextLevel.append((fValue, neighbour))
        self.path[neighbour] = nextCell
        self.distances[neighbour] = newDistance

    self.waitList = [currentLevel, nextLevel]

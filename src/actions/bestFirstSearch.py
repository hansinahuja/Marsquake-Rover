import heapq

def bestFirstSearch(self, environment, targets):

    """
    Performs one iteration of best first search based on agent's current state.
    Args:
        environment: The current environment
        targets: The target agents
    """

    # Clean the logs
    self.logs = []

    # First iteration
    if self.waitList == None:
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList = [(environment.bestHeuristic(
            sourceCell, targets), sourceCell)]
        self.distances[sourceCell] = 0

    # Exhausted all possible moves
    if len(self.waitList) == 0:
        return

    # Pop the top element and log the changes
    minElement = heapq.heappop(self.waitList)
    nextCell = minElement[1]
    self.visited.add(nextCell)
    self.logs.append([self, nextCell, 'visited'])

    # Iterate over valid neighbours
    for nx, ny in nextCell.location.neighbours:

        if not self.isValidMove(environment, nextCell, nx, ny):
            continue

        # Check if a better path is possible
        neighbour = environment.grid[nx][ny]
        newDistance = environment.bestHeuristic(neighbour, targets)
        if neighbour in self.distances and self.distances[neighbour] <= newDistance:
            continue
        
        # Add the neighbour to the heap and log the changes
        heapq.heappush(self.waitList, (newDistance, neighbour))
        self.path[neighbour] = nextCell
        self.distances[neighbour] = newDistance
        self.logs.append([self, neighbour, 'waitList'])

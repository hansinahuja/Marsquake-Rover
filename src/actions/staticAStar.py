import heapq

def staticAStar(self, environment, targets, relaxation):

    """
    Performs one iteration of statically weighted A* based on agent's current state.
    Args:
        environment: The current environment
        targets: The target agents
        relaxation: relaxation factor to calculate heuristics
    """

    # Clean the logs
    self.logs = []

    # First iteration
    if self.waitList == None:
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList = [((1 + relaxation) * environment.bestHeuristic(sourceCell, targets), sourceCell)]
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

        # Calculate heuristic and check if a better path is possible
        neighbour = environment.grid[nx][ny]
        newDistance = self.distances[nextCell] + environment.distance(nextCell, neighbour)
        fValue = newDistance + (1 + relaxation) * environment.bestHeuristic(neighbour, targets)
        if neighbour in self.distances and self.distances[neighbour] <= newDistance:
            continue

        # Add neighbour to the heap and log the changes
        self.distances[neighbour] = newDistance
        heapq.heappush(self.waitList, (fValue, neighbour))
        self.path[neighbour] = nextCell
        self.logs.append([self, neighbour, 'waitList'])

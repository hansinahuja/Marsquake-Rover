import heapq

def dijkstra(self, environment):

    """
    Performs one iteration of Dijkstra's algorithm based on agent's current state.
    Args:
        environment: The current environment
    """

    # Clean the logs
    self.logs = []

    # First iteration
    if self.waitList == None:
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList = [(0, sourceCell)]
        self.distances[sourceCell] = 0

    # Exhausted all possible moves
    if len(self.waitList) == 0:
        return

    # Pop the minimum element and log the changes
    minElement = heapq.heappop(self.waitList)
    nextCell = minElement[1]
    self.logs.append([self, nextCell, 'visited'])


    # Iterate over valid neighbours
    for nx, ny in nextCell.location.neighbours:

        if not self.isValidMove(environment, nextCell, nx, ny, False):
            continue

        # Check if a better path is possible
        neighbour = environment.grid[nx][ny]
        newDistance = self.distances[nextCell] + environment.distance(nextCell, neighbour)
        if neighbour in self.distances and self.distances[neighbour] <= newDistance:
            continue

        # Add neighbour to the heap and log the changes
        heapq.heappush(self.waitList, (newDistance, neighbour))
        self.path[neighbour] = nextCell
        self.distances[neighbour] = newDistance
        self.logs.append([self, neighbour, 'waitList'])

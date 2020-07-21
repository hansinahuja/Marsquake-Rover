from collections import deque

def breadthFirstSearch(self, environment):

    """
    Performs one iteration of breadth first search based on agent's current state.
    Args:
        environment: The current environment
    """

    # Clean the logs
    self.logs = []

    # First iteration
    if self.waitList == None:
        self.waitList = deque()
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.waitList.append(sourceCell)
        self.visited.add(sourceCell)

    # Exhausted all possible moves
    if len(self.waitList) == 0:
        return

    # Pop the next element and log the changes
    nextCell = self.waitList.popleft()
    self.logs.append([self, nextCell, 'visited'])

    # Iterate over valid neighbours
    for nx, ny in nextCell.location.neighbours:

        if not self.isValidMove(environment, nextCell, nx, ny):
            continue

        # Add the neighbour to the queue and log the changes
        neighbour = environment.grid[nx][ny]
        self.waitList.append(neighbour)
        self.path[neighbour] = nextCell
        self.visited.add(neighbour)
        self.logs.append([self, neighbour, 'waitList'])

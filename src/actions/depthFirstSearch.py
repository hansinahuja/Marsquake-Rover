from collections import deque

def depthFirstSearch(self, environment):

    """
    Performs one iteration of depth first search based on agent's current state.
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
        self.visited = {}

    # Exhausted all possible moves
    if len(self.waitList) == 0:
        return

    # Get the next element from the stack
    nextCell = self.waitList[-1]

    # If already visited, take it off the recursion stack
    if nextCell in self.visited:
        self.waitList.pop()
        if self.visited[nextCell] == 'inRecursion':
            self.visited[nextCell] = 'outOfRecursion'
            self.logs.append([self, nextCell, 'outOfRecursion'])

        # To allow recursion stack to become empty 
        self.logs.append(None)
        return

    # If first visit, add the cell in recursion stack
    self.visited[nextCell] = 'inRecursion'
    self.logs.append([self, nextCell, 'inRecursion'])

    
    # Iterate over valid neighbours
    for nx, ny in nextCell.location.neighbours:
        if not self.isValidMove(environment, nextCell, nx, ny):
            continue

        # Add neighbour to the stack
        neighbour = environment.grid[nx][ny]
        self.waitList.append(neighbour)
        self.path[neighbour] = nextCell

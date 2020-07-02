from collections import deque

def bfs(self, environment):

    self.logs = []

    # First iteration
    if self.queue == None:
        self.queue = deque()
        sourceCell = environment.grid[self.location.x][self.location.y]
        self.queue.append(sourceCell)
        self.visited.add(sourceCell)

    # Exhausted all possible moves
    if len(self.queue)==0:
        return

    nextCell = self.queue.popleft()
    self.logs.append([self, nextCell, 'visited'])
    # print(nextCell.location.x, nextCell.location.y, 'visited')

    for nx, ny in nextCell.location.neighbours:
        if not self.isValidMove(environment, nx, ny):
            continue
        neighbour = environment.grid[nx][ny]
        self.queue.append(neighbour)
        self.path[neighbour] = nextCell
        self.visited.add(neighbour)
        self.logs.append([self, neighbour, 'inQueue'])
        # print(neighbour.location.x, neighbour.location.y, 'inQueue')




    
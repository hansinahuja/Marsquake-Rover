# Marsquake-Rover

## Features

### Supported algorithms

Here is a summary of all the algorithms we support:

| Algorithm  | Shortest path guaranteed | Informed search | For weighted graphs | Bidirectional | Supports wormholes |
| :-------------: | :-------------: | :-------------: | :-------------: | :-----------: | :-------: |
| A*  | ✓  | ✓ | ✓ |  ✓ | ✓ |
| Statically Weighted A*  | ✗  | ✓ | ✓ | ✓ | ✓ |
| Dynamically Weighted A*  | ✗  | ✓ | ✓ | ✓ | ✓ |
| Beam Search  | ✗  | ✗ | ✗ | ✓ | ✓ |
| Best First Search  | ✗  | ✓ |  ✗  | ✓ | ✓ |
| Breadth First Search  | ✓  | ✗  | ✗  | ✓ | ✓ |
| Depth First Search  | ✗  | ✗  | ✗  | ✓ | ✓ |
| Dijkstra  | ✓  | ✗  | ✓  | ✓ | ✓ |
| Jump Point Search  | ✓   | ✓ | ✗  | ✓ | ✗ |
| Uniform Cost Search  | ✓  | ✗  | ✗  | ✓ | ✓ |
| IDA*  | ✓   | ✓ | ✓ | ✗ | ✓ |

* IDA* requires iterative update of a threshold value, which cannot remain uniform between a source and a destination. Hence, it does not support bidirectional search.
* Jump point search requires a regular two dimensional grid, and hence does not support the wormhole feature.
* Algorithms which are not meant for weighted graphs will be unaffected by cell weights (the sunlight feature).
* Informed search algorithms take into account various heuristics during path-finding.
* Beam search might not always produce a path even when one is possible at the cost of its space optimization. Increasing the beam width might help in such a scenario.

### Obstacles
* Obstacles are cells over which an agent cannot travel.
* We create a boundary of obstacles around the grid so that the algorithms are bounded to the visible screen.
* If you resize your screen, the old boundaries will be retained. Click of Reset Grid to generate a new boundary.

### Modes
The path finder has 3 modes:
1. **Multiple sources:** All sources simultaneously start their search for the destination and the final path is drawn from the first source that reaches it.
1. **Multiple destinations:** Source ends its search at the first destination it reaches. If the algorithm is guided, the lowest heuristic value from all destinations is used.
1. **Checkpoints:** The path starts from source and ends at destination, visiting all checkpoints in the given order.

### Configurations
1. **Cut corners:** Disable to prevent path from touching the corners of obstacle cells during diagonal movement. This feature cannot be enabled if diagonal movement is not allowed, and cannot be disabled during jump point search.
1. **Allow diagonals:** Specify whether diagonal movement is allowed. This feature cannot be disabled in jump point search.
1. **Bidirectional:** Specify whether the destination is a moving agent or not. This feature is disabled in checkpoint mode and IDA* algorithm.

### Cell weights
* Cell weights have been implemented in the form of the sunlight feature. Low sunlight corresponds to high cell weight and vice versa.
* In terms of weighted edges of a directed graph, the cost of moving from one cell to another is the weight of the destination cell.
* The cost of movement is multiplied by a factor of sqrt(2) in case of diagonal movement.
* The cell weight is representated on a scale of 0 to 2. The default sunlight is 50%, corresponding to a weight of 1.
* The cost of using a wormhole is 0, which can be thought of as the wormhole exit point having a weight of 0.
* The cost of moving from one cell to another is:
![equation1](https://latex.codecogs.com/gif.latex?cost(x,&space;y)&space;=&space;sqrt(manhattanDistance(x,&space;y))&space;*&space;cellWeight(y))
![equation2](https://latex.codecogs.com/gif.latex?cellWeight(y)&space;=&space;((100&space;-&space;sunlightIntensity(y))&space;/&space;100&space;)&space;*&space;2)

### Random mazes

### Wormholes

## Future work

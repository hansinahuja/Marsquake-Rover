# Marsquake-Rover

## Features

### Supported algorithms

Here is a summary of all the algorithms we support:

| Algorithm  | Shortest path guaranteed | Informed search | For weighted graphs |
| ------------- | :-------------: | :-------------: | :-------------: |
| A*  | ✓  | ✓ | ✓ |
| Statically Weighted A*  | ✗  | ✓ | ✓ |
| Dynamically Weighted A*  | ✗  | ✓ | ✓ |
| Beam Search  | ✗  | ✗ | ✗ |
| Best First Search  | ✗  | ✓ |  ✗  |
| Breadth First Search  | ✓  | ✗  | ✗  |
| Depth First Search  | ✗  | ✗  | ✗  |
| Dijkstra  | ✓  | ✗  | ✓  |
| Jump Point Search  | ✓   | ✓ | ✗  |
| Uniform Cost Search  | ✓  | ✗  | ✗  |
| IDA*  | ✓   | ✓ | ✓ |

### Obstacles

### Modes
The path finder has 3 modes:
1) Multiple sources- All sources simultaneously start their search for the destination and the final path is drawn from the first source that reaches it.
2) Multiple destinations- Source ends its search at the first destination it reaches. If the algorithm is guided, the lowest heuristic value from all destinations is used.
3) Checkpoints- The path starts from source and ends at destination, visiting all checkpoints in the given order.

### Configurations

### Cell weights

### Random mazes

### Wormholes

## Future work

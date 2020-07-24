# Marsquake Rover
Welcome to the Marsquake Rover! This is a path-finding visualiser with several algorithms and configurations to play around with. The visualiser has been hosted [here,](http://marsquake.azurewebsites.net) and we hope you have fun using it.

The app waks you through the main features we've implemented. For some comprehensive algorithmic details, check out the technical documentation in this repository.

The app is supported on all major web browsers, but we recommend using it on Google Chrome.

## Table of contents

* [How to run](#how-to-run)
* [Features](#features)
  * [Supported algorithms](#supported-algorithms)
  * [Obstacles](#Obstacles)
  * [Modes](#Modes)
  * [Configurations](#Configurations)
  * [Cell weights](#Cell-weights)
  * [Random mazes](#Random-mazes)
  * [Wormholes](#Wormholes)
* [Tasks](#tasks)

## How to run
The application has been deployed [here.](http://marsquake.azurewebsites.net)
To run locally,

Install all the required libraries (Currently just Flask) with


    pip install -r requirements.txt
 
 After cloning this repository, the flask server can be started by the following commands
 
For Windows Command Prompt,

    cd Marsquake-Rover\src
    set FLASK_APP=api
    flask run

For Windows PowerShell,

    cd Marsquake-Rover\src
    $env:FLASK_APP = "api"
    flask run
 
For Linux / Mac Terminal,
 
    cd Marsquake-Rover/src
    export FLASK_APP=api
    flask run

Now, type `localhost:PORT` in the address bar of the browser. Make sure to replace `PORT` with the actual port the server is running on.

The port is set to 5000 by default and can be verified in the output of the last command.

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

* IDA* requires iterative update of a threshold value, which cannot remain uniform across multiple moving agents. Hence, it does not support bidirectional search or multisource mode.
* Jump point search requires a regular two dimensional grid, and hence does not support the wormhole feature.
* Algorithms which are not meant for weighted graphs will be unaffected by cell weights (the sunlight feature).
* Informed search algorithms take into account various heuristics during path-finding.
* Beam search might not always produce a path even when one is possible at the cost of its space optimization. Increasing the beam width might help in such a scenario.

### Obstacles
* Obstacles are cells over which an agent cannot travel.
* We create a boundary of obstacles around the grid so that the algorithms are bounded to the visible screen.
* If you resize your screen, the old boundaries will be retained. Click on Reset Grid to generate a new boundary.

### Modes
The path finder has 3 modes:
1. **Multiple sources:** All sources simultaneously start their search for the destination and the final path is drawn from the first source that reaches it. This mode is disabed in IDA* algorithm.
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
* The cost of moving from one cell to another is: <br/><br/>
![equation1](https://latex.codecogs.com/gif.latex?cost(x,&space;y)&space;=&space;sqrt(manhattanDistance(x,&space;y))&space;*&space;cellWeight(y)) <br/><br/>
![equation2](https://latex.codecogs.com/gif.latex?cellWeight(y)&space;=&space;((100&space;-&space;sunlightIntensity(y))&space;/&space;100&space;)&space;*&space;2)

### Random mazes
The path finder has 2 maze generation algorithms. Both generate a completely random maze which has a possible path between any two cells.
1. **Recursive Maze Algorithm:** Randomly divides the grid into two parts with a wall which contains a randomly poisitioned free cell, then recursively repeats for sub-grids.
1. **Randomized Prim's Algorithm:** Represents the grid as a graph and generates a random  minimum spanning tree (MST).
### Wormholes
* When an agent steps on cell marked as the wormhole entry, it moves to the wormhole exit with 0 cost.
* The cell marked as wormhole entry can be thought of as being disconnected with its physical neighbours, and its only neighbour becomes the wormhole exit.
* Note that for informed algorithms, wormholes will not be treated as destination nodes. For example, if a wormhole exit is located close to the destination, the algorithm will not be able to account for this non-physical proximity. This can alter the usual properties of any given algorithm.

## Tasks
- [X] Expand browser support.
- [X] Provide an option to change drawing speed.
- [X] Change path colour after reaching a checkpoint.
- [X] Display the time taken.
- [ ] Provide an option to pause visualisation.
- [ ] Provide bidirectional wormholes.
- [ ] Provide an option to alter cell size.

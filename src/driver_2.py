from agent import Agent
from environment.env import Environment
from environment.utils import Location
from modes.checkpointMode import checkpointMode
from modes.nonCheckpointMode import nonCheckpointMode


def driver(dict):

    if (int(dict['multistart']) == 0 and int(dict['multidest']) == 0):
        return checkpointMode(dict)

    else:
        return nonCheckpointMode(dict)


dict = {
    "algo": 10,
    "start": [{"x": 0, "y": 0}],
    "stop": [{"x": 0, "y": 4}],
    "checkpoints": [ ],
    # "wormhole": [{'x': 2, 'y': 0}, {'x': 2, 'y': 4}],
    "multistart": '0',
    "relaxation": '3',
    "maxDepth": '8',
    "multidest": '0',
    "cutCorners": 1,
    "heuristic": 0,
    "allowDiagonals": 1,
    "biDirectional": 0,
    "beamWidth": 2,
    "maze":
    [[0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0],
     ],
     "weights": 
     [[50, 50, 50, 50, 50],
     [50, 50, 50, 50, 50],
     [50, 50, 50, 50, 50],
     [50, 50, 50, 50, 50],
     [50, 50, 50, 50, 50],
     ],
}

print(driver(dict)['path'])

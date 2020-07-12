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
    "algo": 7,
    "start": [{"x": 5, "y": 0}],
    "stop": [{"x": 2, "y": 3}],
    "checkpoints": [
        # {"x": 4, "y": 4}
        ],
    "multistart": '0',
    "multidest": '0',
    "cutCorners": 0,
    "allowDiagonals": 0,
    "biDirectional": 0,
    "beamWidth": 2,
    "maze":
    [[0, 0, 0, 0, 0],
     [0, 1, 1, 0, 0],
     [0, 1, 0, 0, 0],
     [0, 1, 0, 0, 0],
     [0, 1, 1, 1, 1],
     [0, 0, 0, 0, 0]
     ]
}

print(driver(dict))

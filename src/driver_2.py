from agent import Agent
from environment.env import Environment
from environment.utils import Location
from modes.checkpointMode import checkpointMode
from modes.nonCheckpointMode import nonCheckpointMode


def driver(dict):

    if int(dict['multistart']) or int(dict['multidest']):
        return nonCheckpointMode(dict)

    else:
        return checkpointMode(dict)


dict = {
    "algo": 0,
    "start": [{"x": 0, "y": 0}],
    "stop": [{"x": 0, "y": 1}],
    "checkpoints": [{"x": 4, "y": 4}],
    "multistart": '0',
    "multidest": '0',
    "cutCorners": 0,
    "allowDiagonals": 1,
    "biDirectional": 0,
    "beamWidth": 2,
    "maze":
    [[0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0]
     ]
}

print(driver(dict))

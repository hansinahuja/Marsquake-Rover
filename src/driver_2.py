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


# dict = {
#     "algo": 0,
#     "start": [{"x": 0, "y": 0}],
#     "stop": [{"x": 4, "y": 4}],
#     "checkpoints": [
#         # {"x": 4, "y": 4}
#         ],
#     "wormholes": [{'x1': 2, 'y1': 0, 'x2': 4, 'y2': 3}],
#     "multistart": '0',
#     "multidest": '0',
#     "cutCorners": 0,
#     "allowDiagonals": 0,
#     "biDirectional": 0,
#     "beamWidth": 2,
#     "maze":
#     [[0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0],
#      ]
# }

# print(driver(dict))

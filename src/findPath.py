from modes import checkpointMode, nonCheckpointMode

def findPath(config):

    """"
    Driver function to run the required mode of operation.
    Args:
        config: Dictionary with all the configuration settings.
    returns:
        The final path and changes in the grid throughout the run.
    """

    # Check the flags and run the required mode
    
    if (int(config['multistart']) == 0 and int(config['multidest']) == 0):
        return checkpointMode(config)

    else:
        return nonCheckpointMode(config)


# dict = {
#     "algo": 10,
#     "start": [{"x": 0, "y": 0}],
#     "stop": [{"x": 0, "y": 4}],
#     "checkpoints": [ ],
#     # "wormhole": [{'x': 2, 'y': 0}, {'x': 2, 'y': 4}],
#     "multistart": '0',
#     "relaxation": '3',
#     "maxDepth": '8',
#     "multidest": '0',
#     "cutCorners": 1,
#     "heuristic": 0,
#     "allowDiagonals": 1,
#     "biDirectional": 0,
#     "beamWidth": 2,
#     "maze":
#     [[0, 0, 1, 0, 0],
#      [0, 0, 1, 0, 0],
#      [0, 0, 0, 0, 0],
#      [0, 0, 1, 0, 0],
#      [0, 0, 1, 0, 0],
#      ],
#      "weights": 
#      [[50, 50, 50, 50, 50],
#      [50, 50, 50, 50, 50],
#      [50, 50, 50, 50, 50],
#      [50, 50, 50, 50, 50],
#      [50, 50, 50, 50, 50],
#      ],
# }

# print(driver(dict)['path'])

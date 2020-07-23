def validateInput(config):

    """
    Raises an error for invalid API calls.
    Args:
        config: Dictionary with all the configuration settings.
    """

    # --------- Error handling for maze ---------#

    if 'maze' not in config:
        raise Exception('maze not provided.')

    if not isinstance(config['maze'], list):
        raise Exception('maze must be a uniform list of lists.')

    length = len(config['maze'])
    if length == 0:
        raise Exception('maze must be non-empty.')

    breadth = len(config['maze'][0])
    if breadth == 0:
        raise Exception('maze must be non-empty.')

    for row in config['maze']:
        if not isinstance(row, list):
            raise Exception('maze must be a uniform list of lists.')

        if len(row) != breadth:
            raise Exception('maze must be a uniform list of lists.')

        for element in row:
            if not isinstance(element, int) or element < 0 or element > 1:
                raise Exception('maze elements must be 0 or 1.')


    # --------- Error handling for weights ---------#

    if 'weights' not in config:
        raise Exception('weights not provided.')

    if not isinstance(config['weights'], list):
        raise Exception('weights must be a uniform list of lists.')

    if len(config['weights']) != length:
        raise Exception('weights must have same dimensions as maze.')

    for row in config['weights']:
        if not isinstance(row, list):
            raise Exception('weights must be a uniform list of lists.')

        if len(row) != breadth:
            raise Exception('weights must have same dimensions as maze.')

        for element in row:
            if not (isinstance(element, float) or isinstance(element, int)) or element < 0 or element > 100:
                raise Exception('weight elements must be between 0 and 100.')

    # --------- Error handling for algo ---------#

    if 'algo' not in config:
        raise Exception('algo not provided.')

    if not config['algo'].isdigit() or int(config['algo']) < 0 or int(config['algo']) > 11:
        raise Exception('algo must be an integer from 0 to 11.')

    # --------- Error handling for mode selection ---------#

    if 'multistart' not in config:
        raise Exception('multistart not provided.')

    if not config['multistart'].isdigit() or int(config['multistart']) < 0 or int(config['multistart']) > 1:
        raise Exception('multistart must be 0 or 1.')

    if 'multidest' not in config:
        raise Exception('multidest not provided.')

    if not config['multidest'].isdigit() or int(config['multidest']) < 0 or int(config['multidest']) > 1:
        raise Exception('multidest must be 0 or 1.')

    if int(config['multistart']) == 1 and int(config['multidest']) == 1:
        raise Exception('multistart and multidest cannot be activated together.')

    # --------- Error handling for parameter selection ---------#

    # For bidirectional
    if int(config['algo']) != 6:

        if 'biDirectional' not in config:
            raise Exception('biDirectional not provided.')

        if not config['biDirectional'].isdigit() or int(config['biDirectional']) < 0 or int(config['biDirectional']) > 1:
            raise Exception('biDirectional must be 0 or 1.') 
    
    # For allow diagonals and corner cutting
    if int(config['algo']) != 9:

        if 'allowDiagonals' not in config:
            raise Exception('allowDiagonals not provided.')

        if not config['allowDiagonals'].isdigit() or int(config['allowDiagonals']) < 0 or int(config['allowDiagonals']) > 1:
            raise Exception('allowDiagonals must be 0 or 1.') 

        if 'cutCorners' not in config:
            raise Exception('cutCorners not provided.')

        if not config['cutCorners'].isdigit() or int(config['cutCorners']) < 0 or int(config['cutCorners']) > 1:
            raise Exception('cutCorners must be 0 or 1.') 

    # For heuristic selection
    if int(config['algo']) != 5 and int(config['algo']) != 7 and int(config['algo']) != 8 and int(config['algo']) != 10:
        
        if 'heuristic' not in config:
            raise Exception('heuristic not provided.')

        if not config['heuristic'].isdigit() or int(config['heuristic']) < 0 or int(config['heuristic']) > 3:
            raise Exception('heuristic must be an integer from 0 to 3.') 

    # For relaxation
    if int(config['algo']) == 1 or int(config['algo']) == 2:

        if 'relaxation' not in config:
            raise Exception('relaxation not provided.')

        if not config['relaxation'].replace('.', '', 1).isdigit():
            raise Exception('relaxation must be a numeric value.') 

    # For beam width
    if int(config['algo']) == 3:

        if 'beamWidth' not in config:
            raise Exception('beamWidth not provided.')

        if not config['beamWidth'].isdigit():
            raise Exception('beamWidth must be an integer.') 

    # --------- Error handling for start points ---------#

    if 'start' not in config:
        raise Exception('start not provided.')

    if not isinstance(config['start'], list) or len(config['start']) == 0:
        raise Exception('start must be a non-empty list.')

    for start in config['start']:

        if not isinstance(start, dict):
            raise Exception('start points must be dictionaries.') 

        if 'x' not in start or 'y' not in start:
            raise Exception('start points must have both x and y coordinates.') 

        if not isinstance(start['x'], int) or not isinstance(start['y'], int):
            raise Exception('start point coorindates must be integers.')

        if start['x'] < 0 or start['x'] >= length or start['y'] < 0 or start['y'] >= breadth:
            raise Exception('start point out of bounds.')

    # --------- Error handling for stop points ---------#

    if 'stop' not in config:
        raise Exception('stop not provided.')

    if not isinstance(config['stop'], list) or len(config['stop']) == 0:
        raise Exception('stop must be a non-empty list.')

    for stop in config['stop']:

        if not isinstance(stop, dict):
            raise Exception('stop points must be dictionaries.') 

        if 'x' not in stop or 'y' not in stop:
            raise Exception('stop points must have both x and y coordinates.') 

        if not isinstance(stop['x'], int) or not isinstance(stop['y'], int):
            raise Exception('stop point coorindates must be integers.')

        if stop['x'] < 0 or stop['x'] >= length or stop['y'] < 0 or stop['y'] >= breadth:
            raise Exception('stop point out of bounds.')

    # --------- Error handling for checkpoints ---------#

    if 'checkpoints' not in config:
        raise Exception('checkpoints not provided.')

    if not isinstance(config['stop'], list):
        raise Exception('checkpoints must be a list.')

    for checkpoint in config['checkpoints']:

        if not isinstance(stop, dict):
            raise Exception('checkpoints must be dictionaries.') 

        if 'x' not in checkpoint or 'y' not in checkpoint:
            raise Exception('checkpoints must have both x and y coordinates.') 

        if not isinstance(checkpoint['x'], int) or not isinstance(checkpoint['y'], int):
            raise Exception('checkpoint coorindates must be integers.')

        if checkpoint['x'] < 0 or checkpoint['x'] >= length or checkpoint['y'] < 0 or checkpoint['y'] >= breadth:
            raise Exception('checkpoint out of bounds.')

    # --------- Error handling for wormholes ---------#

    if 'wormhole' in config:

        wormhole = config['wormhole']
        if not isinstance(wormhole, list) or len(wormhole) != 2:
            raise Exception('wormhole must be a list of length 2.') 

        wormholeEntry, wormholeExit = wormhole[0], wormhole[1]

        if not isinstance(wormholeEntry, dict) or not isinstance(wormholeExit, dict):
            raise Exception('wormhole elements must be dictionaries.')

        if 'x' not in wormholeEntry or 'y' not in wormholeEntry or 'x' not in wormholeExit or 'y' not in wormholeExit:
             raise Exception('wormhole elements must have x and y coordinates.')

        x1, y1, x2, y2 = wormhole[0]['x'], wormhole[0]['y'], wormhole[1]['x'], wormhole[1]['y']

        if not isinstance(x1, int) or not isinstance(y1, int) or not isinstance(x2, int) or not isinstance(y2, int):
            raise Exception('wormhole coorindates must be integers.')

        if x1 < 0 or x1 >= length or y1 < 0 or y1 >= breadth or x2 < 0 or x2 >= length or y2 < 0 or y2 >= breadth:
            raise Exception('wormhole out of bounds.')
from modes.nonCheckpointMode import nonCheckpointMode


def checkpointMode(dict):
    points = []
    for point in dict['start']:
        points.append(point)
    for point in dict['checkpoints']:
        points.append(point)
    for point in dict['stop']:
        points.append(point)

    gridChanges = []
    path = []
    dict['biDirectional'] = '0'
    dict['checkpoints'] = []
    for i in range(len(points)-1):
        dict['start'] = [points[i]]
        dict['stop'] = [points[i+1]]
        result = nonCheckpointMode(dict)
        gridChanges.extend(result['gridChanges'])
        if len(result['path']) == 0:
            break
        else:
            path.extend(result['path'])
            gridChanges.extend(result['activatedCells'])
            if i < len(points)-2:
                path.pop()
    output = {'gridChages': gridChanges, 'path': path}
    return output

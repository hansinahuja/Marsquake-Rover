from modes.nonCheckpointMode import nonCheckpointMode


def checkpointMode(dict):
    # print("IN")
    # print(dict)
    # print("===================================================")
    points = []
    for point in dict['start']:
        points.append(point)
    for point in dict['checkpoints']:
        points.append(point)
    for point in dict['stop']:
        points.append(point)

    gridChanges = []
    path = []
    # dict['biDirectional'] = '0'
    dict['checkpoints'] = []
    for i in range(len(points)-1):
        # print(i)
        dict['start'] = [points[i]]
        dict['stop'] = [points[i+1]]
        result = nonCheckpointMode(dict)
        gridChanges.extend(result['gridChanges'])
        if len(result['path']) == 0:
            break
        else:
            path.extend(result['path'])
            if(len(points)>2):
                gridChanges.extend(result['activatedCells'])
            if i < len(points)-2:
                path.pop()
    # gridChanges = []
    output = {'gridChanges': gridChanges, 'path': path}
    # print(path)
    # print("===================")
    # print(gridChanges)
    return output

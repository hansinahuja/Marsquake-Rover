from modes import checkpointMode, nonCheckpointMode
from inputValidation import validateInput

def findPath(config):

    """"
    Driver function to run the required mode of operation.
    Args:
        config: Dictionary with all the configuration settings.
    returns:
        The final path and changes in the grid throughout the run.
    """

    try:

        # Error handling
        validateInput(config)

        # Check the flags and run the required mode
        if (int(config['multistart']) == 0 and int(config['multidest']) == 0):
            return checkpointMode(config)
        else:
            return nonCheckpointMode(config)

    except Exception as ex:
        print(str(ex))
        return ex
        
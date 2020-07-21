def aStar(self, environment, targets):

    """
    Performs one iteration of A* based on agent's current state.
    Args:
        environment: The current environment
        targets: The target agents
    """

    # Call static A* with relaxation = 0
    self.staticAStar(environment, targets, 0)
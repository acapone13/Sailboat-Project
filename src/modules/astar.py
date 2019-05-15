from AI import IAI

class Astar(IAI):
    """
    Module used to implement astar from AI interface
    """

    def step(self, params):
        raise NotImplementedError
        
    def log(self, message):
        print(message)
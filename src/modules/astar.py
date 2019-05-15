from AI import IAI

class Astar(IAI):
    """
    Module used to implement astar based on IAI interface
    """

    def step(self, params):
        raise NotImplementedError
        
    def log(self, message):
        print(message)
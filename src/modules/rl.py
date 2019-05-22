from AI import IAI

class Rl(IAI):
    """
    Module used to implement reinforcement learning from AI interface
    """

    def step(self, params):
        raise NotImplementedError
        
    def log(self, message):
        print(message)
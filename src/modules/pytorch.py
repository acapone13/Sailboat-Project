from AI import IAI

class Pytorch(IAI):
    """
    Module used to implement pytorch based on IAI interface
    """

    def step(self, params):
        raise NotImplementedError
        
    def log(self, message):
        print(message)
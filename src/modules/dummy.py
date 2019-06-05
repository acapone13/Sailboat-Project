from AI import IAI
import numpy as np
import random

class Dummy(IAI):
    """
    Module used to implement a random behaviour from AI interface
    """

    def step(self, params):
        # Params not used
        action = np.zeros(9)
        action[random.randrange(9)]=1
        return action.reshape(1,9)    
        
    def log(self, message):
        print(message)
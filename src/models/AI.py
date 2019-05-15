import abc

class IAI(abc.ABC):
    """
    Interface used to implement AI
    """

    @abc.abstractmethod
    def step(self, params):
        """ Next logic step

        Parameters:
            params (dict): Dictionary of parameters
        Returns:
            u (numpy): New rudder angle [Qv, Qd]
        """
        pass
    
    @abc.abstractmethod
    def log(self, message):
        """ Generate log

        Parameters:
            message (str): A message to generate log
        Returns:
            None
        """
        pass
import abc

class IAI(abc.ABC):
    """
    Interface used to implement AI
    """

    @abc.abstractmethod
    def step(self, wind, u, pos, target):
        """ Next logic step

        Parameters:
            wind (numpy): Wind Force (awind) and angle (ψ) -> [awind, ψ]
            u (numpy): Sail angle (Qv) and Rudder angle (Qd) -> [Qv, Qd]
            pos (numpy): Actual position -> [x, y]
            target (numpy): Target position -> [x, y]
        Returns:
            u_new (numpy): New rudder angle -> [Qv, Qd]
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
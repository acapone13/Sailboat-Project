import abc

class IAI(abc.ABC):
    
    @abc.abstractmethod
    def say_something(self, message):
        """ Print something

        Args:
            message : message to print as a string
        Returns:
            None
        """
        pass
import helpers
from astar import Astar
from pytorch import Pytorch

def main():    
    astar = Astar()
    astar.log("Astar module initialized")
    
    pytorch = Pytorch()
    pytorch.log("Pytorch module initialized")

if __name__ == "__main__":
    main()
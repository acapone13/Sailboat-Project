import helpers, argparse
from astar import Astar
from rl import Rl

# Arguments parser
parser = argparse.ArgumentParser(prog = "Sailboat-Project")
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
parser.add_argument("-a", "--astar", action="store_true", help = "Run astar module")
parser.add_argument("-r", "--rl", action="store_true", help = "Run reinforcement learning module")
args = parser.parse_args()

def valid_args(args):
    """
    Validate if the arguments are valid
    """
    if args.astar and args.rl:
        print("Please choose only one module, -h for more information.")
        exit()
    elif not args.astar and not args.rl:
        print("Please choose one module, -h for more information.")
        exit()

def main(args):
    if args.astar:
        # Astar module
        astar = Astar()
        astar.log("Astar module initialized")
    elif args.rl:
        # Reinforcement learning module
        rl = Rl()
        rl.log("Rl module initialized")

if __name__ == "__main__":
    valid_args(args)
    main(args)
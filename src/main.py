import helpers, argparse, gym, gym_voilier
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
    
    # Astar module
    if args.astar:
        model = Astar()
    # Reinforcement learning module
    elif args.rl:
        model = Rl()

    # Create an environment
    env = gym.make('voilier-v2').unwrapped
    state = env.reset()
    # TODO Get range by from argument
    for step in range(0,20,1):
        state = model.step(state)
        env.render()

if __name__ == "__main__":
    valid_args(args)
    main(args)
import helpers, argparse, gym, gym_voilier
from astar import Astar
from rl import Rl
from dummy import Dummy

# Arguments parser
parser = argparse.ArgumentParser(prog = "Sailboat-Project")
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
# parser.add_argument("-a", "--astar", action="store_true", help = "Run astar module")
# parser.add_argument("-r", "--rl", action="store_true", help = "Run reinforcement learning module")
# parser.add_argument("-d", "--dummy", action="store_true", help = "Dummy Test")
parser.add_argument("model", choices=["astar", "rl", "dummy"], help = "Model to use" )
args = parser.parse_args()

# def valid_args(args):
#     """
#     Validate if the arguments are valid
#     """
#     if args.astar and args.rl:
#         print("Please choose only one module, -h for more information.")
#         exit()
#     elif not args.astar and not args.rl and not args.dummy:
#         print("Please choose one module, -h for more information.")
#         exit()

def main(args):
    
    # # Astar module
    # if args.astar:
    #     model = Astar()
    # # Reinforcement learning module
    # elif args.rl:
    #     model = Rl()
    # elif args.dummy:
    #     model = Dummy()

    # Astar Module 
    if args.model == "astar":
        model = Astar()
    # Reinforcement Learning module
    elif args.model == "rl":
        model = Rl()
    # Dummy test 
    elif args.model == "dummy":
        model = Dummy()

    # Create an environment
    env = gym.make('voilier-v2').unwrapped
    state = env.reset()
    # TODO Get range by from argument
    for step in range(0,200,1):
        action = model.step(state)
        state, _, _, _ = env.step(action)
        env.render()

if __name__ == "__main__":
    # valid_args(args)
    main(args)
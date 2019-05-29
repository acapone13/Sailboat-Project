import helpers, argparse, gym, gym_voilier
from astar import Astar
from rl import Rl
from dummy import Dummy

# Arguments parser
parser = argparse.ArgumentParser(prog = "Sailboat-Project")
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
parser.add_argument("model", choices=["astar", "rl", "dummy"], help = "Model to use" )
args = parser.parse_args()

def main(args):
    
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
    # TODO Get range from argument
    for step in range(0,200,1):
        action = model.step(state)
        state, _, _, _ = env.step(action)
        env.render()

if __name__ == "__main__":
    main(args)
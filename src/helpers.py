import os, sys, inspect

# Source dir
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
root_dir = os.path.dirname(src_dir)

# Refers to src folders
sys.path.append(src_dir + "/models")
sys.path.append(src_dir + "/modules")
sys.path.append(src_dir + "/tests")
sys.path.append(src_dir + "/simulator")

# Refers to lib folders
sys.path.append(root_dir + "/lib/gym-voilier-v2-discrete")

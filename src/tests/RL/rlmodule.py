# -*- coding: utf-8 -*-

import gym
import gym_voilier
import math
import random
import numpy as np
from collections import namedtuple

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
from numpy import pi, arange

import sys, getopt



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def decode_action(act):
     return act//9, act%9 # voile, derive

def code_action(action):
    return  action[0]*9 + action[1]


class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class Net(nn.Module):
    def __init__(self, input_size, output_size, hidden_size):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)
        self.fc2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        out = self.fc1(x.float()) #Il y avait un erreur: Expected Float but got Double instead
        out = self.relu(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out

def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
 
            return policy_net(state).max(1)[1].view(1, 1)
    else:
        return torch.tensor([[random.randrange(n_actions)]], device=device, dtype=torch.long)


def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    batch = Transition(*zip(*transitions))
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.uint8)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    state_action_values = policy_net(state_batch).gather(1, action_batch)

    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()

    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

    optimizer.zero_grad()
    loss.backward()
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)
    optimizer.step()

def save_model(model, i):
    path = "../data/model_{:03d}"
    print('Saving model parameters "', path, '"..')
    torch.save(model.state_dict(), path.format(i))

def load_model(model, path):
    print("Loading model parameters from ", path, "..")
    model.load_state_dict(torch.load(path))
    model.eval()

if __name__ == '__main__':
    model_file = None
    try:
        opts, args = getopt.getopt(sys.argv[1:],"",["model_params="])
    except getopt.GetoptError:
        print("RLModule.py --model_params <PATH_TO_FILE>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--model_params':
            model_file = arg
    env = gym.make('voilier-v0').unwrapped
   

    Transition = namedtuple('Transition',
                            ('state', 'action', 'next_state', 'reward'))
    
    env.reset()

    BATCH_SIZE = 128
    GAMMA = 0.999
    #EPS_START = 0.9
    #EPS_END = 0.05
    EPS_START = 0.0
    EPS_END = 0.0
    EPS_DECAY = 200
    TARGET_UPDATE = 10


    input_size = 4
    hidden_size = 40    
    n_actions = 81

    policy_net =  Net(input_size, n_actions, hidden_size).to(device)
    if model_file is not None:
        load_model(policy_net, model_file)
    target_net = Net(input_size, n_actions, hidden_size).to(device)
    target_net.load_state_dict(policy_net.state_dict())
    target_net.eval()

    optimizer = optim.RMSprop(policy_net.parameters())
    memory = ReplayMemory(10000)


    steps_done = 0

    possible_actions = [-pi/2, -pi/3, -pi/4, -pi/5, 0, pi/5, pi/4, pi/3, pi/2]

    episode_durations = []

    t_max = 100
    dt = 0.2
    num_episodes = 1000


    for i_episode in range(num_episodes):

        state = env.reset()
        state = torch.from_numpy(np.array([state], dtype = np.float32)).to(device)
        for t in arange(0,t_max,dt):
            env.render()

            action = select_action(state)
            theta_voile, theta_derive = decode_action(action)
            u = np.array([possible_actions[theta_voile], possible_actions[theta_derive]]) / (pi/2)
            next_state, reward, done, _ = env.step(u)
            next_state = torch.from_numpy(np.array([next_state], dtype = np.float32)).to(device)

            reward = torch.tensor([reward], device=device, dtype = torch.float)

   
            memory.push(state, action, next_state, reward)


            state = next_state

           
            optimize_model()
            if done:
                episode_durations.append(t + 1)
                break

        if i_episode % TARGET_UPDATE == 0:
            target_net.load_state_dict(policy_net.state_dict())
        print("Episode: ", i_episode)

    print('Complete')
    env.render()
    env.close()
    save_model(policy_net, num_episodes)
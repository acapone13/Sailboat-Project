"""
Reinforcement Learning (A3C) using Pytroch + multiprocessing.
The most simple implementation for continuous action.

View more on my Chinese tutorial page [莫烦Python](https://morvanzhou.github.io/).
"""

import torch
import torch.nn as nn
from utils import v_wrap, set_init, push_and_pull, record
import torch.nn.functional as F
import torch.multiprocessing as mp
from shared_adam import SharedAdam
import numpy as np
import gym
import gym_voilier
import os
from discrete_A3C import Net
os.environ["OMP_NUM_THREADS"] = "1"
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# print(device)

UPDATE_GLOBAL_ITER = 10
GAMMA = 0.9
MAX_EP = 100000

env = gym.make('voilier-v2')
N_S = env.observation_space.shape[0]
N_A = env.action_space.n

print('N_S',N_S)
print('N_A',N_A)

class Worker(mp.Process):
    def __init__(self, gnet, opt, global_ep, global_ep_r, res_queue, name, global_record):
        super(Worker, self).__init__()
        self.name = 'w%i' % name
        self.g_ep, self.g_ep_r, self.res_queue = global_ep, global_ep_r, res_queue
        self.gnet, self.opt = gnet, opt
        self.lnet = Net(N_S, N_A)           # local network
        self.env = gym.make('voilier-v2').unwrapped
        self.global_record = global_record

    def run(self):
        total_step = 1
        while self.g_ep.value < MAX_EP:
            s = self.env.reset()
            buffer_s, buffer_a, buffer_r = [], [], []
            ep_r = 0.
            while True:
                if self.name == 'w0':
                    self.env.render()
                a = self.lnet.choose_action(v_wrap(s[None, :]))
                action = np.zeros((N_A))
                action[a] = 1
                # print(self.name,action)
                s_, r, done, _ = self.env.step(action)
                #if done: r = -1
                ep_r += r
                buffer_a.append(a)
                buffer_s.append(s)
                buffer_r.append(r)

                if done:  # update global and assign to local net
                    break
                s = s_
                total_step += 1


if __name__ == "__main__":
    #gnet = Net(N_S, N_A)        # global network
    # gnet = torch.load("./models/model_max_1.299772.pt")
    # gnet = torch.load("./models/model_max_0.99_1.435170.pt")
    gnet = torch.load("./models/model_max.pt")
    gnet.share_memory()         # share the global parameters in multiprocessing
    opt = SharedAdam(gnet.parameters(), lr=0.0001)      # global optimizer
    global_ep, global_ep_r, res_queue, global_record = mp.Value('i', 0), mp.Value('d', 0.), mp.Queue(), mp.Value('d', -100.)

    # parallel training
    #workers = [Worker(gnet, opt, global_ep, global_ep_r, res_queue, i) for i in range(mp.cpu_count())]
    workers = [Worker(gnet, opt, global_ep, global_ep_r, res_queue, i, global_record) for i in range(1)]
    [w.start() for w in workers]
    res = []                    # record episode reward to plot
    while True:
        r = res_queue.get()
        if r is not None:
            res.append(r)
        else:
            break
    [w.join() for w in workers]

    import matplotlib.pyplot as plt
    plt.plot(res)
    plt.ylabel('Moving average ep reward')
    plt.xlabel('Step')
    plt.show()

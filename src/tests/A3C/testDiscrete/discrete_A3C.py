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


class Net(nn.Module):
    def __init__(self, s_dim, a_dim):
        super(Net, self).__init__()
        self.s_dim = s_dim
        self.a_dim = a_dim
        self.pi1 = nn.Linear(s_dim, 128)
        self.pi12 = nn.Linear(128, 32)
        self.pi13 = nn.Linear(32, 16)
        self.pi2 = nn.Linear(16, a_dim)
        self.v1 = nn.Linear(s_dim, 64)
        self.v12 = nn.Linear(64, 16)
        self.v13 = nn.Linear(16, 16)
        self.v2 = nn.Linear(16, 1)
        self.drop = nn.Dropout(0.5)
        set_init([self.pi1, self.pi2, self.v1, self.v2])
        self.distribution = torch.distributions.Categorical

    def forward(self, x):
        pi1 = F.relu6(self.pi1(x))
        # pi1 = self.drop(pi1)
        pi12 = F.relu6(self.pi12(pi1))
        # pi12 = self.drop(pi12)
        pi13 = F.relu6(self.pi13(pi12))
        logits = self.pi2(pi13)
        v1 = F.relu6(self.v1(x))
        # v1 = self.drop(v1)
        v12 = F.relu6(self.v12(v1))
        # v12 = self.drop(v12)
        v13 = F.relu6(self.v13(v12))
        values = self.v2(v13)
        return logits, values

    def choose_action(self, s):
        self.eval()
        logits, _ = self.forward(s)
        prob = F.softmax(logits, dim=1).data
        m = self.distribution(prob)
        return m.sample().numpy()[0]

    def loss_func(self, s, a, v_t):
        self.train()
        logits, values = self.forward(s)
        td = v_t - values
        c_loss = td.pow(2)
        
        probs = F.softmax(logits, dim=1)
        m = self.distribution(probs)
        exp_v = m.log_prob(a) * td.detach().squeeze()
        a_loss = -exp_v
        total_loss = (c_loss + a_loss).mean()
        return total_loss


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

                if total_step % UPDATE_GLOBAL_ITER == 0 or done:  # update global and assign to local net
                    # sync
                    push_and_pull(self.opt, self.lnet, self.gnet, done, s_, buffer_s, buffer_a, buffer_r, GAMMA)
                    buffer_s, buffer_a, buffer_r = [], [], []

                    if done:  # done and print information
                        record(self.g_ep, self.g_ep_r, ep_r, self.res_queue, self.name, self.gnet, self.global_record)
                        break
                s = s_
                total_step += 1
        self.res_queue.put(None)


if __name__ == "__main__":
    gnet = Net(N_S, N_A)        # global network
    #gnet = torch.load("./data/model.pt")
    gnet.share_memory()         # share the global parameters in multiprocessing
    opt = SharedAdam(gnet.parameters(), lr=0.0001)      # global optimizer
    global_ep, global_ep_r, res_queue, global_record = mp.Value('i', 0), mp.Value('d', 0.), mp.Queue(), mp.Value('d', -100.)

    # parallel training
    #workers = [Worker(gnet, opt, global_ep, global_ep_r, res_queue, i) for i in range(mp.cpu_count())]
    workers = [Worker(gnet, opt, global_ep, global_ep_r, res_queue, i, global_record) for i in range(6)]
    [w.start() for w in workers]
    res = []                    # record episode reward to plot
    while True:
        r = res_queue.get()
        if r is not None:
            res.append(r)
        else:
            break
    [w.join() for w in workers]

    print('Saving model')
    torch.save(gnet, 'model_last.pt')

    import matplotlib.pyplot as plt
    plt.plot(res)
    plt.ylabel('Moving average ep reward')
    plt.xlabel('Step')
    plt.show()

"""
Definitions for Actor and Critic
Author: Sameera Lanka
Website: https://sameera-lanka.com
"""

import torch
import torch.nn as nn
import numpy as np
from torch.autograd import Variable


def fanin_init(size, fanin=None):
    """Utility function for initializing actor and critic"""
    fanin = fanin or size[0]
    w = 1. / np.sqrt(fanin)
    return torch.Tensor(size).uniform_(-w, w)


HID_LAYER1 = 400
HID_LAYER2 = 300
HID_LAYER3 = 200
WFINAL = 0.003


class Actor(nn.Module):
    """Defines actor network"""

    def __init__(self):
        super(Actor, self).__init__()
        self.stateDim = 27
        self.actionDim = 3

        self.norm0 = nn.BatchNorm1d(self.stateDim)

        self.fc1 = nn.Linear(self.stateDim, HID_LAYER1)
        self.fc1.weight.data = fanin_init(self.fc1.weight.data.size())
        self.bn1 = nn.BatchNorm1d(HID_LAYER1)

        self.fc2 = nn.Linear(HID_LAYER1, HID_LAYER2)
        self.fc2.weight.data = fanin_init(self.fc2.weight.data.size())
        self.bn2 = nn.BatchNorm1d(HID_LAYER2)

        self.fc3 = nn.Linear(HID_LAYER2, HID_LAYER3)
        self.fc3.weight.data = fanin_init(self.fc3.weight.data.size())
        self.bn3 = nn.BatchNorm1d(HID_LAYER3)

        self.fc4 = nn.Linear(HID_LAYER3, self.actionDim)
        self.fc4.weight.data.uniform_(-WFINAL, WFINAL)

        self.ReLU = nn.ReLU()
        self.Sigmoid = nn.Sigmoid()

    def forward(self, ip):
        ip_norm = self.norm0(ip)
        h1 = self.ReLU(self.fc1(ip_norm))
        h1_norm = self.bn1(h1)
        h2 = self.ReLU(self.fc2(h1_norm))
        h2_norm = self.bn2(h2)
        h3 = self.ReLU(self.fc3(h2_norm))
        h3_norm = self.bn3(h3)
        output = self.fc4(h3_norm)
        action = self.Sigmoid(output)
       # action = action.view(-1, 1)
        return action


class Critic(nn.Module):
    """Defines critic network"""

    def __init__(self):
        super(Critic, self).__init__()
        self.stateDim = 27
        self.actionDim = 3

        self.fc1 = nn.Linear(self.stateDim, HID_LAYER1)
        self.fc1.weight.data = fanin_init(self.fc1.weight.data.size())
        self.bn1 = nn.BatchNorm1d(HID_LAYER1)

        self.fc2 = nn.Linear(HID_LAYER1 + self.actionDim, HID_LAYER2)
        self.fc2.weight.data = fanin_init(self.fc2.weight.data.size())

        self.fc3 = nn.Linear(HID_LAYER2, 1)
        self.fc3.weight.data.uniform_(-WFINAL, WFINAL)

        self.ReLU = nn.ReLU()

    def forward(self, ip, action):
       # action = action.view(3)
        h1 = self.ReLU(self.fc1(ip))
        h1_norm = self.bn1(h1)
        h2 = self.ReLU(self.fc2(torch.cat([h1_norm, action], dim=1)))
        Qval = self.fc3(h2)
        return Qval



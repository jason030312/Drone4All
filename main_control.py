"""
Deep Deterministic Policy Gradient agent
Author: Sameera Lanka
Website: https://sameera-lanka.com
"""

# Torch
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim

# Lib
import numpy as np
import math
from copy import deepcopy
from things.QuadDrone import BigQuad

# Files
from network.noise import OrnsteinUhlenbeckActionNoise as OUNoise
from network.replaybuffer import Buffer
from network.actorcritic_quad import Actor, Critic

# Hyperparameters
ACTOR_LR = 0.0001
CRITIC_LR = 0.001
MINIBATCH_SIZE = 64
NUM_EPISODES = 100000
MU = 0
SIGMA = 0.2
BUFFER_SIZE = 1000000
DISCOUNT = 0.9
TAU = 0.001
WARMUP = 70
EPSILON = 1.0
EPSILON_DECAY = 1e-12
degree_factor = 180
accel_factor = 1

obst_l = []

quad = BigQuad()
device = torch.device("cpu")


def make_obstacle():
    while True:
        input_obst = input()
        if input_obst == 'end':
            break
        obst_l.append(list(map(int, input_obst.split(' '))))
    print(obst_l)


class DDPG:
    def __init__(self):
        self.stateDim = 30
        self.actionDim = 2
        self.actor = Actor()
        self.critic = Critic()
        self.targetActor = deepcopy(Actor())
        self.targetCritic = deepcopy(Critic())
        self.actorOptim = optim.Adam(self.actor.parameters(), lr=ACTOR_LR)
        self.criticOptim = optim.Adam(self.critic.parameters(), lr=CRITIC_LR)
        self.criticLoss = nn.MSELoss()
        self.noise = OUNoise(mu=np.zeros(self.actionDim), sigma=SIGMA)
        self.replayBuffer = Buffer(BUFFER_SIZE)
        self.batchSize = MINIBATCH_SIZE
        self.discount = DISCOUNT
        self.warmup = WARMUP
        self.epsilon = EPSILON
        self.epsilon_decay = EPSILON_DECAY
        self.start = 0
        self.end = NUM_EPISODES

    def getQTarget(self, nextStateBatch, rewardBatch, terminalBatch):
        """Inputs: Batch of next states, rewards and terminal flags of size self.batchSize
            Calculates the target Q-value from reward and bootstraped Q-value of next state
            using the target actor and target critic
           Outputs: Batch of Q-value targets"""

        targetBatch = torch.FloatTensor(rewardBatch)
        nonFinalMask = torch.ByteTensor(tuple(map(lambda s: s is not True, terminalBatch)))
        nextStateBatch = torch.cat(nextStateBatch)
        with torch.no_grad():
            nextActionBatch = self.targetActor(nextStateBatch)
        # nextActionBatch.volatile = True
        qNext = self.targetCritic(nextStateBatch, nextActionBatch)

        nonFinalMask = self.discount * nonFinalMask.type(torch.FloatTensor)
        targetBatch += nonFinalMask * qNext.squeeze().data

        return Variable(targetBatch, requires_grad=False)

    def updateTargets(self, target, original):
        """Weighted average update of the target network and original network
            Inputs: target actor(critic) and original actor(critic)"""

        for targetParam, orgParam in zip(target.parameters(), original.parameters()):
            targetParam.data.copy_((1 - TAU) * targetParam.data + \
                                   TAU * orgParam.data)

    def getMaxAction(self, curState):
        """Inputs: Current state of the episode
            Returns the action which maximizes the Q-value of the current state-action pair"""
        with torch.no_grad():
            noise = self.epsilon * Variable(torch.FloatTensor(self.noise()))
        print(noise)
        action = self.actor(curState)
        actionNoise = action + noise
        return actionNoise

    def train(self):
        print('Training started...')
        make_obstacle()

        for i in range(self.start, self.end):
            quad.__init__()
            quad.setMotors([0, 0], False, True)
            statev = quad.getState()
            obstacle = quad.sense(statev[4][0], statev[0], obst_l)

            location_tensor = torch.as_tensor(statev[0], dtype=torch.float32)
            target_tensor = torch.as_tensor(statev[1], dtype=torch.float32)
            inertialVel_tensor = torch.tensor(statev[2], dtype=torch.float32)
            bodyaccel_tensor = torch.tensor(statev[3], dtype=torch.float32)
            ang_tensor = torch.tensor(statev[4], dtype=torch.float32)
            obstacle_tensor = torch.tensor(obstacle, dtype=torch.float32)
            state = torch.cat([location_tensor, target_tensor, inertialVel_tensor, bodyaccel_tensor, ang_tensor, obstacle_tensor], dim=0)
            state = state.unsqueeze(0)

            print()
            print("*******New episode*******\n")

            for t in range(100000):
                # Get maximizing action
                state = state.type(dtype=torch.float32)
                self.actor.eval()
                action = self.getMaxAction(state)
                self.actor.train()

                # Step episode
                action = action.detach()
                action = action[0]
                action[0] = action[0] * math.pi
                action[1] = action[1] * math.pi
                print()
                print("This is action")
                print(action)
                print()
                last_state = state
                quad.setMotors(action, statev[5], False)

                statev = quad.getState()
                obstacle = quad.sense(statev[4][0], statev[0], obst_l)
                location_tensor = torch.as_tensor(statev[0], dtype=torch.float32)
                target_tensor = torch.as_tensor(statev[1], dtype=torch.float32)
                inertialVel_tensor = torch.tensor(statev[2], dtype=torch.float32)
                bodyaccel_tensor = torch.tensor(statev[3], dtype=torch.float32)
                ang_tensor = torch.tensor(statev[4], dtype=torch.float32)
                obstacle_tensor = torch.tensor(obstacle, dtype=torch.float32)
                state = torch.cat([location_tensor, target_tensor, inertialVel_tensor,
                                   bodyaccel_tensor, ang_tensor, obstacle_tensor], dim=0)
                state = state.type(dtype=torch.float32)
                state = state.unsqueeze(0)
                reward, terminal = quad.giveReward(obstacle)
                reward = torch.tensor([reward], device=device)

                ct = False
                if terminal is True:
                    ct = True
                    terminal = False

                print(action)
                print(statev[0])
                print(statev[1])
                print()
                action = action.unsqueeze(0)
                # Update replay bufer
                self.replayBuffer.append((last_state, action, state, reward, terminal))


                # Training loop
                if len(self.replayBuffer) >= self.warmup:
                    curStateBatch, actionBatch, nextStateBatch, \
                    rewardBatch, terminalBatch = self.replayBuffer.sample_batch(self.batchSize)

                    curStateBatch = torch.cat(curStateBatch)
                    actionBatch = torch.cat(actionBatch)

                    qPredBatch = self.critic(curStateBatch, actionBatch)
                    print(len(nextStateBatch), len(rewardBatch), len(terminalBatch))
                    qTargetBatch = self.getQTarget(nextStateBatch, rewardBatch, terminalBatch).view(-1,1)

                    # Critic update
                    self.criticOptim.zero_grad()
                    criticLoss = self.criticLoss(qPredBatch, qTargetBatch)
                    print('Critic Loss: {}'.format(criticLoss))
                    criticLoss.backward()
                    self.criticOptim.step()

                    # Actor update
                    self.actorOptim.zero_grad()
                    actorLoss = -torch.mean(self.critic(curStateBatch, self.actor(curStateBatch)))
                    print('Actor Loss: {}'.format(actorLoss))
                    actorLoss.backward()
                    self.actorOptim.step()

                    # Update Targets
                    self.updateTargets(self.targetActor, self.actor)
                    self.updateTargets(self.targetCritic, self.critic)
                    self.epsilon -= self.epsilon_decay

                if ct is True:
                    break


if __name__ == "__main__":
    agent = DDPG()
    agent.train()
from collections import deque
import numpy as np
import pandas as pd
import torch
from torch import nn
import random
from Chainreactionenv import ChainReactionEnv
#psudo code
# 1. get the obvservation
# 2. agent takes action for red
# 3. check if red wins 
#       a.if Red wins calculate reward for last 50?? steps
#       b.reset the game
# 4. agent takes action for blue
# 5. check if blue wins
#       a.if Blue wins calculate reward for last 50?? steps
#       b.reset the game

# todo:
# define a model
# define memory

class Agent(nn.Module):
    def __init__(self,size):
        super(Agent, self).__init__()
        self.conv1 = nn.Conv2d(2,16,kernel_size=3,stride=1,padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16,32,kernel_size=3,stride=1,padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32,64,kernel_size=3,stride=1,padding=1)
        self.bn3 = nn.BatchNorm2d(64)
        self.conv4 = nn.Conv2d(64,16,kernel_size=3,stride=1,padding=1)
        self.bn4 = nn.BatchNorm2d(16)
        self.conv5 = nn.Conv2d(16,8,kernel_size=3,stride=1,padding=1)
        self.bn5 = nn.BatchNorm2d(8)
        self.conv6 = nn.Conv2d(8,1,kernel_size=3,stride=1,padding=1)
        
    def forward(self,x):
        x = nn.functional.relu(self.bn1(self.conv1(x)))
        x = nn.functional.relu(self.bn2(self.conv2(x)))
        x = nn.functional.relu(self.bn3(self.conv3(x)))
        x = nn.functional.relu(self.bn4(self.conv4(x)))
        x = nn.functional.relu(self.bn5(self.conv5(x)))
        x = nn.functional.relu(self.conv6(x))
        return x

    
            

class Memory:
    def __init__(self,size):
        self.size = size
        self.memory = {}
        self.memory["red"] = deque(maxlen=size)
        self.memory["blue"] = deque(maxlen=size)

    def sample(self,batch_size,color):
        batch = random.sample(self.memory[color],batch_size)
        return batch

    def append(self,item,color):
        self.memory[color].append(item)

    def __len__(self):
        return min(len(self.memory["red"]),len(self.memory["blue"]))
        
def Train(epochs,batch_size,lr=0.001,memory_size=2000):
    epsilon = 1
    epsilon_decay = 0.99
    gamma = 0.99
    # define the model
    model = Agent(memory_size)
    # define the memory
    memory = Memory(memory_size)
    # define the optimizer
    optimizer = torch.optim.Adam(model.parameters(),lr=lr)
    # define the loss function
    loss_fn = nn.MSELoss()
    # define the environment
    env = ChainReactionEnv((6,8))
    # define the game
    done = False
    for i in range(epochs):
        
        while done == False:
            observation = env.reset()
            observation = torch.from_numpy(observation).float()
            if random.uniform(0,1) < epsilon:
                # do a random action
                action = env.action_space.sample()
                observation_new, reward, done, info = env.step(action)
                observation_new = torch.from_numpy(observation_new).float() 
                # append the observation to the memory
                memory.append([observation,action,reward,done,observation_new],color=info)
            else:
                # do the best action acording to the model
                action = model.forward(observation)
                observation_new, reward, done, info = env.step()
                observation_new = torch.from_numpy(observation_new).float() 
                # append the observation to the memory
                memory.append([observation,action,reward,done,observation_new],color=info)
            
            if epsilon > 0.01:
                epsilon *= epsilon_decay

        def replay(self,memory,color,batch_size,gamma):
            #print("replay")
            # get the batch sample
            batch = memory.sample(batch_size,color)
            for observation,action,reward,done,observation_new in batch:
                if done:
                    target = reward
                else:
                    target = reward + gamma*torch.max(self.forward(observation_new))
                predicted_rewards = self.forward(observation)
                target_rewards = predicted_rewards.clone()
                target_rewards[action] = target
                loss = loss_fn(predicted_rewards,target_rewards)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        if len(memory) > batch_size:
            # do replay for red    
            replay(model,memory,color="red",batch_size=batch_size,gamma=gamma)
            # do replay for blue
            replay(model,memory,color="blue",batch_size=batch_size,gamma=gamma)
            
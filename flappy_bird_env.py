import torch
import gym
from model import Model
from collections import deque
import numpy as np
from env_wrapper import FlappyBirdEnv

env = FlappyBirdEnv(render_mode = "human")

policy = Model(4, 2)

def reinforce(policy, n_training_episodes, max_t, gamma, print_every):
    scores_deque = deque(maxlen=100)
    scores = []
    for i_episode in range(1, n_training_episodes+1):
        saved_log_probs = []
        rewards = []
        state, info = env.reset()
        # Line 4 of pseudocode
        for t in range(max_t):
            # print(state)
            # import ipdb; ipdb.set_trace()
            
            action, log_prob = policy.act(torch.tensor(state))
            saved_log_probs.append(log_prob)
            state, reward, done, _ = env.step(action)
            rewards.append(reward)
            if done:
                break 
        scores_deque.append(sum(rewards))
        scores.append(sum(rewards))
        
        returns = deque(maxlen=max_t) 
        n_steps = len(rewards) 
        
        for t in range(n_steps)[::-1]:
            disc_return_t = (returns[0] if len(returns)>0 else 0)
            returns.appendleft( gamma*disc_return_t + rewards[t]   )    
            
        eps = np.finfo(np.float32).eps.item()
        returns = torch.tensor(returns, dtype = torch.float32)
        returns = (returns - returns.mean()) / (returns.std() + eps)
        
        policy_loss = []
        for log_prob, disc_return in zip(saved_log_probs, returns):
            policy_loss.append(-log_prob * disc_return)
        
        # print(policy_loss)
        policy_loss = torch.cat(policy_loss).sum()
        
        policy.optimizer.zero_grad()
        policy_loss.backward()
        policy.optimizer.step()
        
        if i_episode % print_every == 0:
            print('Episode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_deque)))
        
    return scores

reinforce(
    policy=policy,
    n_training_episodes=1000,
    max_t = 500,
    gamma = 1,
    print_every=100
    )
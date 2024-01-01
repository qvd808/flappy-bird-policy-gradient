import torch
import gymnasium as gym
from model import Model
from collections import deque
import numpy as np
import matplotlib.pyplot as plt

def get_action(epsilon, env, q_table, obs):
    if np.random.uniform(0, 1) < epsilon:
        return env.action_space.sample()
    else:
        return np.argmax(q_table[obs])

def update_Qtable(Q, obs, new_obs, action, reward):
    Q[obs][action] = 0.4 * Q[obs][action] + 0.6 * (reward + Q[new_obs][np.argmax(Q[new_obs])])

def linear_decay(current_episode, total_episodes, initial_value, final_value):
    slope = (final_value - initial_value) / total_episodes
    return initial_value + slope * current_episode

if __name__ == "__main__":
    env = gym.make("FrozenLake-v1", render_mode = "human", is_slippery=True)
    print(env.observation_space.n)
    print(env.action_space.n)

    n_training_episodes = 10_000
    q_table = np.load("q_table_frozen.npy")
    max_eps = 1
    epsilon = max_eps
    n_stop = 5000
    rewards = []
    eps = []
    epsilon_list = []
    reward_per_run = 0
    plt.ion()

    obs, info = env.reset()
    max_step = 100
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))

    for i in range(n_training_episodes):
     
        for t in range(max_step):
            action = np.argmax(q_table[obs])
            obs, reward, done, terminate, _ = env.step(action)
            reward_per_run += reward

            if terminate or done:
                obs, info = env.reset()
                rewards.append(reward_per_run)
                reward_per_run =0
                eps.append(i)
                break 

        axs.clear()
        axs.plot(eps, rewards)

        if i % 250 == 0:
            plt.draw()
            plt.pause(0.001)
        
        plt.tight_layout()
        plt.show()
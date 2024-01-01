import torch
import gymnasium as gym
from model import Model
from collections import deque
import numpy as np
import matplotlib.pyplot as plt

def get_action(epsilon, env, q_table, obs):
    if np.random.uniform(0, 1) > epsilon:
        return np.argmax(q_table[obs])
    else:
        return env.action_space.sample()

def update_Qtable(Q, obs, new_obs, action, reward):
    Q[obs][action] = Q[obs][action] + 0.7 * (reward + 0.95 * np.max(Q[new_obs]) - Q[obs][action])

def linear_decay(current_episode, total_episodes, initial_value, final_value):
    slope = (final_value - initial_value) / total_episodes
    return initial_value + slope * current_episode

if __name__ == "__main__":
    env = gym.make("FrozenLake-v1", render_mode = "rgb_array")
    print(env.observation_space.n)
    print(env.action_space.n)

    n_training_episodes = 50_000
    q_table = np.zeros((env.observation_space.n, env.action_space.n), dtype=np.float32)
    max_eps = 1
    epsilon = max_eps
    rewards = []
    eps = []
    epsilon_list = []

    plt.ion()

    obs, info = env.reset()
    max_step = 100
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    reward_per_run = 0
    min_epsilon = 0.05
    max_epsilon = 1
    decay_rate = 0.0005

    for i in range(n_training_episodes):

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * i)      
        # epsilon = (max_epsilon - min_epsilon) - decay_rate * i + min_epsilon
        for t in range(max_step):
            action = get_action(epsilon=epsilon,
                                env=env,
                                q_table=q_table,
                                obs = obs)
            new_obs, reward, done, terminate, _ = env.step(action)
            update_Qtable(q_table, obs, new_obs, action, reward)
            obs = new_obs
            reward_per_run += reward

            if terminate or done:
                obs, info = env.reset()
                rewards.append(reward_per_run)
                reward_per_run =0
                eps.append(i)
                epsilon_list.append(epsilon)
                break 

        if i % 500 == 0:

            axs[0].clear()
            axs[1].clear()
            axs[0].hist(rewards)
            axs[1].plot(eps, epsilon_list)
            plt.draw()
            plt.pause(0.001)
            if i % 3000 == 0:
                np.save(f"./q_table_step_{i}.npy", q_table)
        

        plt.tight_layout()
        plt.show()
    np.save(f"./q_table_frozen.npy", q_table)
    
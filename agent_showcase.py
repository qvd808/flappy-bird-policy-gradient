import torch
import gymnasium as gym
from model import Model
from collections import deque
import numpy as np
from env_wrapper_2 import FlappyBirdEnv
import matplotlib.pyplot as plt

def get_action(epsilon, env, q_table, state):
    if np.random.uniform(0, 1) < epsilon:
        action = env.action_space.sample()
        return action

    return np.argmax(q_table[state[0]][state[1]])

#convert state to index
def discretize_state(state, v_bin, h_bin):
    v_index = np.digitize(state[0], bins=np.linspace(0, 300, v_bin))
    h_index = np.digitize(state[1], bins=np.linspace(-226, 336, h_bin))

    return v_index - 1, h_index - 1

def update_Qtable(Q, state, n_state, action, reward):
    if action:
        Q[state[0]][state[1]][1] = 0.4 * Q[state[0]][state[1]][1] + (0.85) * (reward + max(Q[n_state[0]][n_state[1]][0], Q[n_state[0]][n_state[1]][1]))
    else:
        Q[state[0]][state[1]][0] = 0.4 * Q[state[0]][state[1]][0] + (0.85) * (reward + max(Q[n_state[0]][n_state[1]][0], Q[n_state[0]][n_state[1]][1]))

def linear_decay(current_episode, total_episodes, initial_value, final_value):
    slope = (final_value - initial_value) / total_episodes
    return initial_value + slope * current_episode

if __name__ == "__main__":

    env = FlappyBirdEnv(render_mode="human")

    max_t = 600
    max_eps = 1
    epsilon = max_eps
    n_training_episodes = 10000
    gamma = 0.99
    v_bin = 10
    h_bin = 40

    q_table = np.load("q_table_step_4000.npy")
    print(q_table)
    state = env.reset()
    reward = 0
    actions_do = []
    reward_one_run = 0
    rewards = []
    eps = []
    plt.ion()

    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))


    for i in range(n_training_episodes):
        for t in range(max_t):
            # print(state)
            # import ipdb; ipdb.set_trace()
            v_prev, h_prev = discretize_state(state, v_bin, h_bin)

            action =np.argmax(q_table[v_prev][h_prev])

            n_state, n_reward, done = env.step(action)
            
            reward_one_run += reward
            
            if done:
                reward = 0
                state = env.reset()
                rewards.append(reward_one_run)
                reward_one_run = 0
                eps.append(i)

                break

        axs.clear()
        axs.plot(eps, rewards)
        if np.average(rewards) > 30000:
            break
        # print(rewards, eps)      

        plt.draw()
        plt.pause(0.001)

    plt.tight_layout()
    plt.show()


        
            
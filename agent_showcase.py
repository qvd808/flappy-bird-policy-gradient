import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from env_wrapper import FlappyBirdEnv

def discretize_state(state, v_bin, h_bin):
    i1 = np.digitize(state[0], bins=np.linspace(-109, 400, v_bin))
    i2 = np.digitize(state[1], bins=np.linspace(-109, 291, h_bin))
    i3 = np.digitize(state[2], bins=np.linspace( 359, 650, v_bin))
    i4 = np.digitize(state[3], bins=np.linspace(-109, 291, h_bin))

    return i1 - 1, i2 - 1, i3 - 1, i4 - 1

    # i1 = np.digitize(state[0], bins=np.linspace(-14, 466, v_bin))
    # i2 = np.digitize(state[1], bins=np.linspace(-260, 145, h_bin))

    # return i1 - 1, i2 - 1


def get_action(Q, state):
    i1, i2, i3, i4 = state
    if Q[i1][i2][i3][i4][1] > Q[i1][i2][i3][i4][0]:
        return 1
    elif Q[i1][i2][i3][i4][1] < Q[i1][i2][i3][i4][0]:
        return 0
    else:
        return np.random.randint(0, 2)

def update_Qtable(Q, state, n_state, action, reward):
    i1, i2, i3, i4 = state
    n1, n2, n3, n4 = n_state
    Q[i1][i2][i3][i4][action] = 0.4 * Q[i1][i2][i3][i4][action] + (0.6) * (reward + max(Q[n1][n2][n3][n4][:]))


if __name__ == "__main__":

    env = FlappyBirdEnv(render_mode="human")

    obs = env.reset()

    v_bin = 8
    h_bin = 8

    q_table = np.load("./q_table_flappy_bird.npy")
    n_training_episode = 10_000
    max_step = 250
    
    eps = []
    rewards = []
    reward_per_run = 0
    
    plt.ion()
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))

    for i in range(n_training_episode):
        for step in range(max_step):
            i1, i2, i3, i4 = discretize_state(obs, v_bin, h_bin)

            action = get_action(q_table, (i1, i2, i3, i4))
            n_obs, reward, terminate = env.step(action)

            reward_per_run += reward

            obs = n_obs
            
            if terminate:
                reward_per_run = 0
                obs = env.reset()
                break

        rewards.append(reward_per_run)
        eps.append(i)
        
        if i % 250 == 0:
            axs.clear()
            axs.plot(eps, rewards)
            plt.draw()
            plt.pause(0.05)

    plt.tight_layout()
    plt.show()

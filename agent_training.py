import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from env_wrapper import FlappyBirdEnv

def discretize_state(state, v_bin, h_bin):
    # i1 = np.digitize(state[-3], bins=np.linspace(-109, 400, v_bin))
    # i2 = np.digitize(state[-2], bins=np.linspace(-109, 291, h_bin))
    # i3 = np.digitize(state[-4], bins=np.linspace(-109, 291, h_bin))
    # i4 = np.digitize(state[-1], bins=np.linspace(-109, 400, v_bin))

    # return i1 - 1, i2 - 1, i3 - 1, i4 - 1

    i1 = np.digitize(state[0], bins=np.linspace(-14, 466, v_bin))
    i2 = np.digitize(state[1], bins=np.linspace(-260, 145, h_bin))

    return i1 - 1, i2 - 1


def get_action(Q, state):
    i1, i2 = state
    if Q[i1][i2][1] > Q[i1][i2][0]:
        return 1
    elif Q[i1][i2][1] < Q[i1][i2][0]:
        return 0
    else:
        return np.random.randint(0, 2)

def update_Qtable(Q, state, n_state, action, reward):
    i1, i2 = state
    n1, n2 = n_state
    Q[i1][i2][action] = 0.4 * Q[i1][i2][action] + (0.6) * (reward + max(Q[n1][n2][:]))

if __name__ == "__main__":

    env = FlappyBirdEnv(render_mode="rgb")

    obs = env.reset()

    v_bin = 12
    h_bin = 12

    q_table = np.zeros((v_bin, h_bin, 2), dtype=np.float32)
    # q_table = np.load("./q_table_flappy_bird.npy")

    n_training_episode = 10_000
    max_step = 250
    
    eps = []
    rewards = []
    reward_per_run = 0
    min_max_arr = [float("inf"), float("-inf"), float("inf"), float("-inf")]
    # min_v, max_v = float("inf"), float("-inf") 
    # min_h, max_h = float("inf"), float("-inf") 
    
    plt.ion()
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))

    for i in range(n_training_episode):
        for step in range(max_step):
            # print(obs)
            if min_max_arr[0] > obs[0]:
                min_max_arr[0] = obs[0]
            if min_max_arr[1] < obs[0]:
                min_max_arr[1] = obs[0]
            if min_max_arr[2] > obs[1]:
                min_max_arr[2] = obs[1]
            if min_max_arr[3] < obs[1]:
                min_max_arr[3] = obs[1]
            
            i1, i2 = discretize_state(obs, v_bin, h_bin)

            action = get_action(q_table, (i1, i2))
            n_obs, reward, terminate = env.step(action)

            n1, n2 = discretize_state(n_obs, v_bin, h_bin)

            update_Qtable(q_table, (i1, i2), (n1, n2), action, reward)
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

            if i % 1000 == 0:
                np.save(f"./q_table_step_{i}.npy", q_table)

    plt.tight_layout()
    plt.show()
    np.save("./q_table_flappy_bird.npy", q_table)


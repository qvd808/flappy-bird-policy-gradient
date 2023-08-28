import gym
from gym import spaces
import numpy as np

def get_distance_first_pipe():
    return 0, 0

class FlappyBirdEnv(gym.Env):
    def __init__(self) -> None:
        super().__init__()
        self.action_space = gym.space.Discrete(2)
        self.observation_space = gym.space.Box(low = 0, high = 150, shape=(2, 0), dtype=np.float32)

    def step(self, action):
        pipe_up, pipe_down = get_distance_first_pipe()

        if action == 0:
            dir = "do nothing"
        else:
            dir = "flap"


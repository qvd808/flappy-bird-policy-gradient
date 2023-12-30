import gymnasium as gym
import numpy as np
from game_logic import FlappyBird
from renderer import FlappyBirdRender
import pygame

class FlappyBirdEnv(gym.Env):
    def __init__(self, render_mode) -> None:
        self.action_space = gym.spaces.Discrete(2)
        self.observation_space = gym.spaces.Box(-np.inf, np.inf, shape = (2, ), dtype = np.float32)

        self.game = FlappyBird(
            screen_height=800,
            screen_width=600
        )
        match render_mode:
            case "human":
                self.renderer = FlappyBirdRender(game=self.game)
                self.renderer.make_display()
                self.renderer.update_surface()
                self.renderer.update_display()
            case _:
                self.renderer = None
    
    def step(self, action):
        self.game.input_action(action)
        terminate = False
        reward = 1
        
        if self.game.next_state():
            terminate = True

        if self.renderer != None:
            self.renderer.update_surface()
            self.renderer.update_display()

        return (self._get_observation(), reward, terminate)


    def reset(self):
        self.game.reset()
        return self._get_observation()
    
    def _get_observation(self):
        
        # bird_x = self.game.bird_x
        # bird_y = self.game.bird_y
        v_dist = float("inf")
        h_dist = 0
        for pipe in self.game.upper_pipes:
            if self.game.upper_pipes[pipe][0] + FlappyBird.SpriteClass.LOWER_PIPE.get_width() - self.game.bird_x < 0:
                continue
            if v_dist > (self.game.upper_pipes[pipe][0] + FlappyBird.SpriteClass.LOWER_PIPE.get_width() // 2 - self.game.bird_x + FlappyBird.SpriteClass.BIRD.get_width() // 2):
                v_dist = self.game.upper_pipes[pipe][0] + FlappyBird.SpriteClass.LOWER_PIPE.get_width() // 2 - self.game.bird_x + FlappyBird.SpriteClass.BIRD.get_width() // 2
                h_dist = self.game.upper_pipes[pipe][1] + FlappyBird.SpriteClass.LOWER_PIPE.get_height() - self.game.bird_y

        return np.array(
            [v_dist, h_dist], dtype=np.float32
        )


    def _test_get_observation(self):
        if self.renderer != None:
            self.renderer.main_loop()

if __name__ == "__main__":
    env = FlappyBirdEnv(render_mode="rgb")
    while True:
        obs = env.reset()
        for step in range(1, 1000):
            obs, reward, terminate = env.step(step % 2)
            print(obs, reward, terminate)
            if terminate:
                break
        

        

import gym
from gym import spaces
import pygame
import numpy as np
import random, sys
from flappy_bird import Bird

class FlappyBirdEnv(gym.Env):

    pygame.init()


    def __init__(self, render_mode):
        self.action_space = gym.spaces.Discrete(2)
        self.observation_space = gym.spaces.Box(-np.inf, np.inf, shape = (2, ), dtype = np.float32)

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 900

        self.pipe_space_max_x = 288
        self.pipe_space_min_x = 266
        self.pipe_space_max_y = 220
        self.pipe_space_min_y = 150
        self.ground_scroll = 0

        self.max_pressing_space_safe = 200

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")

        self.bg = pygame.image.load("img/bg.png")
        self.ground_img = pygame.image.load("img/ground.png")
        self.pipe = pygame.image.load("img/pipe.png")
        self.reverse_pipe = pygame.transform.flip(self.pipe, False, True)

        self.bird1 = pygame.image.load("img/bird1.png")
        self.bird2 = pygame.image.load("img/bird2.png")
        self.bird3 = pygame.image.load("img/bird3.png")


        self.pipe_scroll_array = [0] * ( self.SCREEN_WIDTH // self.pipe_space_max_x + 2)
        self.pipe_delta_array = [0] * ( self.SCREEN_WIDTH // self.pipe_space_max_x + 2)
        self.max_distance_pipe = -1 
        self.closest_pipe = 0


        for i, pos in enumerate(self.pipe_scroll_array):
            self.pipe_scroll_array[i] += self.SCREEN_WIDTH + self.pipe.get_width() + (i * self.pipe_space_max_x)
            prev_index = (i - 1) % len(self.pipe_delta_array)
            max_h = self.pipe_delta_array[prev_index] + random.randint(-1 * self.max_pressing_space_safe, self.max_pressing_space_safe)
            if max_h > 320:
                max_h = 320
            if max_h < -self.ground_img.get_height():
                max_h = -self.ground_img.get_height()
            self.pipe_delta_array[i] = max_h
        
        self.bird = Bird(self.screen, self.ground_img)


   

    def step(self, action):
        
        ## Return obs, reward, end_game?, info

        y_bird, bird_velocity, bird_to_top, bird_to_bottom = 0, 0, 0, 0
        y_bird = self.bird.pos
        bird_velocity = self.bird.velocity
        reward  = 1
        info = {}

        def generate_pipe(y_pos, pipe_space_y, delta, mask_bird):

            ## Have an array of pipe on the screen (depend on the width of the screen). Only check collison for the first pipe since it is more efficient
            pipe_sprite = self.screen.blit(self.pipe, (y_pos, self.SCREEN_HEIGHT - self.pipe.get_height() + delta))
            reverse_pipe_sprite = self.screen.blit(self.reverse_pipe, (y_pos, self.SCREEN_HEIGHT - 2 * self.pipe.get_height() - pipe_space_y + delta))

            # if (pipe_sprite.colliderect(mask_bird)) or (reverse_pipe_sprite.colliderect(mask_bird)):
            #     pygame.quit()

            return (pipe_sprite.colliderect(mask_bird)) or (reverse_pipe_sprite.colliderect(mask_bird))

        speed = 4
        # while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if action:
            self.bird.fly()
        
        self.clock.tick(self.fps)

        self.screen.blit(self.bg, (0, 0))

        mask_bird = self.bird.update_pos()

        ## bottom = SCREEN_HEIGHT - pipe.get_height(), SCREEN_HEIGHT - pipe.get_height() + delta is top

        if self.pipe_scroll_array[self.closest_pipe] - speed < 300:
            self.closest_pipe = (self.closest_pipe + 1) % len(self.pipe_scroll_array)
        
        bird_to_bottom = self.SCREEN_HEIGHT - self.pipe.get_height() + self.pipe_delta_array[self.closest_pipe]
        bird_to_top = self.SCREEN_HEIGHT - self.pipe.get_height() + self.pipe_delta_array[self.closest_pipe] - self.pipe_space_min_y
        


        for i, pos in enumerate(self.pipe_scroll_array):
            lose_game = generate_pipe(self.pipe_scroll_array[i], self.pipe_space_min_y, self.pipe_delta_array[i], mask_bird)

            if lose_game:
                break

            self.pipe_scroll_array[i] -= speed
            if self.pipe_scroll_array[i] + self.pipe.get_width() <= -10:
                self.pipe_scroll_array[i] = self.pipe_scroll_array[self.max_distance_pipe] + self.pipe_space_max_x
                prev_index = (i - 1) % len(self.pipe_delta_array)
                max_h = self.pipe_delta_array[prev_index] + random.randint(-1 * self.max_pressing_space_safe, self.max_pressing_space_safe)
                if max_h > 320:
                    max_h = 320
                if max_h < -self.ground_img.get_height():
                    max_h = -self.ground_img.get_height()
                self.pipe_delta_array[i] = max_h
                self.max_distance_pipe = i
        
        ## Uncomment this make the game goes paused after bird die
        # if lose_game:
        #     pause = True
        #     while pause:
        #         for event in pygame.event.get():
        #             if event.type == pygame.QUIT:
        #                 pause = False
        #                 run = False

        self.screen.blit(self.ground_img, (self.ground_scroll, self.SCREEN_HEIGHT - self.ground_img.get_height()))
        self.ground_scroll -= speed

        if self.ground_scroll + self.ground_img.get_width() == self.SCREEN_WIDTH:
            self.ground_scroll = 0

        pygame.display.update()

        return (y_bird, bird_velocity, bird_to_top, bird_to_bottom), reward, lose_game, info


    
    def reset(self):

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 900

        self.pipe_space_max_x = 288
        self.pipe_space_min_x = 266
        self.pipe_space_max_y = 220
        self.pipe_space_min_y = 150
        self.ground_scroll = 0

        self.max_pressing_space_safe = 200

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.pipe_scroll_array = [0] * ( self.SCREEN_WIDTH // self.pipe_space_max_x + 2)
        self.pipe_delta_array = [0] * ( self.SCREEN_WIDTH // self.pipe_space_max_x + 2)
        self.max_distance_pipe = -1 
        self.closest_pipe = 0


        for i, pos in enumerate(self.pipe_scroll_array):
            self.pipe_scroll_array[i] += self.SCREEN_WIDTH + self.pipe.get_width() + (i * self.pipe_space_max_x)
            prev_index = (i - 1) % len(self.pipe_delta_array)
            max_h = self.pipe_delta_array[prev_index] + random.randint(-1 * self.max_pressing_space_safe, self.max_pressing_space_safe)
            if max_h > 320:
                max_h = 320
            if max_h < -self.ground_img.get_height():
                max_h = -self.ground_img.get_height()
            self.pipe_delta_array[i] = max_h
        
        self.bird = Bird(self.screen, self.ground_img)


if __name__ == "__main__":
    env = FlappyBirdEnv(render_mode = "human")
    while True:
        for j in range(300):
            if j % 18 == 0:
                action = 1
            else:
                action = 0

            obs, reward, terminate, info = env.step(action)

            if terminate:
                env.reset()
                break

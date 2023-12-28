import pygame
from typing import Dict, Tuple

class FlappyBird:
    def __init__(
        self,
        screen_width,
        screen_height
    ) -> None:
        
        ## Game properties
        self.screen_width = screen_width
        self.screen_height = screen_height

        ## Bird properties
        self.bird_x = self.screen_width // 5
        self.bird_y = self.screen_height // 2
        self.bird_vel = 6

        ## ground
        self.ground_x = 0
        self.ground_y = self.screen_height - self.SpriteClass.GROUND.get_height()

        ## pipe properties
        self.pipe_height: int = self.SpriteClass.LOWER_PIPE.get_height()
        self.pipe_width: int = self.SpriteClass.LOWER_PIPE.get_width()
        self.pipe_gap: int = 250 # space between upper and lower pipe
        self.pipes: Dict[0, Tuple(int, int)] = {
            0:  (self.screen_width - self.pipe_width, -300),
            1:  (self.screen_width - self.pipe_width + 250, -300),
            2:  (self.screen_width - self.pipe_width + 500, -300),
            3:  (self.screen_width - self.pipe_width + 750, -300),
            4:  (self.screen_width - self.pipe_width + 750, -300),
        }
        self.pipe_vel:int = -4

    class SpriteClass:
        BIRD = pygame.image.load("img/bird1.png")
        GROUND = pygame.image.load("img/ground.png")
        BG = pygame.image.load("img/bg.png")
        LOWER_PIPE = pygame.image.load("img/pipe.png")
        UPPER_PIPE = pygame.transform.flip(LOWER_PIPE, False, True)

    def update_pipe(self):
        for pipe in self.pipes:
            old_x, old_y = self.pipes[pipe]
            if old_x + self.pipe_width + self.pipe_vel < 0:
                furthest_x, _ = self.pipes[(pipe + 4) % 5]
                self.pipes[pipe] = (furthest_x + 250, -300)
            else:
                self.pipes[pipe] = (old_x + self.pipe_vel, old_y)
        

    def next_state(self):
        self.update_pipe()
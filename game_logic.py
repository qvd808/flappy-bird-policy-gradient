import pygame
from typing import Dict, Tuple

def is_collision(rect1, rect2):
    # rect1 and rect2 are represented as (x, y, width, height)

    # Calculate the coordinates of the four corners for each rectangle
    rect1_left = rect1[0]
    rect1_right = rect1[0] + rect1[2]
    rect1_top = rect1[1]
    rect1_bottom = rect1[1] + rect1[3]

    rect2_left = rect2[0]
    rect2_right = rect2[0] + rect2[2]
    rect2_top = rect2[1]
    rect2_bottom = rect2[1] + rect2[3]

    # Check for overlap along the x-axis
    x_overlap = not (rect1_right < rect2_left or rect1_left > rect2_right)

    # Check for overlap along the y-axis
    y_overlap = not (rect1_bottom < rect2_top or rect1_top > rect2_bottom)

    # If there is overlap along both axes, the rectangles collide
    return x_overlap and y_overlap

class FlappyBird:
    def __init__(
        self,
        screen_width,
        screen_height
    ) -> None:
        
        ## Game properties
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.score = 0

        ## Bird properties
        self.bird_x = self.screen_width // 5
        self.bird_y = self.screen_height // 2
        self.bird_vel = 4
        self.bird_acc = 1
        self.bird_max_vel = 6
        self._bird_flapped = False

        ## ground
        self.ground_x = 0
        self.ground_y = self.screen_height - self.SpriteClass.GROUND.get_height()
        self.ground_vel = -4

        ## pipe properties
        self.pipe_height: int = self.SpriteClass.LOWER_PIPE.get_height()
        self.pipe_width: int = self.SpriteClass.LOWER_PIPE.get_width()
        self.pipe_gap: int = 250 # space between upper and lower pipe
        self.upper_pipes: Dict[0, Tuple(int, int)] = {
            0:  (self.screen_width - self.pipe_width, -300),
            1:  (self.screen_width - self.pipe_width + 250, -300),
            2:  (self.screen_width - self.pipe_width + 500, -300),
            3:  (self.screen_width - self.pipe_width + 750, -300),
            4:  (self.screen_width - self.pipe_width + 750, -300),
        }
        self.lower_pipes: Dict[0, Tuple(int, int)] = {
            0:  (self.screen_width - self.pipe_width, -300 + self.pipe_height + self.pipe_gap),
            1:  (self.screen_width - self.pipe_width + 250, -300 + self.pipe_height + self.pipe_gap),
            2:  (self.screen_width - self.pipe_width + 500, -300 + self.pipe_height + self.pipe_gap),
            3:  (self.screen_width - self.pipe_width + 750, -300 + self.pipe_height + self.pipe_gap),
            4:  (self.screen_width - self.pipe_width + 750, -300 + self.pipe_height + self.pipe_gap),
        }
        self.closest_pipe = 0
        self.pipe_vel:int = -4

    class SpriteClass:
        BIRD = pygame.image.load("img/bird1.png")
        GROUND = pygame.image.load("img/ground.png")
        BG = pygame.image.load("img/bg.png")
        LOWER_PIPE = pygame.image.load("img/pipe.png")
        UPPER_PIPE = pygame.transform.flip(LOWER_PIPE, False, True)

    def update_pipe(self):
        for pipe in self.upper_pipes:
            old_x, old_y = self.upper_pipes[pipe]
            if old_x + self.pipe_width + self.pipe_vel < 0:
                furthest_x, _ = self.upper_pipes[(pipe + 4) % 5]
                self.upper_pipes[pipe] = (furthest_x + 250, -300)
                self.closest_pipe = (self.closest_pipe + 1) % 5
                self.score += 1
            else:
                self.upper_pipes[pipe] = (old_x + self.pipe_vel, old_y)

        for pipe in self.lower_pipes:
            old_x, old_y = self.lower_pipes[pipe]
            if old_x + self.pipe_width + self.pipe_vel < 0:
                furthest_x, _ = self.lower_pipes[(pipe + 4) % 5]
                self.lower_pipes[pipe] = (furthest_x + 250, -300 + self.pipe_height + self.pipe_gap)
            else:
                self.lower_pipes[pipe] = (old_x + self.pipe_vel, old_y)
    
    def update_bird(self):
        self.bird_y += min(
            self.bird_vel, self.ground_y - self.bird_y - self.SpriteClass.BIRD.get_height()
        )

        if self.bird_y < 0:
            self.bird_y =  0

    def update_ground(self):
        self.ground_x += self.ground_vel
        if self.ground_x + self.SpriteClass.GROUND.get_width() == self.screen_width:
            self.ground_x = 0
    
    def check_crash(self):

        for pipe in self.upper_pipes:
            pipe_x, pipe_y = self.upper_pipes[pipe]
            if is_collision((self.bird_x, self.bird_y, self.SpriteClass.BIRD.get_width(), self.SpriteClass.BIRD.get_height()),
                            (pipe_x, pipe_y, self.SpriteClass.UPPER_PIPE.get_width(), self.SpriteClass.UPPER_PIPE.get_height())
                            ):
                return True
            
        for pipe in self.lower_pipes:
            pipe_x, pipe_y = self.lower_pipes[pipe]
            if is_collision((self.bird_x, self.bird_y, self.SpriteClass.BIRD.get_width(), self.SpriteClass.BIRD.get_height()),
                            (pipe_x, pipe_y, self.SpriteClass.LOWER_PIPE.get_width(), self.SpriteClass.LOWER_PIPE.get_height())
                            ):
                return True

        return False
    
    def input_action(self, action: int):
        if action:
            if self.bird_y > -2 * self.SpriteClass.BIRD.get_height():
                self.bird_vel = -9
                self._bird_flapped = True
        
        if self.bird_vel < 10 and not self._bird_flapped:
            self.bird_vel += 1
        
        if self._bird_flapped:
            self._bird_flapped = False

    def next_state(self)-> bool: # Return wheter the games ends or not
        self.update_pipe()
        self.update_bird()
        self.update_ground()
        if self.check_crash():
            return True

        return False
    
    def reset(self):
                
        ## Bird properties
        self.bird_x = self.screen_width // 5
        self.bird_y = self.screen_height // 2
        self.bird_vel = 4
        self.bird_acc = 1
        self.bird_max_vel = 6

        ## ground
        self.ground_x = 0
        self.ground_y = self.screen_height - self.SpriteClass.GROUND.get_height()
        self.ground_vel = -4

        ## pipe properties
        self.pipe_height: int = self.SpriteClass.LOWER_PIPE.get_height()
        self.pipe_width: int = self.SpriteClass.LOWER_PIPE.get_width()
        self.pipe_gap: int = 250 # space between upper and lower pipe
        self.upper_pipes: Dict[0, Tuple(int, int)] = {
            0:  (self.screen_width - self.pipe_width, -300),
            1:  (self.screen_width - self.pipe_width + 250, -300),
            2:  (self.screen_width - self.pipe_width + 500, -300),
            3:  (self.screen_width - self.pipe_width + 750, -300),
            4:  (self.screen_width - self.pipe_width + 750, -300),
        }
        self.lower_pipes: Dict[0, Tuple(int, int)] = {
            0:  (self.screen_width - self.pipe_width, -300 + self.pipe_height + self.pipe_gap),
            1:  (self.screen_width - self.pipe_width + 250, -300 + self.pipe_height + self.pipe_gap),
            2:  (self.screen_width - self.pipe_width + 500, -300 + self.pipe_height + self.pipe_gap),
            3:  (self.screen_width - self.pipe_width + 750, -300 + self.pipe_height + self.pipe_gap),
            4:  (self.screen_width - self.pipe_width + 750, -300 + self.pipe_height + self.pipe_gap),
        }
        self.closest_pipe = 0
        self.pipe_vel:int = -4
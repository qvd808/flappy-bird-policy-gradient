import pygame
import __future__
from game_logic import FlappyBird
import numpy as np

class FlappyBirdRender():
    def __init__(
        self,
        game      
    ) -> None:
        
        ## Initialize some parameters
        self.display = None
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.game = game
        self.surface = pygame.Surface((game.screen_width, game.screen_height))
        
    def run_in_fps(self):
        self.clock.tick(self.fps)

    def make_display(self):
        self.display = pygame.display.set_mode((self.game.screen_width, self.game.screen_height))
        
    def update_surface(self):
        self.surface.fill((0, 0, 0)) #reset surface
        self.surface.blit(FlappyBird.SpriteClass.BG, (0, 0))
        
        for coor in self.game.upper_pipes.values():
            self.surface.blit(FlappyBird.SpriteClass.UPPER_PIPE, (coor[0], coor[1]))
            # self.surface.blit(FlappyBird.SpriteClass.LOWER_PIPE, (coor[0], coor[1] + self.game.pipe_height + self.game.pipe_gap))

        for coor in self.game.lower_pipes.values():
            self.surface.blit(FlappyBird.SpriteClass.LOWER_PIPE, (coor[0], coor[1]))
            # self.surface.blit(FlappyBird.SpriteClass.LOWER_PIPE, (coor[0], coor[1] + self.game.pipe_height + self.game.pipe_gap))


        self.surface.blit(FlappyBird.SpriteClass.GROUND, (self.game.ground_x, self.game.ground_y))

        self.surface.blit(FlappyBird.SpriteClass.BIRD, (self.game.bird_x, self.game.bird_y))
        ###

        # bird_x = self.game.bird_x
        # bird_y = self.game.bird_y
        # v_dist = float("inf")
        # upper_pipe_coor = (0, 0)
        # for pipe in self.game.upper_pipes:
        #     if self.game.upper_pipes[pipe][0] + FlappyBird.SpriteClass.LOWER_PIPE.get_width() - self.game.bird_x < 0:
        #         continue
        #     if v_dist > (self.game.upper_pipes[pipe][0] + FlappyBird.SpriteClass.LOWER_PIPE.get_width() // 2 - self.game.bird_x + FlappyBird.SpriteClass.BIRD.get_width() // 2):
        #         v_dist = self.game.upper_pipes[pipe][0] + FlappyBird.SpriteClass.LOWER_PIPE.get_width() // 2 - self.game.bird_x + FlappyBird.SpriteClass.BIRD.get_width() // 2
        #         upper_pipe_coor = (self.game.upper_pipes[pipe][0] + FlappyBird.SpriteClass.LOWER_PIPE.get_width() // 2,
        #                 self.game.upper_pipes[pipe][1] + FlappyBird.SpriteClass.LOWER_PIPE.get_height())
        # lower_pipe_coor = upper_pipe_coor[0], upper_pipe_coor[1] + self.game.pipe_gap

        # pygame.draw.circle(self.surface, (217, 33, 33), upper_pipe_coor, 5)
        # pygame.draw.circle(self.surface, (217, 33, 33), lower_pipe_coor, 5)
        # pygame.draw.line(self.surface,(217, 33, 33), (bird_x + FlappyBird.SpriteClass.BIRD.get_width() // 2, 0), (bird_x + FlappyBird.SpriteClass.BIRD.get_width() // 2, self.game.screen_height))
        # # if self.renderer != None:
        # pygame.draw.line(self.surface, (217,33,33), (bird_x + FlappyBird.SpriteClass.BIRD.get_width() // 2, bird_y + FlappyBird.SpriteClass.BIRD.get_height() // 2), upper_pipe_coor)
        # pygame.draw.line(self.surface, (217,33,33), (bird_x + FlappyBird.SpriteClass.BIRD.get_width() // 2, bird_y + FlappyBird.SpriteClass.BIRD.get_height() // 2), lower_pipe_coor)

    def update_display(self):
        if self.display == None:
            raise ValueError("There is no display")

        self.run_in_fps()

        self.display.blit(self.surface, [0, 0])
        pygame.display.update()
        

    def main_loop(self):
        run =  True

        self.make_display()

        while run:
            action = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        action = 1
            
            self.clock.tick(self.fps)
            self.game.next_state()
            self.game.input_action(action)

            # action = np.random.randint(0, 2)

            self.update_surface()
            self.update_display()

if __name__ == "__main__":
    game = FlappyBird(
        screen_height=800,
        screen_width=800
    )
    render = FlappyBirdRender(game=game)
    render.main_loop()
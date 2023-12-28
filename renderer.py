import pygame
import __future__
from test_game_logic import FlappyBird

class FlappyBirdRender():
    def __init__(
        self,
        game      
    ) -> None:
        
        ## Initialize some parameters
        self.display = None
        
        self.game = game
        self.background = pygame.image.load("img/bg.png")
        self.surface = pygame.Surface((game.screen_width, game.screen_height))
        
    
    def make_display(self):
        self.display = pygame.display.set_mode((self.game.screen_width, self.game.screen_height))
        
    def update_surface(self):
        self.surface.blit(self.background, (0, 0))

    def update_display(self):
        if self.display == None:
            raise ValueError("There is no display")

        self.display.blit(self.surface, [0, 0])
        pygame.display.update()
        

    def main_loop(self):
        run =  True

        self.make_display()

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            self.update_surface()
            self.update_display()


if __name__ == "__main__":
    game = FlappyBird(
        screen_height=800,
        screen_width=600
    )
    render = FlappyBirdRender(game=game)
    render.main_loop()
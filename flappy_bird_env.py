import pygame
import random, sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

bg = pygame.image.load("img/bg.png")
ground_img = pygame.image.load("img/ground.png")
pipe = pygame.image.load("img/pipe.png")
reverse_pipe = pygame.transform.flip(pipe, False, True)

bird1 = pygame.image.load("img/bird1.png")
bird2 = pygame.image.load("img/bird2.png")
bird3 = pygame.image.load("img/bird3.png")

def generate_pipe(y_pos, pipe_space_y, delta):

    ## Have an array of pipe on the screen (depend on the width of the screen). Only check collison for the first pipe since it is more efficient
    pipe_sprite = screen.blit(pipe, (y_pos, SCREEN_HEIGHT - pipe.get_height()))
    reverse_pipe_sprite = screen.blit(reverse_pipe, (y_pos,  SCREEN_HEIGHT - pipe.get_height() - 50))


    reverse_pipe_sprite = screen.blit(reverse_pipe, (y_pos+100,  SCREEN_HEIGHT - 2*pipe.get_height() - 50))


    # if (pipe_sprite.colliderect(mask_bird)) or (reverse_pipe_sprite.colliderect(mask_bird)):
    #     pygame.quit()

    # return (pipe_sprite.colliderect(mask_bird)) or (reverse_pipe_sprite.colliderect(mask_bird))
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    
    generate_pipe(300, 100, 0)

    pygame.display.update()
import pygame
import random

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

def generate_pipe(y_pos, pipe_space_y):

    ## Have an array of pipe on the screen (depend on the width of the screen). Only check collison for the first pipe since it is more efficient
    screen.blit(pipe, (y_pos, SCREEN_HEIGHT - pipe.get_height()))
    screen.blit(reverse_pipe, (y_pos, SCREEN_HEIGHT - 2 * pipe.get_height() - pipe_space_y))

pipe_space_max_x = 288
pipe_space_min_x = 266
pipe_space_max_y = 200
pipe_space_min_y = 130


ground_scroll = 0
pipe_scroll = SCREEN_WIDTH - pipe.get_width() + 100

pipe_scroll_array = [0] * ( SCREEN_WIDTH // pipe_space_max_x + 2)
for i, pos in enumerate(pipe_scroll_array):
    pipe_scroll_array[i] += SCREEN_WIDTH + pipe.get_width() + (i * pipe_space_max_x)

print(pipe_scroll_array)
max_distance_pipe = -1


# pipe_scroll = 0
speed = 4
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    clock.tick(fps)

    screen.blit(bg, (0, 0))

    for i, pos in enumerate(pipe_scroll_array):
        generate_pipe(pipe_scroll_array[i], pipe_space_min_y)
        pipe_scroll_array[i] -= speed
        if pipe_scroll_array[i] + pipe.get_width() <= -10:
           pipe_scroll_array[i] = pipe_scroll_array[max_distance_pipe] + pipe_space_max_x
           max_distance_pipe = i


    screen.blit(ground_img, (ground_scroll, SCREEN_HEIGHT - ground_img.get_height()))
    ground_scroll -= speed


    if ground_scroll + ground_img.get_width() == SCREEN_WIDTH:
        ground_scroll = 0



        


    pygame.display.update()

pygame.quit()
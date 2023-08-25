import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

bg = pygame.image.load("img/bg.png")
ground_img = pygame.image.load("img/ground.png")

ground_scroll = 0
speed = 4
run = True
while run:

    clock.tick(fps)

    screen.blit(bg, (0, 0))

    screen.blit(ground_img, (ground_scroll, SCREEN_HEIGHT - ground_img.get_height()))
    ground_scroll -= speed

    if ground_scroll + ground_img.get_width() == SCREEN_WIDTH:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        


    pygame.display.update()

pygame.quit()
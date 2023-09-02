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

class Bird:
    def __init__(self, screen, ground_img) -> None:
        self.animations = [bird1, bird2, bird3]
        self.frame = 0
        self.speed = 0
        self.max_vel = 6
        self.velocity = self.max_vel
        self.pos = 300
        self.screen = screen
        self.ground_img = ground_img
    
    def get_bird(self):
        # bird = self.animations[self.frame]
        if self.velocity == 0:
            return self.animations[1]
        elif self.velocity > 0:
            return self.animations[0]
        else:
            return self.animations[2]
        # return bird

    def update_pos(self):
        if self.velocity + 1 <= self.max_vel:
            self.velocity += 1
        else:
            self.velocity = self.max_vel

        if self.pos + self.velocity <= SCREEN_HEIGHT - self.ground_img.get_height() - self.get_bird().get_height():
            self.pos = self.pos + self.velocity
        else:
            self.pos = SCREEN_HEIGHT - self.ground_img.get_height() - self.get_bird().get_height()
        
        result = self.screen.blit(self.get_bird(), (300, self.pos))

        return result

    def fly(self):
        self.velocity = -10

bird = Bird(screen, ground_img)

# def offset(mask1, mask2):
#     return int(mask2.x - mask1.x), int(mask2.y - mask1.y)

def generate_pipe(y_pos, pipe_space_y, delta, mask_bird):

    ## Have an array of pipe on the screen (depend on the width of the screen). Only check collison for the first pipe since it is more efficient
    pipe_sprite = screen.blit(pipe, (y_pos, SCREEN_HEIGHT - pipe.get_height() + delta))
    reverse_pipe_sprite = screen.blit(reverse_pipe, (y_pos, SCREEN_HEIGHT - 2 * pipe.get_height() - pipe_space_y + delta))

    # if (pipe_sprite.colliderect(mask_bird)) or (reverse_pipe_sprite.colliderect(mask_bird)):
    #     pygame.quit()

    return (pipe_sprite.colliderect(mask_bird)) or (reverse_pipe_sprite.colliderect(mask_bird))
    

def main():

    pipe_space_max_x = 288
    pipe_space_min_x = 266
    pipe_space_max_y = 220
    pipe_space_min_y = 150


    ground_scroll = 0
    pipe_scroll = SCREEN_WIDTH - pipe.get_width() + 100

    max_pressing_space_safe = 200

    pipe_scroll_array = [0] * ( SCREEN_WIDTH // pipe_space_max_x + 2)
    pipe_delta_array = [0] * ( SCREEN_WIDTH // pipe_space_max_x + 2)
    for i, pos in enumerate(pipe_scroll_array):
        pipe_scroll_array[i] += SCREEN_WIDTH + pipe.get_width() + (i * pipe_space_max_x)
        prev_index = (i - 1) % len(pipe_delta_array)
        max_h = pipe_delta_array[prev_index] + random.randint(-1 * max_pressing_space_safe, max_pressing_space_safe)
        if max_h > 320:
            max_h = 320
        if max_h < -ground_img.get_height():
            max_h = -ground_img.get_height()
        pipe_delta_array[i] = max_h

    ## Track the current pipe that is far away the most to change the distance for the first pipe to leave the screen
    max_distance_pipe = -1 


    # pipe_scroll = 0
    speed = 4
    run = True
    lose_game = False
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.fly()

        clock.tick(fps)

        screen.blit(bg, (0, 0))

        mask_bird = bird.update_pos()


        for i, pos in enumerate(pipe_scroll_array):
            lose_game = generate_pipe(pipe_scroll_array[i], pipe_space_min_y, pipe_delta_array[i], mask_bird)

            if lose_game:
                break

            pipe_scroll_array[i] -= speed
            if pipe_scroll_array[i] + pipe.get_width() <= -10:
                pipe_scroll_array[i] = pipe_scroll_array[max_distance_pipe] + pipe_space_max_x
                prev_index = (i - 1) % len(pipe_delta_array)
                max_h = pipe_delta_array[prev_index] + random.randint(-1 * max_pressing_space_safe, max_pressing_space_safe)
                if max_h > 320:
                    max_h = 320
                if max_h < -ground_img.get_height():
                    max_h = -ground_img.get_height()
                pipe_delta_array[i] = max_h
                max_distance_pipe = i
            
        if lose_game:
            pause = True
            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pause = False
                        run = False

        screen.blit(ground_img, (ground_scroll, SCREEN_HEIGHT - ground_img.get_height()))
        ground_scroll -= speed

        if ground_scroll + ground_img.get_width() == SCREEN_WIDTH:
            ground_scroll = 0



            
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
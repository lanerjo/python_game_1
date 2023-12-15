import sys
import pygame
import random
import time
from pygame.locals import *

# init pygame
pygame.init()

# Define Colors
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
GREY = pygame.Color(128,128,128)
RED = pygame.Color(255,0,0)

# # Variable for the Game
# SPEED = 5
# SCORE = 0

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

#Display Screen
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Game")

#Limit Frame Rate to human useable
FramesPerSecond = pygame.time.Clock()
FPS = 60

def reinitialize():
    # Variable for the Game
    global SPEED
    SPEED = 5
    global SCORE
    SCORE = 0
    # Init Sprites
    global E1
    E1 = Enemy()
    global P1
    P1 = Player()

    # Init Sprite Groups
    global enemies
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    global all_sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)

# Adding new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Enemy.png')
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0)
    def move(self):
        global SCORE
        self.rect.move_ip(0,10)
        if (self.rect.bottom > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, SCREEN_WIDTH-30), 0)
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,5)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# # Init Sprites
# E1 = Enemy()
# P1 = Player()
#
# # Init Sprite Groups
# enemies = pygame.sprite.Group()
# enemies.add(E1)
# all_sprites = pygame.sprite.Group()
# all_sprites.add(P1)
# all_sprites.add(E1)
#
# # Adding new User event
# INC_SPEED = pygame.USEREVENT + 1
# pygame.time.set_timer(INC_SPEED, 1000)

# Game loop
if __name__ == "__main__":
    reinitialize()
    while True:
        #Quit game loop
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 2

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(BLACK)
        scores = font_small.render(str(SCORE), True, WHITE)
        DISPLAYSURF.blit(scores, (10,10))

        # Moves and redraws all Sprites
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        if pygame.sprite.spritecollideany(P1, enemies):
            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (30,250))
            pygame.display.update()
            # kill all sprites in the event of a collision
            for entity in all_sprites:
                entity.kill()
            time.sleep(5)
            reinitialize()


        pygame.display.update()
        FramesPerSecond.tick(FPS)


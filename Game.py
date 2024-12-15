# A Space Invaders clone(sort of// more like a parody)
# By Gabriel Mortey
# A mini project.
import random
from sys import exit

import pygame
from pygame import mixer

# Initialize Pygame
pygame.init()

# Define game constants
WIDTH = 800
HEIGHT = 600
FPS = 60
FONT_NAME = pygame.font.match_font('arial')

# Define colors
RED = (225, 8, 99, 0.95)
GOLD = (245, 169, 39, 0.8)
WHITE = (30, 60, 90, 0.66)

# Background image
background = pygame.image.load("background1.png")
pygame.display.set_icon(background)

# Create the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Icon
icon = pygame.image.load("galaxy.png")
pygame.display.set_icon(icon)

# Load images
player_img = pygame.image.load('space-ship.png')
enemy_img = pygame.image.load('xtratsl.png')
bullet_img = pygame.image.load('bullet.png')
background_img = pygame.image.load('background1.png')


# Define functions
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, GOLD)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


# Adding countdown functionality
def show_countdown_screen():
    for i in range(3, 0, -1):
        screen.fill(WHITE)
        draw_text(screen, f'Game starts in {i}...!', 48, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()
        pygame.time.wait(1000)


def show_game_over_screen():
    screen.fill(WHITE)
    draw_text(screen, 'GAME OVER!', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, 'Press R to play again!', 24, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, 'Press Esc to exit', 24, WIDTH / 2, HEIGHT / 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                exit()
            if EVENT.type == pygame.KEYDOWN:
                if EVENT.key == pygame.K_r:
                    waiting = False
            if EVENT.type == pygame.KEYDOWN:
                if EVENT.key == pygame.K_ESCAPE:
                    exit()


# creating file to save high score
def get_high_score():
    try:
        with open("High_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


def save_score():
    with open("High_score.txt", "w") as file:
        file.write(str(score))


# Define Sprite classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        # plays laser sound when bullet is shot.
        bullets_sound = mixer.Sound('laser.wav')
        bullets_sound.play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (50, 38))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)

        # Plays explosion sound when enemy is killed

    def kill(self):
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        super().kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop where all the magic happens!
running = True
game_over = False
score = 0
high_score = get_high_score()

while running:
    if game_over:
        show_game_over_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

    # Adding countdown at game start
    if not all_sprites and not game_over:
        show_countdown_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        if score > high_score:
            high_score = score
            save_score()

        player = Player()
        all_sprites.add(player)

        for i in range(8):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        score = 0

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    # Check for bullet collisions with enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for player collisions with enemies
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        game_over = True

    screen.fill(RED)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, f"Score: {score}", 18, 40, 10)
    draw_text(screen, f"High Score: {high_score}", 18, WIDTH / 2, 10)

    pygame.display.flip()

# Quit the game
pygame.quit()

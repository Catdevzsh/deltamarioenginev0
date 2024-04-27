import pygame
from array import array
from random import randint, choice
from math import hypot

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platformer Level with Dynamic Sound')

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60  # Changed to 60 for smoother gameplay

# Sound Functions
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Sounds
jump_sound = generate_beep_sound(784, 0.05)
enemy_proximity_sound = generate_beep_sound(523.25, 0.1)
last_sound_play_time = 0  # To control sound play frequency

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((40, 40))
        self.surf.fill(BLUE)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5
        self.jump_speed = -10
        self.gravity = 0.5
        self.velocity = 0
        self.on_ground = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        
        # Handle jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity = self.jump_speed
            jump_sound.play()  # Play jump sound when jumping

        # Apply gravity
        self.velocity += self.gravity
        self.rect.move_ip(0, self.velocity)

        # Check for ground
        if self.rect.bottom >= SCREEN_HEIGHT - 100:
            self.rect.bottom = SCREEN_HEIGHT - 100
            self.on_ground = True
            self.velocity = 0
        else:
            self.on_ground = False

    def update(self):
        self.move()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill(RED)
        self.rect = self.surf.get_rect(center=(x, y))
        self.speed = choice([-2, 2])

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed *= -1

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.surf = pygame.Surface((width, 20))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(center=(x, y))

# Setup game entities
player = Player()
enemies = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create platforms and enemies
platform_positions = [(400, 500, 200), (150, 400, 100), (650, 300, 120)]
for x, y, width in platform_positions:
    platforms.add(Platform(x, y, width))

for _ in range(5):
    x = randint(50, SCREEN_WIDTH - 50)
    y = SCREEN_HEIGHT - 120
    enemies.add(Enemy(x, y))

# Helper function to check proximity
def check_proximity():
    global last_sound_play_time
    current_time = pygame.time.get_ticks()
    if current_time - last_sound_play_time > 1000:  # Only play sound every 1000 ms
        nearest = min(enemies, key=lambda e: hypot(e.rect.centerx - player.rect.centerx, e.rect.centery - player.rect.centery))
        distance = hypot(nearest.rect.centerx - player.rect.centerx, nearest.rect.centery - player.rect.centery)
        if distance < 100:
            enemy_proximity_sound.play()
            last_sound_play_time = current_time

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic
    player.update()
    enemies.update()
    check_proximity()

    # Collision with platforms
    for platform in platforms:
        if pygame.sprite.collide_rect(player, platform) and player.velocity >= 0:
            player.rect.bottom = platform.rect.top
            player.on_ground = True
            player.velocity = 0

    # Drawing
    screen.fill(WHITE)
    screen.blit(player.surf, player.rect)
    for entity in platforms:
        screen.blit(entity.surf, entity.rect)
    for enemy in enemies:
        screen.blit(enemy.surf, enemy.rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

 # [DELTA MARIO ENGINE V0X.X.X [C] 20XX TEAM FLAMES DEDICATED TO HUMMER TEAM]

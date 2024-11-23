import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 500, 600
FPS = 60
PLATFORM_WIDTH, PLATFORM_HEIGHT = 100, 20
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
GRAVITY = 0.5
JUMP_STRENGTH = 15
DOUBLE_JUMP_STRENGTH = 12

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumping Game")
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.vel_y = 0
        self.on_ground = False
        self.can_double_jump = False

    def update(self, platforms):
        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Collision with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.vel_y = 0
                self.rect.bottom = platform.rect.top
                self.on_ground = True
                self.can_double_jump = False  # Reset double jump when touching the ground

        # Jumping
        if self.on_ground:
            self.vel_y = 0

        # Moving the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

    def jump(self):
        if self.on_ground:
            self.vel_y = -JUMP_STRENGTH
            self.can_double_jump = True  # Enable double jump
        elif self.can_double_jump:
            self.vel_y = -DOUBLE_JUMP_STRENGTH
            self.can_double_jump = False  # Disable double jump after it's used

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.creation_time = time.time()

    def update(self):
        if time.time() - self.creation_time > 2:  # Platform disappears after 2 seconds
            self.kill()

# Moving Platform class
class MovingPlatform(Platform):
    def __init__(self, x, y, speed):
        super().__init__(x, y)
        self.speed = speed
        self.direction = 1  # 1 for right, -1 for left

    def update(self):
        # Move the platform left and right
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1  # Change direction when hitting screen edges
        super().update()

# Power-Up class (Double Jump)
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(CYAN)  # Cyan power-up color
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        if self.rect.colliderect(player.rect):
            # Activate double jump when collected
            player.can_double_jump = True
            self.kill()  # Remove power-up once collected

# Initialize platform and player groups
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

platforms = pygame.sprite.Group()
moving_platforms = pygame.sprite.Group()

# Create initial platforms
for _ in range(5):
    x = random.randint(50, WIDTH - 150)
    y = random.randint(100, HEIGHT - 200)
    platform = Platform(x, y)
    platforms.add(platform)

# Create moving platforms
for _ in range(2):
    x = random.randint(50, WIDTH - 150)
    y = random.randint(100, HEIGHT - 200)
    speed = random.randint(2, 5)
    moving_platform = MovingPlatform(x, y, speed)
    moving_platforms.add(moving_platform)

# Create a double-jump power-up
power_up = PowerUp(random.randint(50, WIDTH - 50), random.randint(100, HEIGHT - 100))
power_up_group = pygame.sprite.Group()
power_up_group.add(power_up)

# Main game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Update game objects
    player_group.update(platforms)  # Pass platforms to player.update
    platforms.update()
    moving_platforms.update()
    power_up_group.update()

    # Check if player has reached the top
    if player.rect.top <= 0:
        print("You won!")
        running = False

    # Draw everything
    player_group.draw(screen)
    platforms.draw(screen)
    moving_platforms.draw(screen)
    power_up_group.draw(screen)

    # Refresh the screen
    pygame.display.flip()

pygame.quit()

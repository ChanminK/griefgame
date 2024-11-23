import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Griever v Anger")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# FPS
FPS = 60


# Fighter class
class Fighter:
    def __init__(self, x, y, color, speed, damage):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 80
        self.color = color
        self.health = 100
        self.speed = speed
        self.attack = False
        self.damage = damage  # Damage dealt by this fighter

    def draw(self):
        # Draw the fighter
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Draw health bar
        pygame.draw.rect(screen, RED, (self.x, self.y - 20, 100, 10))  # Red background
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 20, self.health, 10))  # Green for health

    def move(self, keys=None, controls=None):
        if keys and controls:  # Player movement
            if keys[controls['left']]:
                self.x -= self.speed
            if keys[controls['right']]:
                self.x += self.speed
            if keys[controls['up']]:
                self.y -= self.speed
            if keys[controls['down']]:
                self.y += self.speed

        # Keep within screen boundaries
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

    def ai_move(self, target, delay_counter):
        # Move toward the player if the delay counter allows
        if delay_counter % 30 == 0:  # Adjust delay as needed (higher values = slower response)
            if self.x < target.x:
                self.x += self.speed
            elif self.x > target.x:
                self.x -= self.speed
            if self.y < target.y:
                self.y += self.speed
            elif self.y > target.y:
                self.y -= self.speed

        # Keep within screen boundaries
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

    def attack_enemy(self, enemy):
        if self.attack:  # Check if attack flag is True
            if pygame.Rect(self.x, self.y, self.width, self.height).colliderect(
                pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            ):
                enemy.health -= self.damage  # Decrease health based on this fighter's damage


# Create player and enemy objects
player = Fighter(100, 300, BLUE, speed=6, damage=5)  # Player is faster and does more damage
enemy = Fighter(600, 300, RED, speed=6, damage=3)  # Enemy is slower and does less damage

# Game loop variables
delay_counter = 5  # Counter to control enemy's delayed movement

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Increment delay counter
    delay_counter += 1

    # Get keys for movement and attacks
    keys = pygame.key.get_pressed()

    # Player movement
    player.move(keys, {
        'left': pygame.K_a,
        'right': pygame.K_d,
        'up': pygame.K_w,
        'down': pygame.K_s,
    })

    # Player attack
    player.attack = keys[pygame.K_SPACE]

    # AI movement and attack
    enemy.ai_move(player, delay_counter)
    enemy.attack = random.choice([True, False])  # Randomly decide if the AI attacks

    # Handle attacks
    player.attack_enemy(enemy)
    enemy.attack_enemy(player)

    # Draw fighters
    player.draw()
    enemy.draw()

    # Check for game over
    if player.health <= 0 or enemy.health <= 0:
        font = pygame.font.Font(None, 74)
        winner = "Enemy" if player.health <= 0 else "Player"
        text = font.render(f"{winner} Wins!", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    # Update display and maintain frame rate
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()

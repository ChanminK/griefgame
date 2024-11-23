import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bargaining: Find the Key")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font for displaying text
font = pygame.font.SysFont('Arial', 36)

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

# Define falling object class
class FallingObject(pygame.sprite.Sprite):
    def __init__(self, color, target=False):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 30)
        self.rect.y = random.randint(-50, -30)
        self.speed = random.randint(3, 6)
        self.target = target

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - 30)
            self.rect.y = random.randint(-50, -30)

# Create groups for all sprites and falling objects
all_sprites = pygame.sprite.Group()
falling_objects = pygame.sprite.Group()

# Create player object
player = Player()
all_sprites.add(player)

# Create random falling objects (blue)
for _ in range(5):
    obj = FallingObject(BLUE)
    falling_objects.add(obj)
    all_sprites.add(obj)

# Game variables
clock = pygame.time.Clock()
game_over = False
score = 0
key_secured = False
message = ""
key_fall_time = 0
key_wait_time = 20  # Time to wait before the red key falls again after missing
last_key_fall_time = 0

# Game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Update sprite positions
    all_sprites.update()

    # Time control for when the red key (target) falls
    current_time = time.time()
    if key_secured:
        # Reset wait time for next key fall after key is secured
        key_wait_time = 20
        key_fall_time = current_time + random.randint(15, 30)

    if not key_secured and (current_time - last_key_fall_time) >= key_wait_time:
        # Create red target falling object
        target_object = FallingObject(RED, target=True)
        falling_objects.add(target_object)
        all_sprites.add(target_object)

        # Update the time when the key fell
        last_key_fall_time = current_time
        key_wait_time = random.randint(15, 30)  # Randomize the next fall time (15-30 seconds)

    # Check for collisions with the target object
    if pygame.sprite.collide_rect(player, target_object) and not key_secured:
        key_secured = True
        message = "Key secured!"

    # Check for collisions with other falling objects (blue)
    for obj in falling_objects:
        if obj != target_object and pygame.sprite.collide_rect(player, obj):
            game_over = True
            print("Failed to Bargain.")
            break

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw all sprites
    all_sprites.draw(screen)

    # Display message if the key is secured
    if key_secured:
        text = font.render(message, True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
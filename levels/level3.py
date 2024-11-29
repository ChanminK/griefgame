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
BLUE = (0, 0, 255)

# Font for displaying text
font = pygame.font.SysFont('Arial', 36)

# Load images and sound
player_image_path = "assets/player.png"
key_image_path = "assets/key.png"
chest_image_path = "assets/chest3.png"
win_sound_path = "assets/win.mp3"

player_image = pygame.image.load(player_image_path)
player_image = pygame.transform.scale(player_image, (50, 50))

key_image = pygame.image.load(key_image_path)
key_image = pygame.transform.scale(key_image, (30, 30))

chest_image = pygame.image.load(chest_image_path)
chest_image = pygame.transform.scale(chest_image, (screen_width, screen_height))

pygame.mixer.init()
win_sound = pygame.mixer.Sound(win_sound_path)

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed = 5

    #MOVING
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

# Define falling object class
class FallingObject(pygame.sprite.Sprite):
    def __init__(self, color=None, target=False):
        super().__init__()
        if target:
            self.image = key_image
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill(BLUE)
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
    obj = FallingObject()
    falling_objects.add(obj)
    all_sprites.add(obj)

# Game variables
clock = pygame.time.Clock()
game_over = False
key_secured = False
message = ""
target_object = None

# Game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Update sprite positions
    all_sprites.update()

    # Create red target object (key) if it doesn't already exist
    if not target_object:
        target_object = FallingObject(target=True)
        falling_objects.add(target_object)
        all_sprites.add(target_object)

    # Check for collisions with the target object
    if target_object and pygame.sprite.collide_rect(player, target_object) and not key_secured:
        key_secured = True
        pygame.mixer.Sound.play(win_sound)  # Play the win sound
        message = "Bargaining Defeated"

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
        screen.blit(chest_image, (0, 0))  # Display the chest image
        text = font.render(message, True, BLUE)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2))
        pygame.display.flip()
        pygame.time.delay(3000)  # Show the chest and message for 3 seconds
        game_over = True

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()

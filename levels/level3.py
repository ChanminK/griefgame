import pygame
import random
import sys

pygame.init()

screen_width = 600
screen_height = 400
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont('Arial', 36)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bargaining: Find the Key")

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

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

# Falling object class
class FallingObject(pygame.sprite.Sprite):
    def __init__(self, target=False):
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

def show_lost_screen():
    fade_surface = pygame.Surface((screen_width, screen_height))  
    fade_surface.fill(BLACK)  
    for i in range(0, 256, 5): 
        fade_surface.set_alpha(i) 
        screen.blit(fade_surface, (0, 0))  
        pygame.display.flip() 
        pygame.time.delay(50) 
    message = "YOU ARE TO BLAME. TRY AGAIN"
    text_surface = font.render(message, True, WHITE)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(5000)
    pygame.quit()
    sys.exit() 

# Run level function
def run_level():
    
    all_sprites = pygame.sprite.Group()
    falling_objects = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # random falling objects
    for _ in range(5):
        obj = FallingObject()
        falling_objects.add(obj)
        all_sprites.add(obj)

    clock = pygame.time.Clock()
    key_secured = False
    target_object = None

    initial_display_time = 5000 
    start_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()

        if current_time - start_time < initial_display_time:
            screen.fill(BLACK)
            run_text = font.render("Bargain with the truth", True, WHITE)
            run_text_rect = run_text.get_rect(center=(screen_width // 2, screen_height // 2 - 20))
            screen.blit(run_text, run_text_rect)

            collect_text = font.render("Find the key and continue", True, WHITE)
            collect_text_rect = collect_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
            screen.blit(collect_text, collect_text_rect)

            pygame.display.flip()
            continue

        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        # Sprite update
        all_sprites.update()

        # Create the target object (key) if it doesn't already exist
        if not target_object:
            target_object = FallingObject(target=True)
            falling_objects.add(target_object)
            all_sprites.add(target_object)

        # Check for collisions with the target object
        if target_object and pygame.sprite.collide_rect(player, target_object) and not key_secured:
            key_secured = True
            pygame.mixer.Sound.play(win_sound)  # Play the win sound
            message = "Bargaining Defeated"

            # Display the chest image and message
            screen.blit(chest_image, (0, 0))
            text = font.render(message, True, BLUE)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2))
            pygame.display.flip()
            pygame.time.delay(3000)  # Show for 3 seconds
            return "completed"

        # Check for collisions with other falling objects (blue)
        for obj in falling_objects:
            if obj != target_object and pygame.sprite.collide_rect(player, obj):
                show_lost_screen()
                pygame.quit()
                sys.exit() 

        # Fill the screen with white
        screen.fill(WHITE)

        # Draw all sprites
        all_sprites.draw(screen)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
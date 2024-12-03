import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Functions
def run_level():
    # Initialize screen and clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Level 5 - Image Sequence")
    clock = pygame.time.Clock()

    # Load assets
    image_paths = [
        "assets/image1.png",
        "assets/image2.png",
        "assets/image3.png",
        "assets/image4.png",
        "assets/image5.png",
        "assets/image6.png",
    ]

    images = [pygame.image.load(path) for path in image_paths]
    images = [pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT)) for img in images]  # Scale to fit screen

    # Loopin
    current_image_index = 0
    image_display_time = 5000 
    last_switch_time = pygame.time.get_ticks()  

    while current_image_index < len(images):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        # Switch image
        current_time = pygame.time.get_ticks()
        if current_time - last_switch_time > image_display_time:
            current_image_index += 1
            last_switch_time = current_time

        # Current image
        if current_image_index < len(images):
            screen.fill((0, 0, 0))  #
            screen.blit(images[current_image_index], (0, 0))  
            pygame.display.flip()

        clock.tick(FPS)
    
    # ENDING
    screen.fill((0, 0, 0))  
    font = pygame.font.Font(None, 74)
    
    grief_text = font.render("Grief is difficult.", True, (255, 255, 255))
    grief_rect = grief_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
    screen.blit(grief_text, grief_rect)

    thank_you_text = font.render("Thank you for playing", True, (255, 255, 255))
    text_rect = thank_you_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    screen.blit(thank_you_text, text_rect)
    pygame.display.flip()

    pygame.time.delay(3000)  
    pygame.quit()
    sys.exit()
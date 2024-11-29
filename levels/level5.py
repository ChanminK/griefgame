import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Level 5 - Image Sequence")
clock = pygame.time.Clock()

# Load images (ensure you have these images in your project folder)
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

# Main game loop for Level 5
current_image_index = 0
image_display_time = 5000  # Time per image in milliseconds
last_switch_time = pygame.time.get_ticks()  # Track when to switch images

while current_image_index < len(images):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Check if it's time to switch to the next image
    current_time = pygame.time.get_ticks()
    if current_time - last_switch_time > image_display_time:
        current_image_index += 1
        last_switch_time = current_time

    # Display the current image
    if current_image_index < len(images):
        screen.fill((0, 0, 0))  # Fill screen with black (optional)
        screen.blit(images[current_image_index], (0, 0))  # Draw the current image
        pygame.display.flip()

    clock.tick(FPS)

# Level 5 done
pygame.quit()
sys.exit()

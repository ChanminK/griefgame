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
    "image1.png",
    "image2.png",
    "image3.png",
    "image4.png",
    "image5.png",
    "image6.png",
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

# Level 5 complete
pygame.quit()
sys.exit()

# import pygame
# import sys

# # Initialize Pygame
# pygame.init()

# # Screen dimensions and settings
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# FPS = 60

# # Initialize screen and clock
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Level 5 - Image Sequence")
# clock = pygame.time.Clock()

# # Load images (ensure you have these images in your project folder)
# image_paths = [
#     "image1.png",
#     "image2.png",
#     "image3.png",
#     "image4.png",
#     "image5.png",
#     "image6.png",
# ]

# images = [pygame.image.load(path) for path in image_paths]
# images = [pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT)) for img in images]  # Scale to fit screen

# # Level 5 function (formatted to work with main menu)
# def run_level5():
#     # Display each image for around 5 seconds
#     for img in images:
#         screen.fill((0, 0, 0))  # Fill screen with black (optional)
#         screen.blit(img, (0, 0))  # Draw the current image
#         pygame.display.flip()  # Update the display
#         pygame.time.delay(5000)  # Wait for 5 seconds before showing the next image

#     # After all images are shown, return True to indicate the level is completed
#     return True

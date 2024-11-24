# import pygame
# import sys

# from level1 import level1
# from level2 import level2
# from level3 import level3
# from level4 import level4
# from level5 import level5

# pygame.init()

# # Constants
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Main Menu")
# clock = pygame.time.Clock()

# # Colors
# WHITE = (255, 255, 255)

# # Load assets
# menu_background = pygame.image.load("title.png")
# menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
# play_button = pygame.image.load("playbutton.png")
# play_button = pygame.transform.scale(play_button, (200, 80))  # Adjust size if necessary
# play_button_rect = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

# # Draw menu
# def draw_menu():
#     screen.blit(menu_background, (0, 0))
#     screen.blit(play_button, play_button_rect)
#     pygame.display.flip()

# # Main menu loop
# def main_menu():
#     running = True
#     while running:
#         draw_menu()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if play_button_rect.collidepoint(event.pos):  # Check if the play button is clicked
#                     return  # Exit the menu loop and start the game
#         clock.tick(60)

# # Game flow
# def start_game():
#     completed = lv1-denial()  # Start Level 1
#     if completed:
#         completed = lv2-anger()  # Move to Level 2
#     if completed:
#         completed = lv3-bargaining()  # Move to Level 3
#     if completed:
#         completed = lv4-depression()  # Move to Level 4
#     if completed:
#         lv5-acceptance()  # Final level
#     # End game message
#     screen.fill(WHITE)
#     font = pygame.font.SysFont("Arial", 40)
#     end_text = font.render("Congratulations! You Win!", True, (0, 0, 0))
#     screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2))
#     pygame.display.flip()
#     pygame.time.delay(3000)

# # Run the menu and game
# main_menu()
# start_game()

import pygame
import sys

# Importing the levels (assuming they are named level1.py, level2.py, etc.)
from level1 import run_level1
from level2 import run_level2
from level3 import run_level3
from level4 import run_level4
from level5 import run_level5

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)

# Load assets
menu_background = pygame.image.load("title.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
play_button = pygame.image.load("playbutton.png")
play_button = pygame.transform.scale(play_button, (200, 80))  # Adjust size if necessary
play_button_rect = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

# Draw menu
def draw_menu():
    screen.blit(menu_background, (0, 0))
    screen.blit(play_button, play_button_rect)
    pygame.display.flip()

# Main menu loop
def main_menu():
    running = True
    while running:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):  # Check if the play button is clicked
                    return  # Exit the menu loop and start the game
        clock.tick(60)

# Game flow
def start_game():
    # Start Level 1, and move through subsequent levels
    completed = run_level1()  # Start Level 1
    if completed:
        completed = run_level2()  # Move to Level 2
    if completed:
        completed = run_level3()  # Move to Level 3
    if completed:
        completed = run_level4()  # Move to Level 4
    if completed:
        run_level5()  # Final level

    # After completing Level 5, show the "Congratulations!" message and the end screen
    screen.fill(WHITE)
    font = pygame.font.SysFont("Arial", 40)
    end_text = font.render("Congratulations! You Win!", True, (0, 0, 0))
    screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

    # Show the end image
    end_image = pygame.image.load("final.png")
    end_image = pygame.transform.scale(end_image, (WIDTH, HEIGHT))  # Scale to fit screen
    screen.blit(end_image, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

# Run the menu and game
main_menu()
start_game()
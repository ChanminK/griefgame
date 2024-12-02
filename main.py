import pygame
import sys
import importlib 
import time

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HOVER_COLOR = (100, 100, 100)

#FONT
font = pygame.font.SysFont("Arial", 40)

# Assests
menu_background = pygame.image.load("assets/title.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
play_button = pygame.image.load("assets/playbutton.png")
play_button = pygame.transform.scale(play_button, (200, 80))
play_button_rect = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

quit_button = pygame.image.load("assets/quitbutton.png")
quit_button = pygame.transform.scale(quit_button, (200, 80))
quit_button_rect = quit_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))

# Draw menu
def draw_menu(selected_button=None):
    screen.blit(menu_background, (0, 0))
    # play button + hover
    if selected_button == "play":
        pygame.draw.rect(screen, HOVER_COLOR, play_button_rect)
    screen.blit(play_button, play_button_rect)
    
    # quit button + hover
    if selected_button == "quit":
        pygame.draw.rect(screen, HOVER_COLOR, quit_button_rect)
    screen.blit(quit_button, quit_button_rect)
    
    pygame.display.flip()

# if button clicking
def handle_button_click(button_rect):
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        return True
    return False

# Main menu 
def main_menu():
    selected_button = None
    running = True
    while running:
        draw_menu(selected_button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                # Button color changes when mouse on it
                if play_button_rect.collidepoint(event.pos):
                    selected_button = "play"
                elif quit_button_rect.collidepoint(event.pos):
                    selected_button = "quit"
                else:
                    selected_button = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if handle_button_click(play_button_rect):  # Play button clicked
                    return "play"
                if handle_button_click(quit_button_rect):  # Quit button clicked
                    pygame.quit()
                    sys.exit()
        
        clock.tick(60)

# DYNAMICALLY RUNNING THE GAME
def start_game(level_name):
    try:
        # Dynamic loading
        level_module = importlib.import_module(f"levels.level{level_name}")
        completed = level_module.run_level() 
        if completed:
            print(f"Level {level_name} completed. Returning to main menu.")
    except ModuleNotFoundError:
        print(f"Error: Level {level_name} not found.")

# Level Selecting
def level_selector():
    selected_level = None
    level1_rect, level2_rect, level3_rect, level4_rect, level5_rect = draw_level_selection_menu()
    
    while selected_level is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_rect.collidepoint(event.pos):
                    selected_level = '1'
                elif level2_rect.collidepoint(event.pos):
                    selected_level = '2'
                elif level3_rect.collidepoint(event.pos):
                    selected_level = '3'
                elif level4_rect.collidepoint(event.pos):
                    selected_level = '4'
                elif level5_rect.collidepoint(event.pos):
                    selected_level = '5'
        pygame.display.flip()

    return selected_level

def draw_level_selection_menu():
    screen.fill(BLACK)
    font = pygame.font.SysFont("Arial", 40)
    level1_text = font.render("Level 1", True, WHITE)
    level2_text = font.render("Level 2", True, WHITE)
    level3_text = font.render("Level 3", True, WHITE)
    level4_text = font.render("Level 4", True, WHITE)
    level5_text = font.render("Level 5", True, WHITE)

    # Draw level button
    level1_rect = screen.blit(level1_text, (WIDTH // 2 - level1_text.get_width() // 2, HEIGHT // 2 - 100))
    level2_rect = screen.blit(level2_text, (WIDTH // 2 - level2_text.get_width() // 2, HEIGHT // 2 - 50))
    level3_rect = screen.blit(level3_text, (WIDTH // 2 - level3_text.get_width() // 2, HEIGHT // 2))
    level4_rect = screen.blit(level4_text, (WIDTH // 2 - level4_text.get_width() // 2, HEIGHT // 2 + 50))
    level5_rect = screen.blit(level5_text, (WIDTH // 2 - level5_text.get_width() // 2, HEIGHT // 2 + 100))
    
    return level1_rect, level2_rect, level3_rect, level4_rect, level5_rect

# def show_lost_screen():
#     fade_surface = pygame.Surface((WIDTH, HEIGHT))  
#     fade_surface.fill(BLACK)  
#     for i in range(0, 256, 5): 
#         fade_surface.set_alpha(i) 
#         screen.blit(fade_surface, (0, 0))  
#         pygame.display.flip() 
#         pygame.time.delay(50) 
#     message = "YOU ARE TO BLAME. TRY AGAIN"
#     text_surface = font.render(message, True, WHITE)
#     text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#     screen.blit(text_surface, text_rect)
#     pygame.display.flip()
#     pygame.time.delay(5000)  

# Start the game
if __name__ == "__main__":

    while True:
        choice = main_menu()
        if choice == "play":
            while True:
                WIDTH, HEIGHT = 800, 600 
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                level_choice = level_selector()
                result = start_game(level_choice)  
                if result == "completed":
                    print("Returning to level selector.")
        elif choice == "quit":
            pygame.quit()
            sys.exit()

# import pygame
# import sys
# import importlib
# import asyncio

# # Constants
# WIDTH, HEIGHT = 800, 600
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# HOVER_COLOR = (100, 100, 100)
# screen = pygame.display.set_mode((WIDTH, HEIGHT))

# # Initialize Pygame
# pygame.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Main Menu")
# clock = pygame.time.Clock()
# font = pygame.font.SysFont("Arial", 40)

# # Assets
# menu_background = pygame.image.load("assets/title.png")
# menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
# play_button = pygame.image.load("assets/playbutton.png")
# play_button = pygame.transform.scale(play_button, (200, 80))
# play_button_rect = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
# quit_button = pygame.image.load("assets/quitbutton.png")
# quit_button = pygame.transform.scale(quit_button, (200, 80))
# quit_button_rect = quit_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))

# # Draw the menu
# def draw_menu(selected_button=None):
#     screen.blit(menu_background, (0, 0))
#     if selected_button == "play":
#         pygame.draw.rect(screen, HOVER_COLOR, play_button_rect)
#     screen.blit(play_button, play_button_rect)

#     if selected_button == "quit":
#         pygame.draw.rect(screen, HOVER_COLOR, quit_button_rect)
#     screen.blit(quit_button, quit_button_rect)

#     pygame.display.flip()

# # Main menu
# async def main_menu():
#     selected_button = None
#     while True:
#         draw_menu(selected_button)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEMOTION:
#                 if play_button_rect.collidepoint(event.pos):
#                     selected_button = "play"
#                 elif quit_button_rect.collidepoint(event.pos):
#                     selected_button = "quit"
#                 else:
#                     selected_button = None
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if play_button_rect.collidepoint(event.pos):
#                     return "play"
#                 if quit_button_rect.collidepoint(event.pos):
#                     return "quit"
#         await asyncio.sleep(0)  # Yield control to the event loop

# # Level selector
# async def level_selector():
#     selected_level = None
#     level1_rect, level2_rect, level3_rect, level4_rect, level5_rect = draw_level_selection_menu()

#     while selected_level is None:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if level1_rect.collidepoint(event.pos):
#                     selected_level = '1'
#                 elif level2_rect.collidepoint(event.pos):
#                     selected_level = '2'
#                 elif level3_rect.collidepoint(event.pos):
#                     selected_level = '3'
#                 elif level4_rect.collidepoint(event.pos):
#                     selected_level = '4'
#                 elif level5_rect.collidepoint(event.pos):
#                     selected_level = '5'
#         await asyncio.sleep(0)  # Yield control to the event loop

#     return selected_level

# def draw_level_selection_menu():
#     screen.fill(BLACK)
#     level1_text = font.render("Level 1", True, WHITE)
#     level2_text = font.render("Level 2", True, WHITE)
#     level3_text = font.render("Level 3", True, WHITE)
#     level4_text = font.render("Level 4", True, WHITE)
#     level5_text = font.render("Level 5", True, WHITE)

#     level1_rect = screen.blit(level1_text, (WIDTH // 2 - level1_text.get_width() // 2, HEIGHT // 2 - 100))
#     level2_rect = screen.blit(level2_text, (WIDTH // 2 - level2_text.get_width() // 2, HEIGHT // 2 - 50))
#     level3_rect = screen.blit(level3_text, (WIDTH // 2 - level3_text.get_width() // 2, HEIGHT // 2))
#     level4_rect = screen.blit(level4_text, (WIDTH // 2 - level4_text.get_width() // 2, HEIGHT // 2 + 50))
#     level5_rect = screen.blit(level5_text, (WIDTH // 2 - level5_text.get_width() // 2, HEIGHT // 2 + 100))

#     pygame.display.flip()
#     return level1_rect, level2_rect, level3_rect, level4_rect, level5_rect

# async def start_game(level_name):
#     try:
#         level_module = importlib.import_module(f"levels.level{level_name}")
#         completed = await level_module.run_level()  # Assuming run_level is async
#         if completed:
#             print(f"Level {level_name} completed. Returning to menu.")
#     except ModuleNotFoundError:
#         print(f"Error: Level {level_name} not found.")

# # Main game loop
# async def main():
#     while True:
#         choice = await main_menu()
#         if choice == "play":
#             while True:
#                 WIDTH, HEIGHT = 800, 600
#                 screen = pygame.display.set_mode((WIDTH, HEIGHT))
#                 level_choice = await level_selector()
#                 result = await start_game(level_choice)
#                 if result == "completed":
#                     print("Returning to level selector.")
#         elif choice == "quit":
#             pygame.quit()
#             sys.exit()

# # Run the game
# asyncio.run(main())
import pygame
import sys
import importlib 

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

# Load assets
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
    # Draw play button with hover effect
    if selected_button == "play":
        pygame.draw.rect(screen, HOVER_COLOR, play_button_rect)
    screen.blit(play_button, play_button_rect)
    
    # Draw quit button with hover effect
    if selected_button == "quit":
        pygame.draw.rect(screen, HOVER_COLOR, quit_button_rect)
    screen.blit(quit_button, quit_button_rect)
    
    pygame.display.flip()

# Handle button click
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
                # Change button color when hovering
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

# Dynamic game run
def start_game(level_name):
    try:
        level_module = importlib.import_module(f"level{level_name}")
        completed = level_module.run_level()  # ADD `run_level()` FUNCTION TO EACH LEVEL
        if completed:
            print(f"Level {level_name} completed.")
    except ModuleNotFoundError:
        print(f"Error: Level {level_name} not found!")

# Level Select 
def level_selector():
    selected_level = None
    while selected_level is None:
        draw_level_selection_menu()
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

    # Draw level buttons
    level1_rect = screen.blit(level1_text, (WIDTH // 2 - level1_text.get_width() // 2, HEIGHT // 2 - 100))
    level2_rect = screen.blit(level2_text, (WIDTH // 2 - level2_text.get_width() // 2, HEIGHT // 2 - 50))
    level3_rect = screen.blit(level3_text, (WIDTH // 2 - level3_text.get_width() // 2, HEIGHT // 2))
    level4_rect = screen.blit(level4_text, (WIDTH // 2 - level4_text.get_width() // 2, HEIGHT // 2 + 50))
    level5_rect = screen.blit(level5_text, (WIDTH // 2 - level5_text.get_width() // 2, HEIGHT // 2 + 100))

    return level1_rect, level2_rect, level3_rect, level4_rect, level5_rect

# Start the game
if __name__ == "__main__":
    main_menu()
    level_choice = level_selector()  # Get level choice from user
    start_game(level_choice)  # Pass the level choice to start the game
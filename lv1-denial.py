# import pygame

# pygame.init()

# # Constants
# WIDTH, HEIGHT = 800, 600
# CELL_SIZE = 40
# FPS = 60
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# MAZE_COLOR = (41, 0, 162)
# COLLECTIBLE_COLOR = (224, 255, 0)
# DOOR_COLOR = (0, 255, 0)  # Temporary color for the door (Green)

# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Escape Truth")

# # Maze layout with "C" for collectibles and "D" for door
# maze = [
#     "####################",
#     "#P                E#",
#     "# ### ### ###### ###",
#     "# # C           #   #",
#     "# # ### ##  #####   #",
#     "#     #             #",
#     "# ### ### ###### ###",
#     "#    C          #   #",
#     "# # ### #########   #",
#     "#     #     C        #",
#     "# ### ### ###### ###",
#     "# #           #    #",
#     "# # ### ######   ####",
#     "#     #           D  #",
#     "####################",
# ]
# ROWS = len(maze)
# COLS = len(maze[0])

# player_pos = None
# enemy_pos = None
# walls = []
# collectibles = []
# door_pos = None  # Position of the door

# # Initialize positions, walls, collectibles, and the door
# for row_idx, row in enumerate(maze):
#     for col_idx, cell in enumerate(row):
#         x, y = col_idx * CELL_SIZE, row_idx * CELL_SIZE
#         if cell == "#":
#             walls.append(pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))
#         elif cell == "P":
#             player_pos = [x, y]  # Player position
#         elif cell == "E":
#             enemy_pos = [x, y]  # Enemy position
#         elif cell == "C":
#             collectibles.append(pygame.Rect(x, y, 10, 10))  # Collectibles
#         elif cell == "D":
#             door_pos = [x, y]  # Door position

# # Load player image (replace 'player.png' with your actual image path)
# player_image = pygame.image.load('1.png')
# player_image = pygame.transform.scale(player_image, (CELL_SIZE, CELL_SIZE))

# # Load background image (replace 'background.png' with your actual background image path)
# background_image = pygame.image.load('background.png')
# background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# # Font for displaying text
# font = pygame.font.SysFont("Arial", 40)

# def draw_maze():
#     """Draw the maze walls."""
#     for wall in walls:
#         pygame.draw.rect(screen, MAZE_COLOR, wall)

# def draw_player(pos):
#     """Draw the player with the image."""
#     screen.blit(player_image, pos)

# def draw_enemy(pos):
#     """Draw the enemy."""
#     pygame.draw.rect(screen, (255, 0, 0), (*pos, CELL_SIZE, CELL_SIZE))

# def draw_collectibles():
#     """Draw the collectibles."""
#     for collectible in collectibles:
#         pygame.draw.rect(screen, COLLECTIBLE_COLOR, collectible)

# def draw_door():
#     """Draw the door with a temporary color."""
#     pygame.draw.rect(screen, DOOR_COLOR, (*door_pos, CELL_SIZE, CELL_SIZE))

# def display_game_over():
#     """Display 'CAUGHT, YOU LOSE' text on the screen."""
#     game_over_text = font.render("CAUGHT, YOU LOSE", True, WHITE)
#     text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#     screen.blit(game_over_text, text_rect)

# def display_win():
#     """Display 'YOU WIN' text on the screen."""
#     win_text = font.render("YOU WIN!", True, WHITE)
#     text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#     screen.blit(win_text, text_rect)

# def display_score(score):
#     """Display the player's score on the screen."""
#     score_text = font.render(f"Score: {score}", True, WHITE)
#     screen.blit(score_text, (10, 10))

# def can_move_to(x, y):
#     """Check if the new position (x, y) is not colliding with any walls."""
#     new_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
#     for wall in walls:
#         if new_rect.colliderect(wall):
#             return False
#     return True

# # Main game loop
# running = True
# clock = pygame.time.Clock()

# # Movement directions
# player_speed = 10
# enemy_speed = 2
# score = 0

# try:
#     while running:
#         screen.fill(BLACK)  # Clear the screen

#         # Draw background image
#         screen.blit(background_image, (0, 0))

#         # Event Handling
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         # Player Movement (Arrow Keys)
#         keys = pygame.key.get_pressed()
#         move = [0, 0]
#         if keys[pygame.K_UP]:
#             move[1] -= player_speed  # Move up by player_speed
#         if keys[pygame.K_DOWN]:
#             move[1] += player_speed  # Move down by player_speed
#         if keys[pygame.K_LEFT]:
#             move[0] -= player_speed  # Move left by player_speed
#         if keys[pygame.K_RIGHT]:
#             move[0] += player_speed  # Move right by player_speed

#         # Calculate new player position
#         new_player_pos = [player_pos[0] + move[0], player_pos[1] + move[1]]
#         player_rect = pygame.Rect(*new_player_pos, CELL_SIZE, CELL_SIZE)

#         # Check if player can move (no collision with walls)
#         if not any(player_rect.colliderect(wall) for wall in walls):
#             player_pos = new_player_pos

#         # Check for collectible collision
#         for collectible in collectibles[:]:
#             if player_rect.colliderect(collectible):
#                 collectibles.remove(collectible)  # Remove the collectible
#                 score += 1  # Increase score

#         # Check if all collectibles are collected
#         if score == len(collectibles):
#             # Check if the player reaches the door
#             if player_rect.colliderect(pygame.Rect(door_pos[0], door_pos[1], CELL_SIZE, CELL_SIZE)):
#                 display_win()  # Display 'You Win!'
#                 pygame.display.flip()
#                 pygame.time.delay(2000)  # Show the message for 2 seconds
#                 running = False  # End the game

#         # Enemy movement towards player with wall collision checks
#         move_enemy = [0, 0]
#         if enemy_pos[0] < player_pos[0]:
#             move_enemy[0] = enemy_speed
#         elif enemy_pos[0] > player_pos[0]:
#             move_enemy[0] = -enemy_speed

#         if enemy_pos[1] < player_pos[1]:
#             move_enemy[1] = enemy_speed
#         elif enemy_pos[1] > player_pos[1]:
#             move_enemy[1] = -enemy_speed

#         # Check if the enemy can move in the x direction
#         if can_move_to(enemy_pos[0] + move_enemy[0], enemy_pos[1]):
#             enemy_pos[0] += move_enemy[0]

#         # Check if the enemy can move in the y direction
#         if can_move_to(enemy_pos[0], enemy_pos[1] + move_enemy[1]):
#             enemy_pos[1] += move_enemy[1]

#         # Check for game over: if enemy touches player
#         if pygame.Rect(*player_pos, CELL_SIZE, CELL_SIZE).colliderect(
#             pygame.Rect(*enemy_pos, CELL_SIZE, CELL_SIZE)
#         ):
#             display_game_over()  # Display 'You Lose'
#             pygame.display.flip()  # Update the screen
#             pygame.time.delay(2000)  # Show the message for 2 seconds
#             running = False  # End the game

#         # Draw everything
#         draw_maze()
#         draw_player(player_pos)
#         draw_enemy(enemy_pos)
#         draw_collectibles()
#         draw_door()  # Draw the door with the temporary color
#         display_score(score)

#         pygame.display.flip()  # Update the screen
#         clock.tick(FPS)

# except Exception as e:
#     print(f"Error occurred: {e}")
#     pygame.quit()
#     quit()

# pygame.quit()

import pygame

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAZE_COLOR = (41, 0, 162)
COLLECTIBLE_COLOR = (224, 255, 0)
DOOR_COLOR = (0, 255, 0)  # Temporary color for the door (Green)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape Truth")

# Maze layout with "C" for collectibles and "D" for door
maze = [
    "####################",
    "#P                E#",
    "# ### ### ###### ###",
    "# # C           #   #",
    "# # ### ##  #####   #",
    "#     #             #",
    "# ### ### ###### ###",
    "#    C          #   #",
    "# # ### #########   #",
    "#     #     C        #",
    "# ### ### ###### ###",
    "# #           #    #",
    "# # ### ######   ####",
    "#     #           D#",
    "####################",
]
ROWS = len(maze)
COLS = len(maze[0])

player_pos = None
enemy_pos = None
walls = []
collectibles = []
door_pos = None  # Position of the door

# Initialize positions, walls, collectibles, and the door
for row_idx, row in enumerate(maze):
    for col_idx, cell in enumerate(row):
        x, y = col_idx * CELL_SIZE, row_idx * CELL_SIZE
        if cell == "#":
            walls.append(pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))
        elif cell == "P":
            player_pos = [x, y]  # Player position
        elif cell == "E":
            enemy_pos = [x, y]  # Enemy position
        elif cell == "C":
            collectibles.append(pygame.Rect(x, y, 10, 10))  # Collectibles
        elif cell == "D":
            door_pos = [x, y]  # Door position

# Load player image (replace 'player.png' with your actual image path)
player_image = pygame.image.load('1.png')
player_image = pygame.transform.scale(player_image, (CELL_SIZE, CELL_SIZE))

# Load background image (replace 'background.png' with your actual background image path)
background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load door images
door_image = pygame.image.load('door.png')
door_image = pygame.transform.scale(door_image, (CELL_SIZE, CELL_SIZE))
open_door_image = pygame.image.load('open_door.png')
open_door_image = pygame.transform.scale(open_door_image, (CELL_SIZE, CELL_SIZE))

# Load sound effects
pygame.mixer.music.load('background_music.mp3')  # Replace with your background music path
pygame.mixer.music.play(-1, 0.0)  # Loop the background music indefinitely
bling_sound = pygame.mixer.Sound('bling_sound.wav')  # Replace with your bling sound effect

# Font for displaying text
font = pygame.font.SysFont("Arial", 40)

def draw_maze():
    """Draw the maze walls."""
    for wall in walls:
        pygame.draw.rect(screen, MAZE_COLOR, wall)

def draw_player(pos):
    """Draw the player with the image."""
    screen.blit(player_image, pos)

def draw_enemy(pos):
    """Draw the enemy."""
    pygame.draw.rect(screen, (255, 0, 0), (*pos, CELL_SIZE, CELL_SIZE))

def draw_collectibles():
    """Draw the collectibles."""
    for collectible in collectibles:
        pygame.draw.rect(screen, COLLECTIBLE_COLOR, collectible)

def draw_door():
    """Draw the door with a temporary color or open door."""
    if score == len(collectibles):  # If all collectibles are collected
        screen.blit(open_door_image, (door_pos[0], door_pos[1]))
    else:
        screen.blit(door_image, (door_pos[0], door_pos[1]))

def display_game_over():
    """Display 'CAUGHT, YOU LOSE' text on the screen."""
    game_over_text = font.render("CAUGHT, YOU LOSE", True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, text_rect)

def display_win():
    """Display 'YOU WIN' text on the screen."""
    win_text = font.render("YOU WIN!", True, WHITE)
    text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(win_text, text_rect)

def display_score(score):
    """Display the player's score on the screen."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def can_move_to(x, y):
    """Check if the new position (x, y) is not colliding with any walls."""
    new_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    for wall in walls:
        if new_rect.colliderect(wall):
            return False
    return True

# Main game loop
running = True
clock = pygame.time.Clock()

# Movement directions
player_speed = 10
enemy_speed = 2
score = 0

try:
    while running:
        screen.fill(BLACK)  # Clear the screen

        # Draw background image
        screen.blit(background_image, (0, 0))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player Movement (Arrow Keys)
        keys = pygame.key.get_pressed()
        move = [0, 0]
        if keys[pygame.K_UP]:
            move[1] -= player_speed  # Move up by player_speed
        if keys[pygame.K_DOWN]:
            move[1] += player_speed  # Move down by player_speed
        if keys[pygame.K_LEFT]:
            move[0] -= player_speed  # Move left by player_speed
        if keys[pygame.K_RIGHT]:
            move[0] += player_speed  # Move right by player_speed

        # Calculate new player position with some leniency for collisions
        new_player_pos = [player_pos[0] + move[0], player_pos[1] + move[1]]
        player_rect = pygame.Rect(*new_player_pos, CELL_SIZE, CELL_SIZE)

        # Check if player can move (less strict collision)
        if not any(player_rect.colliderect(wall) for wall in walls):
            player_pos = new_player_pos

        # Check for collectible collision
        for collectible in collectibles[:]:
            if player_rect.colliderect(collectible):
                collectibles.remove(collectible)  # Remove the collectible
                score += 1  # Increase score
                bling_sound.play()  # Play bling sound

        # Check if all collectibles are collected
        if score == len(collectibles):
            # Check if the player reaches the door
            if player_rect.colliderect(pygame.Rect(door_pos[0], door_pos[1], CELL_SIZE, CELL_SIZE)):
                display_win()  # Display 'You Win!'
                pygame.display.flip()
                pygame.time.delay(2000)  # Show the message for 2 seconds
                running = False  # End the game

        # Enemy movement towards player with wall collision checks
        move_enemy = [0, 0]
        if enemy_pos[0] < player_pos[0]:
            move_enemy[0] = enemy_speed
        elif enemy_pos[0] > player_pos[0]:
            move_enemy[0] = -enemy_speed

        if enemy_pos[1] < player_pos[1]:
            move_enemy[1] = enemy_speed
        elif enemy_pos[1] > player_pos[1]:
            move_enemy[1] = -enemy_speed

        # Check if the enemy can move in the x direction
        if can_move_to(enemy_pos[0] + move_enemy[0], enemy_pos[1]): enemy_pos[0] += move_enemy[0]
        
         # Check if the enemy can move in the y direction
        if can_move_to(enemy_pos[0], enemy_pos[1] + move_enemy[1]):
            enemy_pos[1] += move_enemy[1]

        # Check for game over: if enemy touches player
        if pygame.Rect(*player_pos, CELL_SIZE, CELL_SIZE).colliderect(
            pygame.Rect(*enemy_pos, CELL_SIZE, CELL_SIZE)
        ):
            display_game_over()  # Display 'You Lose'
            pygame.display.flip()  # Update the screen
            pygame.time.delay(2000)  # Show the message for 2 seconds
            running = False  # End the game

        # Draw everything
        draw_maze()
        draw_player(player_pos)
        draw_enemy(enemy_pos)
        draw_collectibles()
        draw_door()  # Draw the door with the temporary color
        display_score(score)

        pygame.display.flip()  # Update the screen
        clock.tick(FPS)

except Exception as e:
    print(f"Error occurred: {e}")
    pygame.quit()
    quit()

pygame.quit()
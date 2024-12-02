import pygame
import sys

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAZE_COLOR = (41, 0, 162)
COLLECTIBLE_COLOR = (224, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape Truth")

#Maze Layout
# EVENTUALLY MAKE IT GENERATE ITS OWN
# # = Wall
# P = Player
# E = Enemy
# C = Coin
# D = Door
maze = [
    "####################",
    "# P              E #",
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
    "#    #          D  #",
    "####################",
]
ROWS = len(maze)
COLS = len(maze[0])

player_pos = None
enemy_pos = None
walls = []
collectibles = []

# Load pics
player_image = pygame.image.load('assets/player.png')
player_image = pygame.transform.scale(player_image, (CELL_SIZE, CELL_SIZE))
eye_image = pygame.image.load('assets/eye.png')  
eye_image = pygame.transform.scale(eye_image, (CELL_SIZE, CELL_SIZE))
background_image = pygame.image.load('assets/background.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
door_image = pygame.image.load('assets/door.png')
door_image = pygame.transform.scale(door_image, (CELL_SIZE, CELL_SIZE))
open_door_image = pygame.image.load('assets/open_door.png')
open_door_image = pygame.transform.scale(open_door_image, (CELL_SIZE, CELL_SIZE))
chest_image = pygame.image.load('assets/chest1.png')
chest_image = pygame.transform.scale(chest_image, (WIDTH, HEIGHT))

# Load sfx
pygame.mixer.music.load('assets/background_music.mp3')  
pygame.mixer.music.play(-1, 0.0)  # Loop the background music
bling_sound = pygame.mixer.Sound('assets/bling_sound.wav')  
win_sound = pygame.mixer.Sound('assets/win.mp3')  

# Text Font
font = pygame.font.SysFont("Arial", 40)

# Helper stuff
def draw_maze():
    for wall in walls:
        pygame.draw.rect(screen, MAZE_COLOR, wall)

def get_initial_positions(maze):
    global walls
    global door_pos
    walls.clear

    player_start = None
    enemy_start = None
    door_pos = None
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            x, y = col_idx * CELL_SIZE, row_idx * CELL_SIZE
            if cell == "P":
                player_start = [x, y]
            elif cell == "E":
                enemy_start = [x, y]
            elif cell == "C":
                collectibles.append(pygame.Rect(x, y, 10, 10))  
            elif cell == "D":
                door_pos = [x, y] 
            elif cell == "#":
                walls.append(pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))
    return player_start, enemy_start, collectibles, door_pos, walls

def draw_player(pos):
    screen.blit(player_image, pos)

def draw_enemy(pos):
    screen.blit(eye_image, pos)  

def draw_collectibles():
    for collectible in collectibles:
        pygame.draw.rect(screen, COLLECTIBLE_COLOR, collectible)

def draw_door(door_open):
    if door_open == True:
        image = open_door_image
    else:
        image = door_image
    screen.blit(image, (door_pos[0], door_pos[1]))

def display_text(text):
    render_text = font.render(text, True, WHITE)
    text_rect = render_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(render_text, text_rect)

def show_lost_screen():
    fade_surface = pygame.Surface((WIDTH, HEIGHT))  
    fade_surface.fill(BLACK)  
    for i in range(0, 256, 5): 
        fade_surface.set_alpha(i) 
        screen.blit(fade_surface, (0, 0))  
        pygame.display.flip() 
        pygame.time.delay(50) 
    message = "YOU ARE TO BLAME. TRY AGAIN"
    text_surface = font.render(message, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(5000)
    pygame.quit()
    sys.exit()  

# MAIN LEVEL RUNNING
def run_level():
    door_open = False
    score = 0
    running = True
    clock = pygame.time.Clock()
    
    player_pos, enemy_pos, collectibles, door_pos, walls = get_initial_positions(maze)

    while running:
        screen.fill(BLACK)  # Clear screen
        screen.blit(background_image, (0, 0))  # Draw background

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movement
        keys = pygame.key.get_pressed()
        move = [0, 0]
        if keys[pygame.K_UP]:
            move[1] -= 10
        if keys[pygame.K_DOWN]:
            move[1] += 10
        if keys[pygame.K_LEFT]:
            move[0] -= 10
        if keys[pygame.K_RIGHT]:
            move[0] += 10

        new_player_pos = [player_pos[0] + move[0], player_pos[1] + move[1]]
        player_rect = pygame.Rect(*new_player_pos, CELL_SIZE, CELL_SIZE)

        # Prevent player from walking through walls
        if not any(player_rect.colliderect(wall) for wall in walls):
            player_pos = new_player_pos

        # Collectible collision
        for collectible in collectibles[:]:
            if player_rect.colliderect(collectible):
                collectibles.remove(collectible)
                score += 1
                bling_sound.play()

        # Check if all collectibles are collected
        if len(collectibles) == 0 and not door_open:
            door_open = True
            win_sound.play()

        # Player reaching the door
        door_rect = pygame.Rect(door_pos[0], door_pos[1], CELL_SIZE, CELL_SIZE)
        if player_rect.colliderect(door_rect) and door_open:
            screen.blit(chest_image, (0, 0))  # Show chest image
            pygame.mixer.Sound.play(win_sound)  # Play win sound
            display_text("TRUTH DEFEATED")
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
            return "completed"

        # Enemy movement logic (follows player)
        move_enemy = [0, 0]
        if enemy_pos[0] < player_pos[0]:
            move_enemy[0] = 2
        elif enemy_pos[0] > player_pos[0]:
            move_enemy[0] = -2
        if enemy_pos[1] < player_pos[1]:
            move_enemy[1] = 2
        elif enemy_pos[1] > player_pos[1]:
            move_enemy[1] = -2

        #Lose scenario
        enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], CELL_SIZE, CELL_SIZE)
        if player_rect.colliderect(enemy_rect):
            show_lost_screen()

        enemy_rect = pygame.Rect(enemy_pos[0] + move_enemy[0], enemy_pos[1], CELL_SIZE, CELL_SIZE)
        if not any(enemy_rect.colliderect(wall) for wall in walls):
            enemy_pos[0] += move_enemy[0]

        enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1] + move_enemy[1], CELL_SIZE, CELL_SIZE)
        if not any(enemy_rect.colliderect(wall) for wall in walls):
            enemy_pos[1] += move_enemy[1]

        # Drawing
        draw_maze()
        draw_player(player_pos)
        draw_enemy(enemy_pos)
        draw_collectibles()
        draw_door(door_open)

        pygame.display.flip()
        clock.tick(FPS)

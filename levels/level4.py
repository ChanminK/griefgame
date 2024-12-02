import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLUE = (135, 206, 250)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonts
font = pygame.font.Font(None, 36)

# Load assets
player_image = pygame.image.load("assets/player.png")
player_image = pygame.transform.scale(player_image, (40, 40))

win_image = pygame.image.load("assets/chest4.png")
win_image = pygame.transform.scale(win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.mixer.init()
win_sound = pygame.mixer.Sound("assets/win.mp3")

# Functions
def draw_text(text, x, y, color=BLACK):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def spawn_platform(platforms, platform_width, platform_height):
    """Spawns a new platform at a random height."""
    y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 50)
    platform = pygame.Rect(SCREEN_WIDTH, y, platform_width, platform_height)
    platforms.append(platform)

def run_level():
    # Initialize screen and clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platform Jumper")
    clock = pygame.time.Clock()

    # Player settings
    player_width = 40
    player_height = 40
    player_x = 100
    player_y = SCREEN_HEIGHT - 150
    player_velocity_y = 0
    gravity = 0.8
    jump_force = -15
    is_jumping = False

    # Platform settings
    platform_width = 100
    platform_height = 20
    platforms = []
    platform_speed = 5
    spawn_timer = 0
    spawn_interval = 1500  # milliseconds

    # Scoring
    score = 0
    max_score = 15  # Win condition

    # Difficulty scaling
    difficulty_timer = 0
    difficulty_interval = 5000  # milliseconds
    speed_increase = 0.5

    # Parallax Background
    background_scroll = 0
    background_speed = 2

    # Game state
    game_won = False

    while True:
        screen.fill(BLUE)  # Background color

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        if not game_won:
            # Player Input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not is_jumping:
                player_velocity_y = jump_force
                is_jumping = True

            # Update Player
            player_velocity_y += gravity
            player_y += player_velocity_y

            # Prevent player from falling off the screen
            if player_y > SCREEN_HEIGHT:
                return "failed"  # Game Over

            # Prevent player from jumping indefinitely
            if player_y + player_height >= SCREEN_HEIGHT - 100:
                player_y = SCREEN_HEIGHT - 100 - player_height
                is_jumping = False

            # Update Platforms
            for platform in platforms[:]:
                platform.x -= platform_speed
                if platform.x + platform.width < 0:  # Remove off-screen platforms
                    platforms.remove(platform)
                    score += 1

                # Player collision with platform
                if (
                    player_x + player_width > platform.x
                    and player_x < platform.x + platform.width
                    and player_y + player_height >= platform.y
                    and player_y + player_height <= platform.y + platform.height
                ):
                    player_y = platform.y - player_height
                    player_velocity_y = 0
                    is_jumping = False

            # Spawn new platforms
            spawn_timer += clock.get_time()
            if spawn_timer > spawn_interval:
                spawn_timer = 0
                spawn_platform(platforms, platform_width, platform_height)

            # Difficulty scaling
            difficulty_timer += clock.get_time()
            if difficulty_timer > difficulty_interval:
                difficulty_timer = 0
                platform_speed += speed_increase

            # Check for win condition
            if score >= max_score:
                game_won = True
                pygame.mixer.Sound.play(win_sound)

        else:
            # Winning Screen
            screen.blit(win_image, (0, 0))
            draw_text("Depression Defeated!", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20, BLACK)

        # Background Parallax
        background_scroll -= background_speed
        if background_scroll <= -SCREEN_WIDTH:
            background_scroll = 0
        pygame.draw.rect(screen, GREEN, (background_scroll, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        pygame.draw.rect(screen, GREEN, (background_scroll + SCREEN_WIDTH, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

        # Draw Player
        if not game_won:
            player = pygame.Rect(player_x, player_y, player_width, player_height)
            screen.blit(player_image, (player_x, player_y))

        # Draw Platforms
        for platform in platforms:
            pygame.draw.rect(screen, BLACK, platform)

        # Draw Score
        if not game_won:
            draw_text(f"Score: {score}", 10, 10)

        # Update Screen
        pygame.display.flip()
        clock.tick(FPS)

    return "completed" if game_won else "failed"

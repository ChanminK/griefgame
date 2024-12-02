import pygame
import sys
import random

#Initialize
WIDTH = 800
HEIGHT = 400
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont("Arial", 40)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Griever v Anger")

# Load assets
win_sound_path = "assets/win.mp3"
chest_image_path = "assets/chest2.png"
pygame.mixer.init()
win_sound = pygame.mixer.Sound(win_sound_path)
chest_image = pygame.image.load(chest_image_path)
chest_image = pygame.transform.scale(chest_image, (WIDTH, HEIGHT))

# Fighter class
class Fighter:
    def __init__(self, x, y, image_path, speed, damage):
        self.x = x
        self.y = y
        original_image = pygame.image.load(image_path)
        original_width, original_height = original_image.get_size()
        scale_factor = 0.5
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.width, self.height = self.image.get_size()
        self.health = 100
        self.speed = speed
        self.attack = False
        self.damage = damage

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        pygame.draw.rect(screen, RED, (self.x, self.y - 20, 100, 10))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 20, self.health, 10))

    def move(self, keys=None, controls=None):
        if keys and controls:
            if keys[controls['left']]:
                self.x -= self.speed
            if keys[controls['right']]:
                self.x += self.speed
            if keys[controls['up']]:
                self.y -= self.speed
            if keys[controls['down']]:
                self.y += self.speed

        self.x = max(0, min(self.x, WIDTH - self.width))
        self.y = max(0, min(self.y, HEIGHT - self.height))

    def ai_move(self, target, delay_counter):
        if delay_counter % 30 == 0:
            if self.x < target.x:
                self.x += self.speed
            elif self.x > target.x:
                self.x -= self.speed
            if self.y < target.y:
                self.y += self.speed
            elif self.y > target.y:
                self.y -= self.speed

        self.x = max(0, min(self.x, WIDTH - self.width))
        self.y = max(0, min(self.y, HEIGHT - self.height))

    def attack_enemy(self, enemy):
        if self.attack:
            if pygame.Rect(self.x, self.y, self.width, self.height).colliderect(
                pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            ):
                enemy.health -= self.damage


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

def run_level():
    player = Fighter(100, 300, "assets/2.png", speed=6, damage=5)
    enemy = Fighter(600, 300, "assets/eye.png", speed=4, damage=2)
    delay_counter = 5
    running = True

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        keys = pygame.key.get_pressed()
        player.move(keys, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s})
        player.attack = keys[pygame.K_SPACE]
        enemy.ai_move(player, delay_counter)
        enemy.attack = random.choice([True, False])
        player.attack_enemy(enemy)
        enemy.attack_enemy(player)
        player.draw()
        enemy.draw()

        if player.health <= 0:
            show_lost_screen()
            pygame.quit()
            sys.exit() 
        if enemy.health <= 0:
            pygame.mixer.Sound.play(win_sound)
            screen.blit(chest_image, (0, 0))
            text = font.render(f"Anger Defeated", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            return "completed"

        pygame.display.flip()
        clock.tick(FPS)
        delay_counter += 1

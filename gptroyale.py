import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Epic Battle Royale")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Load assets
gun_image = pygame.Surface((10, 10))  # Placeholder gun sprite
pygame.draw.circle(gun_image, RED, (5, 5), 5)

# Load sound file
try:
    explosion_sound = pygame.mixer.Sound("./shot.wav")
except pygame.error as e:
    print(f"Error loading sound: {e}")
    explosion_sound = None

# Function to play explosion sound
def explosion_sound_play():
    if explosion_sound:
        explosion_sound.play()

# Player class with directional shooting!
class Player(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((40, 40))
        self.image.fill(random.choice([RED, GREEN, BLUE, YELLOW]))
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 100
        self.speed = 5
        self.bullets = pygame.sprite.Group()
        self.last_shot_time = 0
        self.direction = pygame.math.Vector2(0, -1)  # Default to "up"

    def move(self, keys, left, right, up, down):
        if keys[left]:
            self.rect.x -= self.speed
            self.direction = pygame.math.Vector2(-1, 0)  # Left
        if keys[right]:
            self.rect.x += self.speed
            self.direction = pygame.math.Vector2(1, 0)  # Right
        if keys[up]:
            self.rect.y -= self.speed
            self.direction = pygame.math.Vector2(0, -1)  # Up
        if keys[down]:
            self.rect.y += self.speed
            self.direction = pygame.math.Vector2(0, 1)  # Down

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > 500:  # Shoot cooldown
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            self.bullets.add(bullet)
            explosion_sound_play()
            self.last_shot_time = now

# Bullet class with directional movement
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.transform.scale(gun_image, (10, 10))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.direction = direction

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

# Draw health bar
def draw_health_bar(player, x, y):
    pygame.draw.rect(screen, RED, (x, y, 100, 10))
    pygame.draw.rect(screen, GREEN, (x, y, player.health, 10))

# Game loop
def battle_royale_game():
    clock = pygame.time.Clock()
    running = True

    # Create players
    player1 = Player("Player 1", 100, HEIGHT - 100)
    player2 = Player("Player 2", WIDTH - 100, HEIGHT - 100)

    players = pygame.sprite.Group(player1, player2)

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
        player2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

        if keys[pygame.K_SPACE]:
            player1.shoot()
        if keys[pygame.K_RETURN]:
            player2.shoot()

        # Update bullets and detect collisions
        player1.bullets.update()
        player2.bullets.update()

        for bullet in player1.bullets:
            if player2.rect.colliderect(bullet.rect):
                player2.health -= 20
                bullet.kill()

        for bullet in player2.bullets:
            if player1.rect.colliderect(bullet.rect):
                player1.health -= 20
                bullet.kill()

        # Draw players, bullets, and health bars
        players.draw(screen)
        player1.bullets.draw(screen)
        player2.bullets.draw(screen)
        draw_health_bar(player1, player1.rect.x, player1.rect.y - 20)
        draw_health_bar(player2, player2.rect.x, player2.rect.y - 20)

        # Check for game over
        if player1.health <= 0 or player2.health <= 0:
            winner = player1.name if player1.health > 0 else player2.name
            screen.fill(WHITE)
            winner_text = font.render(f"{winner} wins!", True, BLACK)
            screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    battle_royale_game()
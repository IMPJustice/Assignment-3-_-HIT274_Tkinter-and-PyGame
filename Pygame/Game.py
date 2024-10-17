import pygame
import random
pygame.init()
# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scrolling Game with Dragon Boss")
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (165, 42, 42)  # Animal color
YELLOW = (255, 255, 0)  # Bullet color
PURPLE = (128, 0, 128)  # Boss color
ORANGE = (255, 165, 0)  # Health boost color
# Clock for controlling FPS
clock = pygame.time.Clock()
# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(midbottom=(100, HEIGHT - 100))
        self.speed = 5
        self.jump_speed = 15
        self.gravity = 0.8
        self.vel_y = 0
        self.health = 100
        self.lives = 3
        self.is_jumping = False
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # Jumping mechanics (UP arrow for jump)
        if keys[pygame.K_UP] and not self.is_jumping:
            self.is_jumping = True
            self.vel_y = -self.jump_speed
        # Apply gravity
        if self.is_jumping:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
            if self.rect.bottom >= HEIGHT - 50:
                self.rect.bottom = HEIGHT - 50
                self.is_jumping = False
                self.vel_y = 0
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.lives -= 1
            self.health = 100  # Reset health when losing a life
            if self.lives <= 0:
                return False  # Indicates game over
        return True
    def shoot(self, projectiles):
        projectile = Projectile(self.rect.centerx + 10, self.rect.top)  # Adjusted position to start slightly ahead
        projectiles.add(projectile)
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 50, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, 50 * (self.health / 100), 5))
    def gain_health(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100  # Cap health at 100
# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 12
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()  # Remove the projectile if it goes off-screen
# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = speed
        self.health = 50
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.kill()
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 40, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, 40 * (self.health / 50), 5))
# Dragon Boss class
class DragonBoss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((120, 80))  # Size of the dragon boss
        self.image.fill(PURPLE)  # Boss color
        # Adding some wings for a dragon effect
        pygame.draw.polygon(self.image, GREEN, [(60, 0), (90, 20), (30, 20)])  # Left wing
        pygame.draw.polygon(self.image, GREEN, [(60, 0), (90, 20), (60, 20)])  # Right wing
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 2  # Speed for boss
        self.health = 200
    def update(self, player):
        # Move towards the player
        if self.rect.centerx < player.rect.centerx:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        # Boss attacks player
        if self.rect.colliderect(player.rect):
            player.take_damage(1)  # Damage to player when colliding
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Remove the dragon boss if health is zero
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 120, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, 120 * (self.health / 200), 5))
# Health Boost class
class HealthBoost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Size of the health boost
        self.image.fill(ORANGE)  # Color for health boost
        self.rect = self.image.get_rect(center=(x, y))
    def update(self):
        # Health boosts don't move; they are static
        pass
# Main game function
def main():
    # Sprite groups
    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    health_boosts = pygame.sprite.Group()
    # Player setup
    player = Player()
    all_sprites.add(player)
    # Game variables
    level = 1
    enemies_to_spawn = 10  # Number of enemies to defeat to move to the next level
    defeated_enemies = 0  # Count of defeated enemies
    boss_fight = False
    boss = None
    enemy_spawn_timer = 0  # Timer to control enemy spawning
    enemy_spawn_delay = 1500  # Delay between enemy spawns in milliseconds
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot(projectiles)  # Shoot on SPACE key press
        keys = pygame.key.get_pressed()
        player.update(keys)
        # Timer for spawning enemies
        enemy_spawn_timer += clock.get_time()
        # Update projectiles, enemies, health boosts
        projectiles.update()
        enemies.update()
        health_boosts.update()
        # Spawn enemies based on the current level and timer
        if not boss_fight and enemy_spawn_timer >= enemy_spawn_delay:
            enemy = Enemy(WIDTH, HEIGHT - 100, random.randint(1, 2))  # Reduced speed for enemies
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemy_spawn_timer = 0  # Reset timer for the next enemy spawn
        # Check for projectiles hitting enemies
        for projectile in projectiles:
            hit_enemies = pygame.sprite.spritecollide(projectile, enemies, False)
            for enemy in hit_enemies:
                enemy.take_damage(20)
                defeated_enemies += 1  # Count this enemy as defeated
                projectile.kill()  # Remove projectile after hitting an enemy
                # Chance to spawn a health boost after defeating an enemy
                if random.random() < 0.3:  # 30% chance to spawn a health boost
                    health_boost = HealthBoost(enemy.rect.centerx, enemy.rect.centery)
                    all_sprites.add(health_boost)
                    health_boosts.add(health_boost)
        # Check for player collisions with health boosts
        if pygame.sprite.spritecollide(player, health_boosts, True):
            player.gain_health(20)  # Heal player by 20 health
        # Check for player collisions with enemies
        if pygame.sprite.spritecollide(player, enemies, False):
            if not player.take_damage(5):
                running = False  # End game when the player is out of lives
        # Check for boss appearance after defeating enemies
        if defeated_enemies >= enemies_to_spawn:
            if level == 2:  # Boss fight at level 2
                boss_fight = True
                boss = DragonBoss(WIDTH // 2, HEIGHT - 100)  # Use the DragonBoss class
                all_sprites.add(boss)
            else:  # Move to the next level after defeating the enemies
                level += 1
                defeated_enemies = 0  # Reset defeated enemies count
                enemies_to_spawn += 10  # Increase difficulty for next level
        # Boss fight logic
        if boss_fight and boss:
            boss.update(player)  # Update boss position towards player
            if pygame.sprite.spritecollide(boss, projectiles, True):
                boss.take_damage(10)  # Boss takes damage
        # Drawing
        screen.fill(WHITE)
        all_sprites.draw(screen)
        for sprite in all_sprites:
            if hasattr(sprite, 'draw'):
                sprite.draw(screen)
        # Display player's health, lives, and current level
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {player.health}", True, BLACK)
        lives_text = font.render(f"Lives: {player.lives}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(health_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(level_text, (10, 90))
        # Check if the game is over
        if player.lives <= 0:
            running = False  # End game if player is out of lives
        pygame.display.flip()
        clock.tick(60)
    # Game Over Screen
    game_over_screen()
def game_over_screen():
    """Display the game over screen and restart option."""
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, BLACK)
    restart_font = pygame.font.Font(None, 36)
    restart_text = restart_font.render("Press R to Restart or Q to Quit", True, BLACK)
    while True:
        screen.fill(WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    main()
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    return
        pygame.display.flip()
if __name__ == "__main__":
    main()

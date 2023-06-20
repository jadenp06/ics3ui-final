import pygame
import sys
import random
from pygame.sprite import Group
from pygame.locals import *

# Initialize pygame
pygame.font.init()
screen_width, screen_height = 1200, 1200
pygame.display.set_caption("Stalingrad: 1943")
font = pygame.font.Font(None, 50)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./images/yak.png")  # Load player plane image
        self.rect = self.image.get_rect(center=(screen_width / 2, screen_height / 2))  # Start in the middle of the canvas
        self.kills = 0  # Number of enemies killed by the player
        self.points = 0  # Player's score
        self.health = 5  # Player's health

    def update(self):
        self.rect.center = pygame.mouse.get_pos()  # Update player position based on the cursor

    def create_bullet(self):
        return Bullet(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])  # Create a bullet at the cursor position

class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.image.load("./images/bf109.png")  # Load enemy plane image
        self.rect = self.image.get_rect(center=(random.randrange(200, 1000), random.randrange(-1200, -100)))  # Randomly position the enemy off-screen
        self.level = level  # Enemy level determines its strength
        self.bullet_cooldown = random.randint(100, 200)  # Cooldown for shooting bullets
        self.health = 2  # Enemy health

    def update(self):
        self.rect.y += 4  # Move the enemy downwards

        if len(enemy_group) < self.level:
            spawn_enemies(self.level - len(enemy_group))  # Spawn more enemies if there are fewer than the level requirement

        if self.rect.y >= 1300:
            self.kill()  # Destroy the enemy when it goes off-screen

        self.bullet_cooldown -= 1  # Decrease the bullet shooting cooldown

        if self.rect.y >= 0 and self.bullet_cooldown <= 0:  # Only shoot bullets when the enemy is on the screen and the cooldown is reached
            self.create_bullet()
            self.bullet_cooldown = random.randint(60, 120)  # Reset the cooldown to a higher value

    def create_bullet(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.centery)  # Create an enemy bullet at the enemy's position
        enemy_bullet_group.add(bullet)

class Boss(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.image = pygame.image.load("./images/me262.png")  # Load boss plane image
        self.rect = self.image.get_rect(center=(random.randrange(200, 1000), random.randrange(-1500, -600)))  # Randomly position the boss off-screen
        self.level = level  # Boss level determines its strength
        self.bullet_cooldown = random.randint(10, 60)  # Cooldown for shooting bullets
        self.health = 5  # Boss health

    def update(self):
        self.rect.y += 10  # Move the boss downwards

        if len(enemy_group) < self.level:
            spawn_enemies(self.level - len(enemy_group))  # Spawn more enemies if there are fewer than the level requirement

        if self.rect.y >= 1300:
            self.kill()  # Destroy the boss when it goes off-screen

        self.bullet_cooldown -= 1  # Decrease the bullet shooting cooldown

        if self.rect.y >= 0 and self.bullet_cooldown <= 0:  
            self.create_bullet()
            self.bullet_cooldown = random.randint(10,60)  # Reset the cooldown to a smaller value

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, is_enemy_bullet=False):
        super().__init__()
        self.image = pygame.Surface((2, 20))  # Create a bullet surface
        self.image.fill((255, 0, 0))  # Set color to red for player bullets
        self.rect = self.image.get_rect(center=(pos_x, pos_y))  # Position the bullet at the specified coordinates
        self.is_enemy_bullet = is_enemy_bullet  # Flag to indicate if the bullet is an enemy bullet

    def update(self):
        self.rect.y -= 35  # Move the bullet upwards

        if self.rect.y <= -100:
            self.kill()  # Destroy the bullet when it goes off-screen

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((4, 30))  # Create an enemy bullet surface
        self.image.fill((0, 255, 0))  # Set color to green for enemy bullets
        self.rect = self.image.get_rect(center=(pos_x, pos_y))  # Position the enemy bullet at the specified coordinates

    def update(self):
        self.rect.y += 15  # Move the enemy bullet downwards

        if self.rect.y >= 1300:
            self.kill()  # Destroy the enemy bullet when it goes off-screen

class Background(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = pygame.image.load("./images/snow.jpg")  # Load background image
        self.rect = self.image.get_rect(center=(screen_width / 2, y))  # Position the background

    def update(self):
        self.rect.y += 3  # Move the background downwards

        if self.rect.top >= screen_height:
            self.rect.y = -self.rect.height  # Reset the background position when it goes off-screen

def spawn_enemies(num_enemies):
    for i in range(num_enemies):
        new_enemy = Enemy(3)  # Create a new enemy
        enemy_group.add(new_enemy)

def spawn_boss(num_boss):
    for i in range(num_boss):
        new_boss = Boss(1)  # Create a new bosse enemy
        boss_group.add(new_boss)

def render_score(score):
    text = font.render("Score: " + str(score), True, (0, 0, 0))  # Render the score as text
    return text  # Return the rendered score text

def start_menu():
    start_image = pygame.image.load("./images/stalingrad.jpg")  # Load the start menu background image
    start_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 100)  # Define the start button position and size
    start_font = pygame.font.Font(None, 40)  # Set font and size for the start button text
    game_name_font = pygame.font.Font(None, 120)  # Set font and size for the game name text

    pygame.mouse.set_visible(True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return  # Exit the start menu and start the game

        screen.blit(start_image, (0, 0))  # Draw the start menu background image

        game_name_text = game_name_font.render("STALINGRAD: 1943", True, (255, 0, 0))  # Render the game name text
        game_name_rect = game_name_text.get_rect(center=(screen_width // 2, screen_height // 3))  # Position the game name text at the top of the screen
        screen.blit(game_name_text, game_name_rect)  # Draw the game name text

        pygame.draw.rect(screen, (200, 200, 200), start_button)  # Draw the start button rectangle
        start_text = start_font.render("START GAME", True, (0, 0, 0))  # Render the start button text
        text_rect = start_text.get_rect(center=start_button.center)  # Position the start button text at the center of the button
        screen.blit(start_text, text_rect)  # Draw the start button text

        pygame.display.update()
        clock.tick(60)

def game_over(score):
    game_over_image = pygame.image.load("./images/stalingrad.jpg")  # Load the game over background image
    game_over_font = pygame.font.Font(None, 60)  # Set font and size for the game over text
    score_font = pygame.font.Font(None, 50)  # Set font and size for the score text

    restart_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 50)  # Define the restart button position and size
    leave_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 200, 200, 50)  # Define the leave button position and size

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return "restart"  # Return "restart" if the restart button is clicked
                elif leave_button.collidepoint(event.pos):
                    return "leave"  # Return "leave" if the leave button is clicked

        screen.blit(game_over_image, (0, 0))  # Draw the game over background image

        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))  # Render the game over text
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))  # Position the game over text at the center of the screen
        screen.blit(game_over_text, game_over_rect)  # Draw the game over text

        score_text = score_font.render("Score: " + str(score), True, (0, 0, 0))  # Render the score text
        score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))  # Position the score text below the game over text
        screen.blit(score_text, score_rect)  # Draw the score text

        pygame.draw.rect(screen, (0, 255, 0), restart_button)  # Draw the restart button rectangle
        restart_text = score_font.render("Restart", True, (0, 0, 0))  # Render the restart button text
        restart_rect = restart_text.get_rect(center=restart_button.center)  # Position the restart button text at the center of the button
        screen.blit(restart_text, restart_rect)  # Draw the restart button text

        pygame.draw.rect(screen, (255, 0, 0), leave_button)  # Draw the leave button rectangle
        leave_text = score_font.render("Leave", True, (255, 255, 255))  # Render the leave button text
        leave_rect = leave_text.get_rect(center=leave_button.center)  # Position the leave button text at the center of the button
        screen.blit(leave_text, leave_rect)  # Draw the leave button text

        pygame.display.update()
        clock.tick(60)

def health_bar(surface, x, y, health, max_health):
    bar_width = 200
    bar_height = 20
    health_ratio = health / max_health
    bar_fill = bar_width * health_ratio
    bar_outline = pygame.Rect(x, y, bar_width, bar_height)
    bar_fill_rect = pygame.Rect(x, y, bar_fill, bar_height)
    pygame.draw.rect(surface, (255, 0, 0), bar_fill_rect)  # Fill the health bar with red
    pygame.draw.rect(surface, (0, 0, 0), bar_outline, 5)  # Draw an outline around the health bar

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.mouse.set_visible(False)

# Create the player and groups
enemy_bullet_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

player = Player()
enemy = Enemy(5)
boss = Boss(1)

player_group.add(player)
enemy_group.add(enemy)
boss_group.add(boss)

# Create the backgrounds
backgrounds = pygame.sprite.Group()
backgrounds.add(Background(0))
backgrounds.add(Background(-screen_height))

start_menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet_group.add(player.create_bullet())

    screen.fill((30, 30, 30))
    
    backgrounds.update()
    bullet_group.update()
    player_group.update()
    enemy_bullet_group.update()
    enemy_group.update()
    boss_group.update()
    
    for background in backgrounds:
        screen.blit(background.image, background.rect)

    bullet_group.draw(screen)
    player_group.draw(screen)
    enemy_bullet_group.draw(screen)
    enemy_group.draw(screen)
    boss_group.draw(screen)

    enemy_hit = pygame.sprite.groupcollide(bullet_group, enemy_group, True, False)
    for bullet in enemy_hit:
        for enemy in enemy_hit[bullet]:
            enemy.health -= 1
            if enemy.health <= 0:
                enemy.kill()
                player.kills += 1  # Increment the player's kills
                player.points += 10
                new_enemy = Enemy(player.kills // 10 + 1)  # Create a new enemy with a level based on the player's kills

    boss_hit = pygame.sprite.groupcollide(bullet_group, boss_group, True, False)
    for bullet in boss_hit:
        for boss in boss_hit[bullet]:
            boss.health -= 1
            if boss.health <= 0:
                boss.kill()
                player.kills += 1  # Increment the player's kills
                player.points += 50
                new_boss = Boss(player.kills // 5 + 1)  # Create a new boss with a level based on the player's kills
    
    player_hit = pygame.sprite.spritecollide(player, enemy_bullet_group, True)
    if player_hit:
        player.health -= 1
        if player.health <= 0:
            result = game_over(player.points)  # Call the game over function and pass the player's score
            if result == "restart":
                # Reset the game and start a new game loop
                # Reset player score, health, and any other necessary variables
                player.points = 0
                player.health = 5
                # Reset any other game-related variables
                enemy_bullet_group.empty()
                enemy_group.empty()
                boss_group.empty()
                # Start a new game loop
                continue
            elif result == "leave":
                running = False  # Exit the game loop and end the game
                pygame.quit()
                sys.exit()

    if len(enemy_group) == 0:
        spawn_enemies(player.kills // 10 + 1)  # Spawn a new wave of enemies

    if len(boss_group) == 0:
        spawn_boss(player.kills // 50 + 1)

    if pygame.sprite.spritecollideany(player, enemy_group):
        result = game_over(player.points)  # Call the game over function and pass the player's score
        if result == "restart":
            # Reset the game and start a new game loop
            # Reset player score, health, and any other necessary variables
            player.points = 0
            player.health = 5
            # Reset any other game-related variables
            enemy_bullet_group.empty()
            enemy_group.empty()
            boss_group.empty()
            # Start a new game loop
            continue
        
        elif result == "leave":
            running = False  # Exit the game loop and end the game
            pygame.quit()
            sys.exit()

    if pygame.sprite.spritecollideany(player, boss_group):
        result = game_over(player.points)  # Call the game over function and pass the player's score
        if result == "restart":
            # Reset the game and start a new game loop
            # Reset player score, health, and any other necessary variables
            player.points = 0
            player.health = 5
            # Reset any other game-related variables
            enemy_bullet_group.empty()
            enemy_group.empty()
            boss_group.empty()
            # Start a new game loop
            continue

        elif result == "leave":
            running = False  # Exit the game loop and end the game
            pygame.quit()
            sys.exit()

    health_bar(screen, 10, 50, player.health, 5)  # Display the player's health bar

    score = render_score(player.points)  # Render the player's score
    screen.blit(score, (10, 10))  # Display the score on the screen

    pygame.display.update()
    clock.tick(60)

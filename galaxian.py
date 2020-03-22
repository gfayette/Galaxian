#!/usr/bin/env python3
"""
George Fayette
Justin Keller
CIS 343
Arcade Game in Python
3-22-2020
"""
import pygame
import random
import sys

# Class for handling the game overlay
class Overlay(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(50)
        pygame.mixer.music.load('assets/loop.wav')
        pygame.mixer.music.play(-1)
        super(pygame.sprite.Sprite, self).__init__()
        self.image = pygame.Surface((800, 20))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.text = self.font.render('', True, (255, 255, 255))

    # Change the text on the overlay
    def render(self, text):
        self.text = self.font.render(text, True, (255, 255, 255))
        self.image.blit(self.text, self.rect)

    # Draw the overlay
    def draw(self, screen):
        screen.blit(self.text, (0, 0))

    # Update score and lives
    def update(self, score, lives):
        self.render('Score: ' + str(score) + '        Lives: ' + str(lives))


# Class for handling the player's ship
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'assets/ship.png')
        self.rect = self.image.get_rect()
        self.rect.x = 375
        self.rect.y = 500

    # Draw the ship
    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Class for handling enemy ships
class EnemyShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'assets/enemy.png')
        self.rect = self.image.get_rect()
        self.offset = 0
        self.velocity = 1

    # Update the enemy ship's position and possibly fire a laser
    def update(self, game, blocks, enemy_lasers):
        if abs(self.offset) > 60:
            self.velocity = self.velocity * -1
        self.rect.x = self.rect.x + self.velocity
        self.offset = self.offset + self.velocity
        if random.randint(0, 500) < 1:
            enemy_laser = EnemyLaser()
            enemy_laser.rect.x = self.rect.x + 44
            enemy_laser.rect.y = self.rect.y + 50
            enemy_lasers.add(enemy_laser)


# Class for handling the player's lasers
class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'assets/laser.png')
        self.rect = self.image.get_rect()

    # Update the player's laser and detect collisions
    def update(self, game, enemy_ships, ship):
        if self.rect.y < 0:
            self.kill()
        hit_object = pygame.sprite.spritecollideany(self, enemy_ships)
        if hit_object:
            self.kill()
            hit_object.kill()
            game.score += 1
        self.rect.y -= 10


# Class for handling enemy lasers
class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'assets/enemy_laser.png')
        self.rect = self.image.get_rect()

    # Update the enemy laser and detect collisions
    def update(self, game, enemy_ships, ship):
        if self.rect.y > 600:
            self.kill()
        if pygame.sprite.collide_rect(self, ship):
            self.kill()
            pygame.event.post(game.new_life_event)
        self.rect.y += 5


# The player shoots a laser
def shoot(game, x, y):
    laser = Laser()
    laser.rect.x = game.ship.rect.x + x
    laser.rect.y = game.ship.rect.y + y
    game.lasers.add(laser)


# Draw the screen
def draw(game, dead):
    game.overlay.draw(game.screen)
    game.lasers.draw(game.screen)
    game.enemy_lasers.draw(game.screen)
    game.enemy_ships.draw(game.screen)
    if not dead:
        game.ship.draw(game.screen)
    pygame.display.flip()


# Display a message
def message(game, text, dead):
    game.overlay.render(text)
    draw(game, dead)
    pygame.time.delay(1000)


# Class for handling the game events and game mechanics
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        self.lasers = pygame.sprite.Group()
        self.ship = Ship()
        self.enemy_ships = pygame.sprite.Group()
        self.enemy_lasers = pygame.sprite.Group()
        self.new_life_event = pygame.event.Event(pygame.USEREVENT + 1)
        self.overlay = Overlay()
        self.screen.fill((255, 255, 255))
        self.game_started = False
        self.upgraded = False
        self.score = 0
        self.lives = 5
        self.enemy_offset = 0
        self.enemy_velocity = 5
        for i in range(0, 3):
            for j in range(0, 6):
                block = EnemyShip()
                block.rect.x = j * 120 + 50
                block.rect.y = i * 80 + 40
                self.enemy_ships.add(block)
        self.overlay.render('Galaxian!')

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == self.new_life_event.type:
                    self.lives -= 1
                    self.game_started = False
                    if self.lives <= 0:
                        message(self, 'You Lose!', True)
                        pygame.quit()
                        sys.exit(0)
                    message(self, 'You Died!', True)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if not self.game_started:
                        self.game_started = True
                    else:
                        if event.key == pygame.K_SPACE:
                            shoot(self, 44, 0)
                            if self.upgraded:
                                shoot(self, 88, 25)
                                shoot(self, 0, 25)
                        if event.key == pygame.K_LEFT:
                            self.ship.rect.x -= 12
                            if self.ship.rect.x <= 0:
                                self.ship.rect.x = 0
                        if event.key == pygame.K_RIGHT:
                            self.ship.rect.x += 12
                            if self.ship.rect.x >= 700:
                                self.ship.rect.x = 700
            if self.game_started:
                if len(self.enemy_ships) < 10 and not self.upgraded:
                    message(self, 'Weapons Upgrade!', False)
                    self.upgraded = True
                if len(self.enemy_ships) == 0:
                    message(self, 'You Win!', False)
                    pygame.quit()
                    sys.exit(0)
                self.enemy_ships.update(self, self.enemy_ships, self.enemy_lasers)
                self.enemy_lasers.update(self, self.enemy_ships, self.ship)
                self.overlay.update(self.score, self.lives)
                self.lasers.update(self, self.enemy_ships, self.ship)
            draw(self, False)
            self.clock.tick(60)


# Starting point for the program
if __name__ == "__main__":
    game = Game()
    game.run()

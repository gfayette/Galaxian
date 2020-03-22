#!/usr/bin/env python3

import pygame
import random
import sys


class Overlay(pygame.sprite.Sprite):
    def __init__(self):
        super(pygame.sprite.Sprite, self).__init__()
        self.image = pygame.Surface((800, 20))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.render('Score: 0        Lives: 5')

    def render(self, text):
        self.text = self.font.render('Galaxian!', True, (255, 255, 255))
        self.image.blit(self.text, self.rect)

    def draw(self, screen):
        screen.blit(self.text, (0, 0))

    def update(self, score, lives):
        self.render('Score: ' + str(score) + '        Lives: ' + str(lives))


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'assets/ship.png')
        self.rect = self.image.get_rect()
        self.rect.x = 375
        self.rect.y = 500

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class EnemyShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'assets/enemy.png')
        self.rect = self.image.get_rect()
        self.offset = 0
        self.velocity = 1

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


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'assets/laser.png')
        self.rect = self.image.get_rect()

    def update(self, game, blocks, paddle):
        if self.rect.y < 0:
            self.kill()
        hitObject = pygame.sprite.spritecollideany(self, blocks)
        if hitObject:
            self.kill()
            hitObject.kill()
            game.score += 1
        self.rect.y -= 10


class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'assets/enemy_laser.png')
        self.rect = self.image.get_rect()

    def update(self, game, blocks, paddle):
        if self.rect.y > 600:
            self.kill()
        if pygame.sprite.collide_rect(self, paddle):
            self.kill()
            pygame.event.post(game.new_life_event)
        self.rect.y += 10


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
        self.score = 0
        self.lives = 500000
        self.enemy_offset = 0
        self.enemy_velocity = 5
        for i in range(0, 4):
            for j in range(0, 6):
                block = EnemyShip()
                block.rect.x = j * 120 + 50
                block.rect.y = i * 80
                self.enemy_ships.add(block)

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == self.new_life_event.type:
                    self.lives -= 1
                    self.game_started = False
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit(0)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if not self.game_started:
                        self.game_started = True
                    else:
                        if event.key == pygame.K_SPACE:
                            ball = Laser()
                            ball.rect.x = self.ship.rect.x + 44
                            ball.rect.y = self.ship.rect.y
                            self.lasers.add(ball)
                        if event.key == pygame.K_LEFT:
                            self.ship.rect.x -= 12
                            if self.ship.rect.x <= 0:
                                self.ship.rect.x = 0
                        if event.key == pygame.K_RIGHT:
                            self.ship.rect.x += 12
                            if self.ship.rect.x >= 750:
                                self.ship.rect.x = 750
            if self.game_started:
                if len(self.enemy_ships) == 0:
                    pygame.quit()
                    sys.exit(0)
                self.enemy_ships.update(self, self.enemy_ships, self.enemy_lasers)
                self.lasers.update(self, self.enemy_ships, self.ship)
                self.enemy_lasers.update(self, self.enemy_ships, self.ship)
                self.overlay.update(self.score, self.lives)
                self.lasers.draw(self.screen)
                self.enemy_lasers.draw(self.screen)
                self.ship.draw(self.screen)
                self.enemy_ships.draw(self.screen)
                self.overlay.draw(self.screen)
                pygame.display.flip()
                self.clock.tick(60)


class Intro(pygame.sprite.Sprite):
    def __init__(self):
        super(pygame.sprite.Sprite, self).__init__()
        self.image = pygame.Surface((800, 20))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font('freesansbold.ttf', 18)

    def draw(self, screen):
        screen.blit(self.text, (0, 0))


if __name__ == "__main__":
    pygame.init()
    pygame.key.set_repeat(50)
    pygame.mixer.music.load('assets/loop.wav')
    pygame.mixer.music.play(-1)
    intro = Intro()
    game = Game()
    game.run()

import pygame as pg
from random import *
from properties import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = BAT_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(self.game.blue_bat, (TILESIZE, PLAYER_LENGTH))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vel = PLAYER_SPEED

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.y > 0:
            self.y -= self.vel * self.game.dt
        elif keys[pg.K_DOWN] and self.y < HEIGHT - PLAYER_LENGTH:
            self.y += self.vel * self.game.dt

    def update(self):
        self.get_keys()

        self.rect.x = self.x
        self.rect.y = self.y

class Opponent(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = BAT_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(self.game.red_bat, (TILESIZE, OPPONENT_LENGTH))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vel = OPPONENT_SPEED
        self.dir = 1
        if self.game.m_2player:
            self.control = True
        else:
            self.control = False

    def move(self):
        if self.y + OPPONENT_LENGTH//2 > self.game.ball.y \
                and self.game.ball.y > OPPONENT_LENGTH//2:
            self.dir = -1
        elif self.y + OPPONENT_LENGTH//2 < self.game.ball.y\
                and self.game.ball.y < HEIGHT - OPPONENT_LENGTH//2:
            self.dir = 1
        else:
            self.dir = 0

        self.y += self.vel * self.dir * self.game.dt

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.y > 0:
            self.y -= self.vel * self.game.dt
        elif keys[pg.K_s] and self.y < HEIGHT - OPPONENT_LENGTH:
            self.y += self.vel * self.game.dt

    def update(self):
        if not self.control:
            self.move()
        elif self.control:
            self.get_keys()

        self.rect.x = self.x
        self.rect.y = self.y

class Ball(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = BALL_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(self.game.ball_sprite, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.velx = BALL_SPEED_X
        self.vely = BALL_SPEED_Y * choice([-1, 1])
        self.dir = 1

    def update(self):
        if self.y > HEIGHT - TILESIZE or self.y < 0:
            self.vely *= -1

        if self.x > WIDTH + TILESIZE:
            self.game.point_scored = 0
            self.velx = BALL_SPEED_X
            self.game.player_score += 1
            self.x = WIDTH - TILESIZE*2
            self.y = HEIGHT/2
            self.dir = -1
            self.game.opponent.vel = OPPONENT_SPEED
            self.vely *= -1
            self.game.player.y = (HEIGHT/(TILESIZE*2) - PLAYER_LENGTH/(TILESIZE*2)) * TILESIZE
            self.game.opponent.y = (HEIGHT/(TILESIZE*2) - OPPONENT_LENGTH/(TILESIZE*2)) * TILESIZE

        elif self.x < -TILESIZE:
            self.game.point_scored = 1
            self.velx = BALL_SPEED_X
            self.game.opponent_score += 1
            self.x = TILESIZE*2
            self.y = HEIGHT/2
            self.dir = 1
            self.game.opponent.vel = OPPONENT_SPEED
            self.vely *= -1
            self.game.player.y = (HEIGHT/(TILESIZE*2) - PLAYER_LENGTH/(TILESIZE*2)) * TILESIZE
            self.game.opponent.y = (HEIGHT/(TILESIZE*2) - OPPONENT_LENGTH/(TILESIZE*2)) * TILESIZE

        self.x += self.velx * self.dir * self.game.dt
        self.y += self.vely * self.game.dt

        self.rect.x = self.x
        self.rect.y = self.y
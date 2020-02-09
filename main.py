import pygame as pg
from pygame.locals import *
import sys
from os import path
from properties import *
from characters import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Ping Pong 2D")
        self.clock = pg.time.Clock()
        self.load_data()
        self.speed_up = 0
        self.player_score = 0
        self.opponent_score = 0
        self.point_scored = -1
        self.paused = False
        self.just_started = False
        self.show_menu = True
        self.m_1player = False
        self.m_2player = False
        self.m_quit = False
        self.m_controls = False
        self.show_controls = False
        self.p_menu = False
        self.p_quit = False
        self.show_dif = False
        self.easy = False
        self.normal = False
        self.hard = False
        self.game_over = False
        self.e_menu = False
        self.e_quit = False

    def draw_text(self, text, font_name, size, color, x, y):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        data_folder = path.join(game_folder, 'data')
        self.font = path.join(data_folder, "good times rg.ttf")
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        #loading sprites
        self.ball_sprite = pg.image.load(path.join(data_folder, BALL_SPRITE)).convert()
        self.table = pg.image.load(path.join(data_folder, TABLE_IMG)).convert()
        self.blue_bat = pg.image.load(path.join(data_folder, BLUE_BAT)).convert()
        self.red_bat = pg.image.load(path.join(data_folder, RED_BAT)).convert()

        #loading sound
        self.hit_sound = pg.mixer.Sound(path.join(data_folder, 'jump.wav'))

    def quit(self):
        pg.quit()
        sys.exit()

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()

        self.opponent = Opponent(self, WIDTH/TILESIZE - 1, HEIGHT/(TILESIZE*2) - OPPONENT_LENGTH/(TILESIZE*2))
        self.ball = Ball(self, 1, HEIGHT/(TILESIZE*2))
        self.player = Player(self, 0, HEIGHT/(TILESIZE*2) - PLAYER_LENGTH/(TILESIZE*2))

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.event()
            if not self.paused:
                self.update()
            self.draw()


    def event(self):
        now = pg.time.get_ticks()
        if now - self.speed_up > SPEED_UP_TIME:
            self.speed_up = now
            if self.ball.velx < BALL_SPEED_LIMIT:
                self.ball.velx += BALL_SPEED_INCREASE
            if not self.opponent.control:
                if self.opponent.vel > OPPONENT_LEAST_FATIGUE:
                    if self.easy:
                        self.opponent.vel -= OPPONENT_FATIGUE + 20
                    elif self.normal:
                        self.opponent.vel -= OPPONENT_FATIGUE
                    elif self.hard:
                        self.opponent.vel -= OPPONENT_FATIGUE - 20

        for event in pg.event.get():
            if event.type == QUIT:
                self.quit()
            if event.type == KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.p_menu:
                        self.playing = False
                        self.show_menu = True
                    elif self.p_quit:
                        self.quit()

    def update(self):
        self.all_sprites.update()

        if self.player_score > SCORE_LIMIT or self.opponent_score > SCORE_LIMIT:
            self.playing = False
            self.game_over = True

        #collision of ball and player
        hits = pg.sprite.collide_rect(self.player, self.ball)
        if hits:
            self.hit_sound.play()
            self.ball.dir = 1
            if (self.ball.y < self.player.y and self.ball.vely > 0) \
                    or (self.ball.y + BALL_SIZE > self.player.y + PLAYER_LENGTH and self.ball.vely < 0):
                self.ball.vely *= -1

        #collision of opponent and ball
        hits = pg.sprite.collide_rect(self.opponent, self.ball)
        if hits:
            self.hit_sound.play()
            self.ball.dir = -1
            if (self.ball.y < self.opponent.y and self.ball.vely > 0) \
                    or (self.ball.y + BALL_SIZE > self.opponent.y + PLAYER_LENGTH and self.ball.vely < 0):
                self.ball.vely *= -1

    def draw(self):
        self.screen.blit(pg.transform.scale(self.table, (WIDTH, HEIGHT)), (0,0))
        #pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.all_sprites.draw(self.screen)

        self.draw_text(str(self.player_score), self.font, 40, WHITE, WIDTH/2 - TILESIZE * 2, 50)
        self.draw_text(str(self.opponent_score), self.font, 40, WHITE, WIDTH/2 + TILESIZE * 2, 50)

        if self.point_scored is 0 or self.point_scored is 1:
            self.point()
            self.wait_for_key()
            self.point_scored = -1

        if self.just_started:
            self.starting()
            self.wait_for_key()
            self.just_started = False

        if self.paused:
            self.pause_screen()

        pg.display.flip()

    def control(self):
        self.screen.fill(BLACK)

        self.draw_text("Player One", self.font, 20,BLUE, 200, 50)
        self.draw_text("Arrow Keys", self.font, 15, WHITE, 200, 150)
        self.draw_text("'UP' & 'DOWN'", self.font, 15, WHITE, 200, 200)
        self.draw_text("Player Two", self.font, 20, RED, 550, 50)
        self.draw_text("'W' for Up", self.font, 15, WHITE, 550, 150)
        self.draw_text("'S' for Down", self.font, 15, WHITE, 550, 200)
        self.draw_text("'Esc' to pause", self.font, 15, WHITE, 350, 250)
        self.draw_text("Press any key to continue", self.font, 20, WHITE, WIDTH/2, HEIGHT - TILESIZE*3)

        pg.display.flip()

    def point(self):
        self.screen.blit(self.dim_screen, (0,0))
        if self.point_scored is 1:
            self.draw_text("RED SCORED", self.font, 50, RED, WIDTH/2, HEIGHT/2)

        elif self.point_scored is 0:
            self.draw_text("BLUE SCORED", self.font, 50, BLUE, WIDTH/2, HEIGHT / 2)

        pg.display.flip()

    def starting(self):
        self.screen.blit(self.dim_screen, (0,0))
        self.draw_text("Press any key to start", self.font, 50, WHITE, WIDTH/2, HEIGHT/2)

        self.player_score = 0
        self.opponent_score = 0
        self.ball.x = WIDTH/2
        self.ball.y = HEIGHT/2
        self.ball.dir = 1
        self.ball.velx = BALL_SPEED_X
        self.opponent.vel = OPPONENT_SPEED
        self.player.y = (HEIGHT / (TILESIZE * 2) - PLAYER_LENGTH / (TILESIZE * 2)) * TILESIZE
        self.opponent.y = (HEIGHT / (TILESIZE * 2) - OPPONENT_LENGTH / (TILESIZE * 2)) * TILESIZE

        pg.display.flip()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def pause_screen(self):
        self.screen.blit(self.dim_screen, (0,0))
        self.draw_text("PAUSED", self.font, 50, RED, WIDTH/2, HEIGHT/2 - TILESIZE*2)

        self.mouse = pg.mouse.get_pos()

        if 400 > self.mouse[0] > 300 and 350 > self.mouse[1] > 300:
            pg.draw.rect(self.screen, LIGHTGREY, (300, 300, 100, 50))
            self.p_menu = True
        else:
            pg.draw.rect(self.screen, GREY, (300, 300, 100, 50))
            self.p_menu = False

        if 600 > self.mouse[0] > 500 and 350 > self.mouse[1] > 300:
            pg.draw.rect(self.screen, LIGHTGREY, (500, 300, 100, 50))
            self.p_quit = True
        else:
            pg.draw.rect(self.screen, GREY, (500, 300, 100, 50))
            self.p_quit = False

        self.draw_text("Menu", self.font, 15, WHITE, 350, 325)
        self.draw_text("Quit", self.font, 15, WHITE, 550, 325)

        pg.display.flip()

    def start_game(self):
        self.paused = False
        for event in pg.event.get():
            if event.type == QUIT:
                self.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.m_1player:
                        self.show_menu = False
                        self.show_dif = True
                    elif self.m_2player:
                        self.show_menu = False
                        self.just_started = True
                    elif self.m_controls:
                        self.show_controls = True
                    elif self.m_quit:
                        self.quit()

        if not self.show_controls:
            self.screen.fill(BLACK)
            self.draw_text("PING PONG 2D", self.font, 60, RED, WIDTH/2, 80)

            self.mouse = pg.mouse.get_pos()
            if 400 > self.mouse[0] > 300 and 250 > self.mouse[1] > 200:
                pg.draw.rect(self.screen, LIGHTGREY, (300, 200, 100, 50))
                self.m_1player = True
            else:
                pg.draw.rect(self.screen, GREY, (300, 200, 100, 50))
                self.m_1player = False

            if 400 > self.mouse[0] > 300 and 330 > self.mouse[1] > 280:
                pg.draw.rect(self.screen, LIGHTGREY, (300, 280, 100, 50))
                self.m_2player = True
            else:
                pg.draw.rect(self.screen, GREY, (300, 280, 100, 50))
                self.m_2player = False

            if 600 > self.mouse[0] > 500 and 400 > self.mouse[1] > 350:
                pg.draw.rect(self.screen, LIGHTGREY, (500, 350, 100, 50))
                self.m_quit = True
            else:
                pg.draw.rect(self.screen, GREY, (500, 350, 100, 50))
                self.m_quit = False

            if 600 > self.mouse[0] > 500 and 250 > self.mouse[1] > 200:
                pg.draw.rect(self.screen, LIGHTGREY, (500, 200, 100, 50))
                self.m_controls = True
            else:
                pg.draw.rect(self.screen, GREY, (500, 200, 100, 50))
                self.m_controls = False

            self.draw_text("One Player", self.font, 10, WHITE, 350, 225)
            self.draw_text("Two Players", self.font, 10, WHITE, 350, 305)
            self.draw_text("QUIT", self.font, 20, WHITE, 550, 375)
            self.draw_text("Controls", self.font, 10, WHITE, 550, 225)
        elif self.show_controls:
            self.control()
            self.wait_for_key()
            self.show_controls = False

        pg.display.flip()

    def difficulty_screen(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.easy:
                        self.show_dif = False
                        self.just_started = True
                    elif self.normal:
                        self.show_dif = False
                        self.just_started = True
                    elif self.hard:
                        self.show_dif = False
                        self.just_started = True

        self.screen.fill(BLACK)
        self.draw_text("Select Difficulty", self.font, 40, RED, WIDTH/2, TILESIZE*3)

        self.mouse = pg.mouse.get_pos()
        if 500 > self.mouse[0] > 400 and 200 > self.mouse[1] > 150:
            pg.draw.rect(self.screen, LIGHTGREY, (400, 150, 100, 50))
            self.easy = True
        else:
            pg.draw.rect(self.screen, GREY, (400, 150, 100, 50))
            self.easy = False

        if 500 > self.mouse[0] > 400 and 300 > self.mouse[1] > 250:
            pg.draw.rect(self.screen, LIGHTGREY, (400, 250, 100, 50))
            self.normal = True
        else:
            pg.draw.rect(self.screen, GREY, (400, 250, 100, 50))
            self.normal = False

        if 500 > self.mouse[0] > 400 and 400 > self.mouse[1] > 350:
            pg.draw.rect(self.screen, LIGHTGREY, (400, 350, 100, 50))
            self.hard = True
        else:
            pg.draw.rect(self.screen, GREY, (400, 350, 100, 50))
            self.hard = False

        self.draw_text("Easy", self.font, 15, WHITE, 450, 175)
        self.draw_text("Normal", self.font, 15, WHITE, 450, 275)
        self.draw_text("Hard", self.font, 15, WHITE, 450, 375)

        pg.display.flip()

    def end_game(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.e_menu:
                        self.game_over = False
                        self.show_menu = True
                    elif self.e_quit:
                        self.quit()

        self.screen.fill(BLACK)
        if self.player_score > SCORE_LIMIT:
            self.draw_text("Blue Won", self.font, 40, BLUE, WIDTH/2, TILESIZE*3)
        else:
            self.draw_text("Red Won", self.font, 40 ,RED, WIDTH/2, TILESIZE*3)

        self.mouse = pg.mouse.get_pos()
        if 500 > self.mouse[0] > 400 and 250 > self.mouse[1] > 200:
            pg.draw.rect(self.screen, LIGHTGREY, (400, 200, 100, 50))
            self.e_menu = True
        else:
            pg.draw.rect(self.screen, GREY, (400, 200, 100, 50))
            self.e_menu = False

        if 500 > self.mouse[0] > 400 and 350 > self.mouse[1] > 300:
            pg.draw.rect(self.screen, LIGHTGREY, (400, 300, 100, 50))
            self.e_quit = True
        else:
            pg.draw.rect(self.screen, GREY, (400, 300, 100, 50))
            self.e_quit = False

        self.draw_text("Menu", self.font, 15, WHITE, 450, 225)
        self.draw_text("Quit", self.font, 15, WHITE, 450, 325)

        pg.display.flip()


g = Game()
while True:
    if g.show_menu:
        g.start_game()
    elif g.show_dif:
        g.difficulty_screen()
    elif not g.game_over:
        g.new()
        g.run()
    if g.game_over:
        g.end_game()
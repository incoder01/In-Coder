#game properties
WIDTH = 896 #28
HEIGHT = 512 #16
TILESIZE = 32
FPS = 60
SCORE_LIMIT = 5

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHTGREY = (100,100,100)
GREY = (50, 50, 50)

#player properties
PLAYER_COLOR = WHITE
PLAYER_LENGTH = TILESIZE * 4
PLAYER_SPEED = 400

#opponent properties
OPPONENT_FATIGUE = 25 #normal
OPPONENT_LEAST_FATIGUE = 200
OPPONENT_COLOR = RED
OPPONENT_LENGTH = TILESIZE * 4
OPPONENT_SPEED = 400

#ball properties
BALL_SIZE = TILESIZE
BALL_SPEED_INCREASE =100
BALL_SPEED_LIMIT = 1800
BALL_COLOR  = GREEN
SPEED_UP_TIME = 2000
BALL_SPEED_Y = 300
BALL_SPEED_X = 500

#sprites
BALL_SPRITE = 'ping pong ball.png'
TABLE_IMG = 'ping pong table 2.png'
BLUE_BAT = 'pong bat blue.png'
RED_BAT = 'pong red bat.png'

#layers
BAT_LAYER = 1
BALL_LAYER = 2
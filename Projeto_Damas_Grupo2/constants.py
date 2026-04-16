import pygame

BOARD_SIZE, STATUS_HEIGHT = 600, 120
WIDTH, HEIGHT = BOARD_SIZE, BOARD_SIZE + STATUS_HEIGHT
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_SIZE // COLS

MAX_TIME = 900 
LIMIT_EMPATE = 40 

CREAM, BROWN = (240, 230, 140), (139, 69, 19)
BLACK, WHITE, GRAY = (0, 0, 0), (255, 255, 255), (200, 200, 200)
RED, GOLD, BLUE, GREEN = (255, 0, 0), (255, 215, 0), (70, 130, 180), (0, 255, 0)

pygame.init()
FONT = pygame.font.SysFont('Arial', 18)
BIG_FONT = pygame.font.SysFont('Arial', 40, bold=True)
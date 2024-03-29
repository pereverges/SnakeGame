import sys, pygame, random

#SIZES
GRID_HEIGHT = GRID_WIDTH = 800
CELL_HEIGHT = CELL_WIDTH = 20
WINDOW_TEXT_HEIGHT = 100
WINDOW_HEIGHT = GRID_HEIGHT + WINDOW_TEXT_HEIGHT
WINDOW_WIDTH = GRID_WIDTH
SNAKE_SPAWN_MARGIN = 5
TEXT_MARGIN = 10

#COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)

#NUMBER OF CELLS
N_VERTICAL_CELLS = int(GRID_HEIGHT/CELL_HEIGHT)
N_HORITZONTAL_CELLS = int(GRID_WIDTH/CELL_WIDTH)

#DIRECTION
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

class Snake:
    def __init__(self):
        self.body = [(random.randint(0+SNAKE_SPAWN_MARGIN, N_HORITZONTAL_CELLS-1-SNAKE_SPAWN_MARGIN), random.randint(0+SNAKE_SPAWN_MARGIN, N_VERTICAL_CELLS-1-SNAKE_SPAWN_MARGIN))]
        self.direction = UP
        self.apple = self.new_apple()
        self.speed = 2
        self.score = 0
        self.pause = False
        self.lost = False

    def size(self):
        return len(self.body)

    def get_head(self):
        return self.body[0]

    def get_snake(self):
        return self.body

    def get_apple(self):
        return self.apple

    def get_speed(self):
        return self.speed

    def get_apples_eaten(self):
        return self.score

    def remove_tail(self):
        x, y = self.body[self.size() - 1]
        draw_cell(x,y,BLACK)
        del self.body[self.size() - 1]

    def new_apple(self):
        possible_values = list(range(0, N_VERTICAL_CELLS * N_HORITZONTAL_CELLS))
        for x, y in self.body:
            possible_values.remove(x * N_HORITZONTAL_CELLS + y)
        position = random.choice(possible_values)
        return int(position/N_HORITZONTAL_CELLS), position % N_HORITZONTAL_CELLS

    def move(self):
        x, y = self.get_head()
        if self.direction == UP:
            self.body.insert(0, (x, y - 1))
        elif self.direction == DOWN:
            self.body.insert(0, (x, y + 1))
        elif self.direction == LEFT:
            self.body.insert(0, (x - 1, y))
        elif self.direction == RIGHT:
            self.body.insert(0, (x + 1, y))
        if self.get_head() == self.get_apple():
            if self.get_apples_eaten()%3 == 0:
                self.speed += 1
            self.score+=1
            draw_score()
            self.apple = self.new_apple()
            draw_apple()
        else:
            self.remove_tail()
        x_head, y_head = self.get_head()
        if x_head < 0 or x_head >= N_HORITZONTAL_CELLS or y_head < 0 or y_head >= N_VERTICAL_CELLS:
            lost()
        if self.eats_itself():
            lost()
            
    def eats_itself(self):
        x_head, y_head = self.get_head()
        for x, y in self.body[1::]:
            if x_head == x and y_head == y:
                return True
        return False

#GLOBAL INIT
SNAKE = Snake()
pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH + 1, WINDOW_HEIGHT + 1))
SCREEN.fill(BLACK)

#INITS
def text_init():
    pygame.font.init()
    draw_score()

def screen_init():
    draw_grid()
    draw_apple()
    draw_snake()
    text_init()

#EXIT GAME

def stop():
    pygame.quit()
    sys.exit()

#DRAWERS

def draw_grid():
    for x in range(0, GRID_WIDTH + 1, CELL_WIDTH):
        pygame.draw.line(SCREEN, WHITE, (x,0), (x, GRID_HEIGHT + 1))
    for y in range(0, GRID_HEIGHT + 1, CELL_HEIGHT):
        pygame.draw.line(SCREEN, WHITE, (0,y), (GRID_WIDTH + 1, y))

def draw_cell(x,y,color):
    x = x*CELL_WIDTH
    y = y*CELL_HEIGHT
    cell = pygame.Rect(x+1,y+1,CELL_WIDTH-1,CELL_HEIGHT-1)
    pygame.draw.rect(SCREEN,color,cell)
    pygame.display.update()

def draw_apple():
    x, y = SNAKE.get_apple()
    draw_cell(x,y,RED)

def draw_snake():
    for x,y in SNAKE.get_snake():
        draw_cell(x,y,GREEN)

def draw_score():
    font_score = pygame.font.SysFont('Exo', 32)
    cell = pygame.Rect(0, GRID_HEIGHT, GRID_WIDTH,  WINDOW_TEXT_HEIGHT)
    pygame.draw.rect(SCREEN, BLACK, cell)
    score_text_surface = font_score.render('Score: ' + str(SNAKE.score), False, WHITE)
    SCREEN.blit(score_text_surface,(TEXT_MARGIN,GRID_HEIGHT+TEXT_MARGIN+10))
    speed_text_surface = font_score.render('Speed: ' + str(SNAKE.speed - 1), False, WHITE)
    SCREEN.blit(speed_text_surface,(TEXT_MARGIN,GRID_HEIGHT+TEXT_MARGIN+40))
    score_text_surface = font_score.render('Pause: [P]', False, WHITE)
    SCREEN.blit(score_text_surface,(WINDOW_WIDTH-115,GRID_HEIGHT+TEXT_MARGIN+10))
    pygame.display.update()

def draw_text(text):
    font_score = pygame.font.SysFont('Exo', 40)
    cell = pygame.Rect(200, GRID_HEIGHT+1, GRID_WIDTH, WINDOW_TEXT_HEIGHT)
    pygame.draw.rect(SCREEN, BLACK, cell)
    score_text_surface = font_score.render(text, False, WHITE)
    SCREEN.blit(score_text_surface, (340, GRID_HEIGHT + TEXT_MARGIN+25))
    pygame.display.update()

def lost():
    SNAKE.lost = True
    font_score = pygame.font.SysFont('Exo', 40)
    text_cell = pygame.Rect(0, GRID_HEIGHT+1, GRID_WIDTH, WINDOW_TEXT_HEIGHT)
    pygame.draw.rect(SCREEN, BLACK, text_cell)
    pygame.display.update()
    score_text_surface = font_score.render('YOU LOST WITH AN SCORE OF ' + str(SNAKE.score), False, WHITE)
    SCREEN.blit(score_text_surface, (160, GRID_HEIGHT + TEXT_MARGIN+25))
    font_score = pygame.font.SysFont('Exo', 32)
    score_text_surface = font_score.render('To restart press R', False, WHITE)
    SCREEN.blit(score_text_surface, (280, GRID_HEIGHT + TEXT_MARGIN + 55))
    pygame.display.update()

#MAIN LOOP

def restart_game():
    global SNAKE
    SNAKE = Snake()
    cell = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(SCREEN, BLACK, cell)
    screen_init()

def loop():
    while True:
        if not SNAKE.pause and not SNAKE.lost:
            SNAKE.move()
            draw_grid()
            draw_snake()
            pygame.display.update()
            pygame.time.Clock().tick(SNAKE.get_speed())
            if SNAKE.lost:
                lost()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()
            elif event.type == pygame.KEYDOWN:
                if SNAKE.pause:
                    if event.key == pygame.K_p:
                        SNAKE.pause = False
                        draw_score()
                elif SNAKE.lost:
                    if event.key == pygame.K_r:
                        restart_game()
                else:
                    if event.key == pygame.K_UP and SNAKE.direction != DOWN:
                        SNAKE.direction = UP
                    elif event.key == pygame.K_DOWN and SNAKE.direction != UP:
                        SNAKE.direction = DOWN
                    elif event.key == pygame.K_RIGHT and SNAKE.direction != LEFT:
                        SNAKE.direction = RIGHT
                    elif event.key == pygame.K_LEFT and SNAKE.direction != RIGHT:
                        SNAKE.direction = LEFT
                    elif event.key == pygame.K_p:
                        draw_text('PAUSE')
                        SNAKE.pause = True

def main():
    screen_init()
    loop()

main()
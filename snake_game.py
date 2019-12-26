import sys, pygame, numpy, random

GRID_HEIGHT = 400
GRID_WIDTH = 400
CELL_HEIGHT = CELL_WIDTH = 20
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
N_VERTICAL_CELLS = int(GRID_HEIGHT/CELL_HEIGHT)
N_HORITZONTAL_CELLS = int(GRID_WIDTH/CELL_WIDTH)

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

class Snake:
    def __init__(self):
        self.body = [(random.randint(0, N_HORITZONTAL_CELLS-1), random.randint(0, N_VERTICAL_CELLS-1))]
        self.direction = RIGHT
        self.apple = self.new_apple()

    def size(self):
        return len(self.body)

    def get_head(self):
        return self.body[0]

    def remove_tail(self):
        x, y = self.body[self.size() - 1]
        draw_cell(x,y,BLACK)
        del self.body[self.size() - 1]

    def get_snake(self):
        return self.body

    def get_apple(self):
        return self.apple

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
            self.apple = self.new_apple()
            draw_apple()
        else:
            self.remove_tail()

    def new_apple(self):
        possible_values = list(range(0, N_VERTICAL_CELLS * N_HORITZONTAL_CELLS))
        for x, y in self.body:
            possible_values.remove(x * N_HORITZONTAL_CELLS + y)
        position = random.choice(possible_values)
        return int(position/N_HORITZONTAL_CELLS), position % N_HORITZONTAL_CELLS


SNAKE = Snake()
pygame.init()
SCREEN = pygame.display.set_mode((GRID_HEIGHT + 1, GRID_WIDTH + 1))
SCREEN.fill(BLACK)


def stop():
    pygame.quit()
    sys.exit()

def draw_grid():
    for x in range(0, GRID_WIDTH + 1, CELL_WIDTH):
        pygame.draw.line(SCREEN, WHITE, (x,0), (x, GRID_HEIGHT + 1))
    for y in range(0, GRID_HEIGHT + 1, CELL_HEIGHT):
        pygame.draw.line(SCREEN, WHITE, (0,y), (GRID_WIDTH + 1, y))



def main():
    draw_grid()
    draw_apple()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    SNAKE.direction = UP
                elif event.key == pygame.K_DOWN:
                    SNAKE.direction = DOWN
                elif event.key == pygame.K_RIGHT:
                    SNAKE.direction = RIGHT
                elif event.key == pygame.K_LEFT:
                    SNAKE.direction = LEFT
                SNAKE.move()
                draw_grid()
                draw_snake()
                pygame.display.update()


def draw_cell(x,y,color):
    x = x*CELL_WIDTH
    y = y*CELL_HEIGHT
    cell = pygame.Rect(x+1,y+1,CELL_WIDTH-1,CELL_HEIGHT-1)
    pygame.draw.rect(SCREEN,color,cell)
    pygame.display.update()

def draw_apple():
    x, y = SNAKE.get_apple()
    print(x,y)
    draw_cell(x,y,RED)


def draw_snake():
    for x,y in SNAKE.get_snake():
        draw_cell(x,y,GREEN)

main()
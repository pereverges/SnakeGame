import sys, pygame, numpy, random

class Snake:
    def __init__(self):
        self.body = [(random.randint(0, N_HORITZONTAL_CELLS-1), random.randint(0, N_VERTICAL_CELLS-1))]

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

    def move(self):
        x, y = self.get_head()
        if DIRECTION == UP:
            self.body.insert(0, (x, y - 1))
        elif DIRECTION == DOWN:
            self.body.insert(0, (x, y + 1))
        elif DIRECTION == LEFT:
            self.body.insert(0, (x - 1, y))
        elif DIRECTION == RIGHT:
            self.body.insert(0, (x + 1, y))
        self.remove_tail()



GRID_HEIGHT = 400
GRID_WIDTH = 400
CELL_HEIGHT = CELL_WIDTH = 20
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
N_VERTICAL_CELLS = int(GRID_HEIGHT/CELL_HEIGHT)
N_HORITZONTAL_CELLS = int(GRID_WIDTH/CELL_WIDTH)

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
DIRECTION = RIGHT

SNAKE = Snake()


#GRID = numpy.full((N_HORITZONTAL_CELLS,N_VERTICAL_CELLS),Cell)

class Snake:
    def __init__(self):
        self.body = [(random.randint(0,N_HORITZONTAL_CELLS),random.randint(0,N_VERTICAL_CELLS))]

    def size(self):
        return len(self.body)

    def get_head(self):
        return self.body[0]

    def remove_tail(self):
        del self.body[self.size()-1]

    def get_snake(self):
        return self.body

    def move(self):
        x, y = self.get_head()
        if DIRECTION == UP:
            self.body.insert(0,(x,y-1))
        elif DIRECTION == DOWN:
            self.body.insert(0,(x,y+1))
        elif DIRECTION == LEFT:
            self.body.insert(0,(x-1,y))
        elif DIRECTION == RIGHT:
            self.body.insert(0,(x+1,y))
        self.remove_tail()


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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()
            elif event.type == pygame.KEYUP:
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


def draw_snake():
    for x,y in SNAKE.get_snake():
        draw_cell(x,y,RED)

main()
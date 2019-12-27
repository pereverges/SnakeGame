import sys, pygame, random

GRID_HEIGHT = 400
GRID_WIDTH = 400
CELL_HEIGHT = CELL_WIDTH = 20
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
WINDOW_HEIGHT = GRID_HEIGHT + 100
WINDOW_WIDTH = GRID_WIDTH
N_VERTICAL_CELLS = int(GRID_HEIGHT/CELL_HEIGHT)
N_HORITZONTAL_CELLS = int(GRID_WIDTH/CELL_WIDTH)
SNAKE_SPAWN_MARGIN = 5

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
FPS = 5

class Snake:
    def __init__(self):
        self.body = [(random.randint(0+SNAKE_SPAWN_MARGIN, N_HORITZONTAL_CELLS-1-SNAKE_SPAWN_MARGIN), random.randint(0+SNAKE_SPAWN_MARGIN, N_VERTICAL_CELLS-1-SNAKE_SPAWN_MARGIN))]
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
        x_head, y_head = self.get_head()
        if x_head < 0 or x_head >= N_HORITZONTAL_CELLS or y_head < 0 or y_head >= N_VERTICAL_CELLS:
            stop()
        if self.eats_itself:
            stop()

    def eats_itself(self):
        x_head, y_head = self.get_head()
        for x, y in self.body[1::]:
            if x_head == x and y_head == y:
                return True
        return False

    def new_apple(self):
        possible_values = list(range(0, N_VERTICAL_CELLS * N_HORITZONTAL_CELLS))
        for x, y in self.body:
            possible_values.remove(x * N_HORITZONTAL_CELLS + y)
        position = random.choice(possible_values)
        return int(position/N_HORITZONTAL_CELLS), position % N_HORITZONTAL_CELLS


SNAKE = Snake()
pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH + 1, WINDOW_HEIGHT + 1))
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
    draw_snake()
    while True:
        SNAKE.move()
        draw_grid()
        draw_snake()
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and SNAKE.direction != DOWN:
                    SNAKE.direction = UP
                elif event.key == pygame.K_DOWN and SNAKE.direction != UP:
                    SNAKE.direction = DOWN
                elif event.key == pygame.K_RIGHT and SNAKE.direction != LEFT:
                    SNAKE.direction = RIGHT
                elif event.key == pygame.K_LEFT and SNAKE.direction != RIGHT:
                    SNAKE.direction = LEFT



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

main()
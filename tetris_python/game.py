import pygame 
from random import *
pygame.init()

# Constant Variable
WIDTH = 300
HEIGHT = 500
CELLSIZE = 20
FPS = 40

BG_COLOR = (20, 5, 94)
WHITE = (255,255,255)
GRID = (39, 80, 174)
BLACK = (0,0,0)
WIN = (50,230,50)
LOSE = (252,91,122)
RED = (255,0,0)

ROWS = (HEIGHT-120) //CELLSIZE
COLS = WIDTH//CELLSIZE

font = pygame.font.Font(None, 30)
font2 = pygame.font.Font(None, 55)

# Game settings - Screen, FPS, Colors
SCR = pygame.display.set_mode((WIDTH,HEIGHT), pygame.NOFRAME)
clock = pygame.time.Clock()

ASSETS = {
    1:pygame.image.load("assets/1.png"),
    2:pygame.image.load("assets/2.png"),
    3:pygame.image.load("assets/3.png"),
    4:pygame.image.load("assets/4.png"),
}

class Shape:
    VERSION = {
        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O': [[1, 2, 5, 6]]
    }
    SHAPES = ['I', 'Z', 'S', 'L', 'J', 'T', 'O']

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = choice(self.SHAPES)
        self.shape = self.VERSION[self.type]
        self.color = randint(1,4)
        self.orientation = 0

    # Image
    def image(self):
        return self.shape[self.orientation]

    # Rotate
    def rotate(self):
        self.orientation = (self.orientation + 1) % len(self.shape)
    
class Tetris:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.score = 0
        self.level = 1
        self.board = [[0 for j in range(self.cols)] for i in range(self.rows)]
        self.next = None
        self.end = False
        self.new_shape()

    def make_grid(self):
        for i in range(self.rows + 1):
            pygame.draw.line(SCR, GRID, (0,CELLSIZE*i), (WIDTH, CELLSIZE*i))

        for j in range(self.cols + 1):
            pygame.draw.line(SCR, GRID, (CELLSIZE*j,0),(CELLSIZE*j, HEIGHT - 120))

    def new_shape(self):
        if not self.next:
            self.next = Shape(5,0)
        self.figure = self.next
        self.next = Shape(5,0)



    def collision(self) -> bool:
        for i in range(4):
            for j in range(4):
                if (i*4+j) in self.figure.image():
                    block_row = i + self.figure.y
                    block_col = j + self.figure.x

                    if (block_row >= self.rows or block_col >= self.cols or block_col < 0 or self.board[block_row][block_col] > 0):
                        return True
        return False
    
    def move_down(self):
        self.figure.y += 1
        if self.collision():
            self.figure.y -= 1
            self.freeze()

    def move_left(self):
        self.figure.x -= 1
        if self.collision():
            self.figure.x += 1

    def move_right(self):
        self.figure.x += 1
        if self.collision():
            self.figure.x -= 1

    def freefall(self):
        while not self.collision():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def rotate(self):
        orientation = self.figure.orientation
        self.figure.rotate()
        if self.collision():
            self.figure.orientation = orientation

    # Freeze - ERROR
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if (i*4+j) in self.figure.image():
                    self.board[i+self.figure.y][j+self.figure.x] = self.figure.color
        self.remove_row()
        self.new_shape()
        if self.collision():
            self.end = True


    # Remove Row
    def remove_row(self):
        rerun = False
        for y in range(self.rows-1, 0, -1):
            completed = True
            for x in range(0, self.cols):
                if self.board[y][x] == 0:
                    completed = False
            if completed:
                del self.board[y]
                self.board.insert(0, [0 for i in range (self.cols)])
                self.score += 1
                if self.score % 10 == 0:
                    self.level += 1
                rerun = True
        if rerun:
            # recurrison
            self.remove_row()

    def end_game(self):
        popup = pygame.Rect(50,140,WIDTH-100, HEIGHT - 350)
        pygame.draw.rect(SCR, BLACK, popup)
        pygame.draw.rect(SCR, RED,popup, 2)

        lose = font.render("YOU LOST...", True, WHITE)
        choice1 = font.render("Press r to restart", True, WHITE)
        choice2 = font.render("Press q to quit", True, WHITE)

        SCR.blit(lose, (popup.centerx-lose.get_width()//2, popup.y + 20))
        SCR.blit(choice1, (popup.centerx-lose.get_width()//2-20, popup.y + 80))
        SCR.blit(choice2, (popup.centerx-lose.get_width()//2-20, popup.y + 110))





tetris = Tetris(ROWS, COLS)

space_pressed = False
counter = 0
move = True



run = True
while run:
    SCR.fill(BG_COLOR)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            run = False


        keys = pygame.key.get_pressed()
        if not tetris.end:
            if keys[pygame.K_LEFT]:
                tetris.move_left()
            if keys[pygame.K_RIGHT]:
                tetris.move_right()
            if keys[pygame.K_DOWN]:
                tetris.move_down()
            if keys[pygame.K_UP]:
                tetris.rotate()
            if keys[pygame.K_SPACE]:
                space_pressed = True
        if keys[pygame.K_r]:
            tetris.__init__(ROWS, COLS)
        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            run = False


    counter += 1
    if counter >= 15000:
        counter = 0

    if move:
        if counter % (FPS//(tetris.level*2)) == 0:
            if not tetris.end:
                if space_pressed:
                    tetris.freefall()
                    print("Freefall")
                    space_pressed = False
                else:
                    tetris.move_down()

    tetris.make_grid()


    # Keep shape on screen
    for x in range(ROWS):
        for y in range(COLS):
            if tetris.board[x][y] > 0:
                value = tetris.board[x][y]
                print(value)
                image = ASSETS[value]
                SCR.blit(image,(y*CELLSIZE,x*CELLSIZE))
                pygame.draw.rect(SCR, WHITE, (y*CELLSIZE, x*CELLSIZE, CELLSIZE, CELLSIZE),1)

    # Show shape on screen
    if tetris.figure:
        for i in range(4):
            for j in range(4):
                if (i*4+j) in tetris.figure.image():
                    shape = ASSETS[tetris.figure.color]
                    x = CELLSIZE * (tetris.figure.x +j)
                    y = CELLSIZE * (tetris.figure.y +i)
                    SCR.blit(shape,(x, y))
                    pygame.draw.rect(SCR, WHITE, (x, y, CELLSIZE, CELLSIZE), 1)


    if tetris.next:
        for i in range(4):
            for j in range(4):
                if (i*4+j) in tetris.next.image():
                    image = ASSETS[tetris.next.color]
                    x = CELLSIZE * (tetris.next.x + j -4) 
                    y = HEIGHT -100 +CELLSIZE * (tetris.next.y + i)
                    SCR.blit(image, (x,y))

    if tetris.end:
        tetris.end_game()

    score_text = font2.render(f"{tetris.score}", True, WHITE)
    level_text = font.render(f"Level: {tetris.level}", True, WHITE)

    SCR.blit(score_text, (250,400))
    SCR.blit(level_text, (200,440))



    

    pygame.display.update()
    clock.tick(FPS)


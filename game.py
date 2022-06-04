import pygame
import random
import sys
from pygame.locals import  *



# initializing
pygame.init()
pygame.font.init()
pygame.display.set_caption("Tasty Blocks")
clock = pygame.time.Clock()
fps = 30

# colours
black = (0, 0, 0)
white = (255, 255, 255)
purple = [(227, 159, 246), (164, 94, 229), (152, 103, 197), (163, 44, 196), (122, 73, 136), (113, 1, 147)]

# sizes
screen_size = (800, 600) # width x height
screen = pygame.display.set_mode(screen_size)
board_dimension = 9

# other
font = pygame.font.SysFont('Comic Sans', 60)
title = font.render('Tasty Blocks', False, purple[0])
text = font.render('Score', False, purple[0])

class queue_object:
    def __init__(self):
        self.q = []

    def push(self, value):
        self.q.append(value)

    def front(self):
        return self.q.pop(0)

    def size(self):
        return len(self.q)



class gamer:

    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "start"
        self.x = 6
        self.y = 6
        self.board = [[0 for _ in range(self.x + 1)] for _ in range(self.x + 1)]
        self.tile = None

    def draw_board(self):
        screen.blit(title, (250, 10))
        for i in range(self.x + 1):
            pygame.draw.line(screen, purple[0], (i * 50 + 100, 100), (i * 50 + 100, 550), 3)
        for i in range(self.y + 1):
            pygame.draw.line(screen, purple[0], (100, i * 50 + 100), (550, i * 50 + 100), 4)
    
    def spawn(self):

        option = []

        for i in range (1, self.x + 1):
            for j in range (1, self.y + 1):
                if (self.board[i][j] == 0):
                    option.append([i, j])

        if (len(option) == 0):
            self.state = "gameover"
            return 1
        
        spot = random.choice(option)
        self.board[spot[0]][spot[1]] = random.choice([3, 9])
        return 0
    
    def up(self):
        for i in range(1, self.y + 1):
            for j in range(1, self.x + 1):
                if self.board[i-2][j] == self.board[i][j] and self.board[i-1][j] > 0:
                    self.board[i-2][j] *= 3
                    self.score += self.board[i-2][j]
                    self.board[i][j] = 0

        queue = queue_object()
        for i in range(1, self.y + 1):
            for j in range(1, self.x + 1):
                if self.board[i][j] > 0:
                    queue.push([i, j])
        
        while queue.size() > 0:
            f = queue.front()
            curx = f[0]
            cury = f[1]

            if (curx == 1):
                continue
            if (self.board[curx - 1][cury] == 0):
                self.board[curx - 1][cury] = self.board[curx][cury]
                self.board[curx][cury] = 0
                if curx - 1 > 1:
                    queue.push([curx - 1, cury])

        

    def down(self):
        for i in range(self.y - 2, 0, -1):
            for j in range(self.x - 2, 0, -1):
                if self.board[i+2][j] == self.board[i][j] and self.board[i+1][j] > 0:
                    self.board[i+2][j] *= 3
                    self.score += self.board[i+2][j]
                    self.board[i][j] = 0
        
        queue = queue_object()
        for i in range(self.y, 1, -1):
            for j in range(self.x, 1, -1):
                if self.board[i][j] > 0:
                    queue.push([i, j])
        
        while queue.size() > 0:
            f = queue.front()
            curx = f[0]
            cury = f[1]
            if (curx == self.x):
                continue
            if (self.board[curx + 1][cury] == 0):
                self.board[curx + 1][cury] = self.board[curx][cury]
                self.board[curx][cury] = 0
                if curx + 1 < self.x:
                    queue.push([curx + 1, cury])


    def left(self):
        for i in range(self.x, 2, -1):
            for j in range(self.y, 2, -1):
                if self.board[i][j-2] == self.board[i][j] and self.board[i][j-1] > 0:
                    self.board[i][j-2] *= 3
                    self.score += self.board[i][j-2]
                    self.board[i][j] = 0
                    
        queue = queue_object()
        for i in range(1, self.y + 1):
            for j in range(1, self.x + 1):
                if self.board[i][j] > 0:
                    queue.push([i, j])
        
        while queue.size() > 0:
            f = queue.front()
            curx = f[0]
            cury = f[1]
            if (cury == 1):
                continue
            if (self.board[curx][cury - 1] == 0):
                self.board[curx][cury - 1] = self.board[curx][cury]
                self.board[curx][cury] = 0
                if cury-1 > 1:
                    queue.push([curx, cury - 1])

                    
    def right(self):
        for i in range(1, self.y - 1):
            for j in range(1, self.x - 1):
                if self.board[i][j+2] == self.board[i][j] and self.board[i][j+1] > 0:
                    self.board[i][j+2] *= 3
                    self.score += self.board[i][j+2]
                    self.board[i][j] = 0

        queue = queue_object()
        for i in range(1, self.y + 1):
            for j in range(1, self.x + 1):
                if self.board[i][j] > 0:
                    queue.push([i, j])
        
        while queue.size() > 0:
            f = queue.front()
            curx = f[0]
            cury = f[1]
            if cury == self.y:
                continue
            if self.board[curx][cury+1] == 0:
                self.board[curx][cury+1] = self.board[curx][cury]
                self.board[curx][cury] = 0
                if 10 > cury + 1:
                    queue.push([curx, cury+1])


    """
    self.x = random.randint(0, 9)
    self.y = random.randint(0, 9)

    while (gamer.board[self.x][self.y] > 0):
    self.x = random.randint(0, 9)
    self.y = random.randint(0, 9)
    """

    def a(self):
        for x in self.board:
            print(x)

game = gamer()
game.spawn()
game.a()
# main code
done = False
while not done:

    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.up()
                print()
                game.a()
            if event.key == pygame.K_DOWN:
                game.down()
                print()
                game.a()
            if event.key == pygame.K_LEFT:
                game.left()
                print()
                game.a()
            if event.key == pygame.K_RIGHT:
                game.right()
                print()
                game.a()
            if event.key == pygame.K_ESCAPE:
                ... 
        
        if (game.spawn() == 1):
            game.state = "gameover"
            break

    text_game_over = font.render("Game Over", True, white)
    text_game_over1 = font.render("Press ESC", True, white)

    screen.blit(text, [0, 0])

    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    game.draw_board()
    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

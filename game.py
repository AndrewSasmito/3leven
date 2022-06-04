import pygame
import random
import sys
from pygame.locals import  *



# initializing
pygame.init()
pygame.font.init()
pygame.display.set_caption("3eleven")
clock = pygame.time.Clock()
fps = 30

# colours
black = (0, 0, 0)
white = (255, 255, 255)
purple = [(227, 159, 246), (164, 94, 229), (152, 103, 197), (163, 44, 196), (122, 73, 136), (113, 1, 147)]
colour = random.choice(purple)

# sizes
screen_size = (850, 500) # width x height
screen = pygame.display.set_mode(screen_size)
board_dimension = 9

# other
font = pygame.font.SysFont('Comic Sans', 60)
small_font = pygame.font.SysFont('Comic Sans', 20)
text_title = font.render('3eleven', False, colour)
text_score = font.render('Score', False, colour)

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
        screen.blit(text_title, (150, 10))
        screen.blit(text_score, (500, 20))
        screen.blit(font.render(str(self.score), False, colour), (500, 80))
        # top left corner: 100, 100
        # each cell: 50 * 50
        for i in range(self.x + 1):
            pygame.draw.line(screen, random.choice(purple), (i * 50 + 100, 100), (i * 50 + 100, 100 + (self.x) * 50), 3)
        for i in range(self.y + 1):
            pygame.draw.line(screen, random.choice(purple), (100, i * 50 + 100), (100 + (self.y) * 50, i * 50 + 100), 3)
        
        for i in range(1, self.y + 1):
            for j in range(1, self.x + 1):
                screen.blit(small_font.render(str(self.board[j][i]), False, purple[0]), (i * 50 + 70, j * 50 + 50))
    
    def spawn(self):

        option = []

        for i in range (1, self.x + 1):
            for j in range (1, self.y + 1):
                if self.board[i][j] == 0:
                    option.append([i, j])
                if self.board[i][j] == 177147:
                    self.state = "gameover"
                    return 1

        if len(option) == 0:
            self.state = "gameover"
            return 1
        
        spot = random.choice(option)
        self.board[spot[0]][spot[1]] = random.choice([3, 9])
        return 0
    
    def up(self):
        for i in range(self.y, 3, -1):
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
        for i in range(1, self.y - 2):
            for j in range(1, self.x + 1):
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
        for i in range(1, self.y + 1):
            for j in range(self.x, 3, -1):
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
        for i in range(1, self.y + 1):
            for j in range(1, self.x - 2):
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

    def debug(self):
        for x in self.board:
            print(x)

game = gamer()
game.spawn()
game.debug()
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
                game.debug()
            if event.key == pygame.K_DOWN:
                game.down()
                print()
                game.debug()
            if event.key == pygame.K_LEFT:
                game.left()
                print()
                game.debug()
            if event.key == pygame.K_RIGHT:
                game.right()
                print()
                game.debug()
            if event.key == pygame.K_ESCAPE:
                ... 
        
            if game.spawn() == 1:
                game.state = "gameover"
                break

    text_game_over = font.render("Game Over", True, colour)
    text_game_over1 = font.render("Press ESC", True, colour)

    if game.state == "gameover":
        screen.blit(text_game_over, [500, 200])
        screen.blit(text_game_over1, [500, 265])

    game.draw_board()
    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

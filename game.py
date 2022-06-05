import pygame
import random
import sys
from pygame.locals import  *



# initializing
pygame.init()
pygame.font.init()
pygame.mixer.init()
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
font = pygame.font.SysFont('Comic Sans', 80)
text_title_1 = font.render('3', False, colour)
text_title_2 = font.render('eleven', False, colour)
score_font = pygame.font.SysFont('Comic Sans', 20)
text_score = score_font.render('Score', False, colour)

#Self-made queue
class queue_object:
    def __init__(self):
        self.q = []

    def push(self, value):
        self.q.append(value)

    def front(self):
        return self.q.pop(0)

    def size(self):
        return len(self.q)


# Game class
class the_game:

    #initializing
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "start"
        self.x = 6
        self.y = 6
        self.board = [[0 for _ in range(self.x + 1)] for _ in range(self.x + 1)]
        self.tile = None


    #Drawing the board
    def draw_board(self):
        screen.blit(text_title_1, (500, 200))
        screen.blit(text_title_2, (550, 150))
        screen.blit(text_score, (200, 50))
        screen.blit(score_font.render(str(self.score), False, colour), (280, 50))
        screen.blit(pygame.font.SysFont('Comic Sans', 15).render('Press ESC to restart', False, colour), (580, 260))
        # top left corner: 100, 100
        # each cell: 50 * 50
        for i in range(self.x + 1):
            pygame.draw.line(screen, random.choice(purple), (i * 50 + 100, 100), (i * 50 + 100, 100 + (self.x) * 50), 4)
        for i in range(self.y + 1):
            pygame.draw.line(screen, random.choice(purple), (100, i * 50 + 100), (100 + (self.y) * 50, i * 50 + 100), 4)
        
        for i in range(1, self.y + 1):
            for j in range(1, self.x + 1):
                number_font = pygame.font.SysFont('Comic Sans', 20)
                if self.board[j][i] == 0:
                    number_font = pygame.font.SysFont('Comic Sans', 0)
                if self.board[j][i] > 1000:
                    number_font = pygame.font.SysFont('Comic Sans', 15)
                if self.board[j][i] > 10000:
                    number_font = pygame.font.SysFont('Comic Sans', 10)
                grid_number = number_font.render(str(self.board[j][i]), False, colour)
                center_number = grid_number.get_rect(center = (i * 50 + 75, j * 50 + 75))
                screen.blit(grid_number, center_number)


    
    #Checking if the game is over or no
    def checker(self):
        #return 1 if move is possible
        #retun 0 if move is not possible
        for i in range(1, self.x + 1):
            for j in range (1, self.y + 1):
                # check if cell is empty
                if self.board[i][j] == 0:
                    return 1
                # check if up is possible
                if i >= 3:
                    if self.board[i-2][j] == self.board[i][j]:
                        return 1
                # check if down is possible
                if i <= self.x - 2:
                    if self.board[i+2][j] == self.board[i][j]:
                        return 1
                # check if left is possible
                if j >= 3:
                    if self.board[i][j - 2] == self.board[i][j]:
                        return 1
                
                #check if right is possible
                if j <= self.y - 2:
                    if self.board[i][j + 2] == self.board[i][j]:
                        return 1
        return 0

                

    #Spawning in the blocks randomly
    def spawn(self):

        option = []

        for i in range (1, self.x + 1):
            for j in range (1, self.y + 1):
                if self.board[i][j] == 0:
                    option.append([i, j])
                if self.board[i][j] == 177147:
                    self.state = "win"
                    return 1
        
        if self.checker() == 0:
            self.state = "gameover"
            return 1

        if len(option) != 0:
            spot = random.choice(option)
            self.board[spot[0]][spot[1]] = random.choice([3, 9])
        return 0
    
    #When the player presses up
    def up(self):
        for i in range(self.y, 2, -1):
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
                queue.push([curx - 1, cury])

        
    #When the player presses down
    def down(self):
        for i in range(1, self.y - 1):
            for j in range(0, self.x + 1):
                if self.board[i+2][j] == self.board[i][j] and self.board[i+1][j] > 0:
                    self.board[i+2][j] *= 3
                    self.score += self.board[i+2][j]
                    self.board[i][j] = 0
        
        queue = queue_object()
        for i in range(self.x, 0, -1):
            for j in range(self.x, 0, -1):
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
                queue.push([curx + 1, cury])

    #When the player presses left
    def left(self):
        for i in range(1, self.y + 1):
            for j in range(self.x, 2, -1):
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
                queue.push([curx, cury - 1])

    #When the player presses right
    def right(self):
        for i in range(1, self.y + 1):
            for j in range(1, self.x - 2):
                if self.board[i][j+2] == self.board[i][j] and self.board[i][j+1] > 0:
                    self.board[i][j+2] *= 3
                    self.score += self.board[i][j+2]
                    self.board[i][j] = 0

        queue = queue_object()
        for i in range(self.y, 0, -1):
            for j in range(self.x, 0, -1):
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
                queue.push([curx, cury+1])

    #Debugging the game
    def debug(self):
        for x in self.board:
            print(x)
    
    #Changing the gamestate
    def change_gamestate(self, x):
        f = ["start", "gameover", "win"]
        self.state = f[x]


#Audio
# pygame.mixer.music.load('music.ogg')
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(-1)



game = the_game()
game.spawn()
game.debug()


# main code
done = False

#The start screen
while 1:
    screen.fill(black)
    start_screen_font = pygame.font.SysFont('Comic Sans', 100)
    start_screen_text = start_screen_font.render('UPP Inc', False, colour)
    center_start_screen = start_screen_text.get_rect(center = (screen_size[0] // 2, screen_size[1] // 2))
    screen.blit(start_screen_text, center_start_screen)
    pygame.display.update()
    pygame.display.flip()
    
    pygame.time.delay(2000)
    break



while 1:
    breaker = 0
    screen.fill(purple[1])

    instructions = pygame.image.load('instructions.png')
    screen.blit(instructions, instructions.get_rect(center = (screen_size[0] // 2, screen_size[1] // 2)))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            breaker = 1
            break
    
    if breaker == 1:
        break
    
    
    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)
        
while not done:

    screen.fill(black)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            valid_key = 0
            if event.key == pygame.K_UP or event.key == pygame.K_a:
                game.up()
                print()
                game.debug()
                valid_key = 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                game.down()
                print()
                game.debug()
                valid_key = 1
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                game.left()
                print()
                game.debug()
                valid_key = 1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                game.right()
                print()
                game.debug()
            if event.key == pygame.K_ESCAPE:
                game = the_game()
                valid_key = 1

            if valid_key == 1:
                if game.spawn() == 1:
                    break
    
    game_font = pygame.font.SysFont('comicsansms', 30)
    text_game_over_1 = game_font.render("Game Over", True, colour)
    text_game_over_2 = game_font.render("You Won", True, colour)

    if game.state == "gameover":
        screen.blit(text_game_over_1, text_game_over_1.get_rect(center = (650, 320)))
    if game.state == "win":
        screen.blit(text_game_over_2, text_game_over_2.get_rect(center = (650, 360)))

    game.draw_board()
    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

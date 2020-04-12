import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))

backgroundImage = pygame.image.load('background1.jpg')
gameoverImage = pygame.image.load('GAMEOVER.jpg')
appleImage = pygame.image.load('apple.png')

class Snake:

    def __init__(self):
        self.size = 1
        self.elements = [[100, 100]]
        self.radius = 15
        self.dx = 5  # right
        self.dy = 0
        self.is_add = False

    def draw(self):
        for element in self.elements:
            pygame.draw.circle(screen, (255, 0, 0), element, self.radius)

    def add_to_snake(self):
        self.size += 1
        self.elements.append([0, 0])
        self.is_add = False

    def move(self):
        if self.is_add:
            self.add_to_snake()

        for i in range(self.size - 1, 0, -1):
            self.elements[i][0] = self.elements[i - 1][0]
            self.elements[i][1] = self.elements[i - 1][1]

        self.elements[0][0] += self.dx
        self.elements[0][1] += self.dy

class Apple():
    def __init__(self):
        self.x = random.randint(25, 745)
        self.y = random.randint(25, 545)
        self.rad = 15
    def draw(self):
        screen.blit(appleImage, (self.x, self.y))

snake = Snake()
apple = Apple()
score = 0

def collision():
    if((apple.x >= snake.elements[0][0] - 40 and apple.x <= snake.elements[0][0] + 40) and (apple.y >= snake.elements[0][1] - 40 and apple.y <= snake.elements[0][1] + 40)):
        return True
    return False

def death():
    for i in range (1, len(snake.elements)):
        if(snake.elements[0][0] == snake.elements[i][0] and snake.elements[0][1] == snake.elements[i][1]):
            return True
    return False 
def death_wall():
    if ((snake.elements[0][0] < 25 or snake.elements[0][0] > 775) or(snake.elements[0][1] < 25 or snake.elements[0][1] > 575)):
        return True
    return False

def scores(x, y):
    shrift = pygame.font.SysFont('times new roman', 25)
    text = shrift.render('SCORE: ' + str(score), True, (255, 0, 0))
    screen.blit(text, (x, y))

def GameOver(x, y):
    screen.blit(gameoverImage, (x, y))

running = True

d = 8

FPS = 30

clock = pygame.time.Clock()

isGameOver = False

while running:
    mill = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_RIGHT:
                snake.dx = d
                snake.dy = 0
            if event.key == pygame.K_LEFT:
                snake.dx = -d
                snake.dy = 0
            if event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -d
            if event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = d

    pressed = pygame.key.get_pressed()
    coll = collision()
    dead = death()
    d_w = death_wall()
    if coll:
        snake.is_add = True
        apple.x = random.randint(25, 745)
        apple.y = random.randint(25, 545)
        score += 1
    
    if (dead == True) or (d_w == True):
        isGameOver = True
        screen.blit(gameoverImage, (0, 0))

    if not isGameOver:
        screen.blit(backgroundImage, (0, 0))
        snake.move()
        screen.fill((0, 0, 0))
        apple.draw()
        snake.draw()
        scores(670, 0)
        pygame.display.flip()

pygame.quit()
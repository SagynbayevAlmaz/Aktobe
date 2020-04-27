import pygame
import time
import random


pygame.init()
screen = pygame.display.set_mode((900,700))

backgroundImage = pygame.transform.scale(pygame.image.load('pic/background.jpg'), (900, 700))
life_img1 = pygame.image.load('pic/life_red.png')
life_img2 = pygame.image.load('pic/life_blue.png')


class Direction:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Tank:

    def __init__(self, x, y, speed, color,life_img, life_pos, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN):
        self.x = x
        self.y = y
        self.life = 4
        self.color = color
        self.life = 3
        self.life_img = life_img
        self.life_pos = life_pos
        self.speed = speed
        self.width = 50
        self.direction = 0 #random.randint(1, 4)
        
        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN}
    
    def draw(self):
        tank_c = (self.x + int(self.width/2), self.y + int(self.width/2))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width), 7)
        pygame.draw.circle(screen, self.color, tank_c, int(self.width/2), 13)

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width + int(self.width/2), self.y + int(self.width / 2)), 8)
        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (self.x - int(self.width/2), self.y + int(self.width / 2)), 8)
        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width/2), self.y - int(self.width / 2)), 8)
        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width/2), self.y + self.width + int(self.width / 2)), 8)  
    
    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed

        if self.y < 0:
            self.y = 700
        if self.y > 700:
            self.y = 0
        if self.x < 0:
            self.x = 900
        if self.x > 900:
            self.x = 0
        
        self.draw()
        
    def life_draw(self):
        for i in range(self.life):
            screen.blit(self.life_img, (self.life_pos[0] + (26 * i), self.life_pos[1]))

class Bullet:

    def __init__(self, x, y, colour, sx, sy):
        self.x = x
        self.y = y
        self.colour = colour
        self.radius = 6
        self.speedx = sx
        self.speedy = sy

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius)
    
    def move(self):
        
        self.x += self.speedx
        self.y += self.speedy

        self.draw()

r = random.randint(0, 255)
g = random.randint(0, 255)
b = random.randint(0, 255)


FPS = 30
clock = pygame.time.Clock()

tank1 = Tank(200, 300, 5, (255, 0, 0), life_img2, (805, 20))
tank2 = Tank(500, 300, 5, (0, 0, 255), life_img1, (20, 20), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
tanks = [tank1, tank2]
bullets = []

sound1 = pygame.mixer.Sound('sound/shoot.mp3')
sound2 = pygame.mixer.Sound('sound/hit.wav')

run = True 
isGameOver1 = False
isGameover2 = False
while run:
    mill = clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key in tank1.KEY.keys():
                tank1.change_direction(tank1.KEY[event.key])
            if event.key in tank2.KEY.keys():
                tank2.change_direction(tank2.KEY[event.key])

            if event.key == pygame.K_RETURN:
                sound1.play()
                if tank1.direction == Direction.LEFT:
                    bullet = Bullet(tank1.x - 20, tank1.y + 20, (r, g, b), -10, 0)
                if tank1.direction == Direction.RIGHT:
                    bullet = Bullet(tank1.x + 60, tank1.y + 20, (r, g, b), 10, 0)
                if tank1.direction == Direction.UP:
                    bullet = Bullet(tank1.x + 20, tank1.y - 20, (r, g, b), 0, -10)
                if tank1.direction == Direction.DOWN:
                    bullet = Bullet(tank1.x + 20, tank1.y + 60, (r, g, b), 0, 10)
                bullets.append(bullet)

            if event.key == pygame.K_SPACE:
                sound1.play()
                if tank2.direction == Direction.LEFT:
                    bullet = Bullet(tank2.x - 20, tank2.y + 20, (r, g, b), -12, 0)
                if tank2.direction == Direction.RIGHT:
                    bullet = Bullet(tank2.x + 60, tank2.y + 20, (r, g, b), 12, 0)
                if tank2.direction == Direction.UP:
                    bullet = Bullet(tank2.x + 20, tank2.y - 20, (r, g, b), 0, -12)
                if tank2.direction == Direction.DOWN:
                    bullet = Bullet(tank2.x + 20, tank2.y + 60, (r, g, b), 0, 12)
                bullets.append(bullet)
    
    for b in bullets:
        if b.x < 0 or b.x > 800 or b.y < 0 or b.y > 600:
            bullets.pop(0)
    
        if b.x in range(tank2.x, tank2.x + 40) and b.y in range(tank2.y, tank2.y + 40):
            sound2.play()
            bullets.pop(0)
            tank1.life -= 1
        if b.x in range(tank1.x, tank1.x + 40) and b.y in range(tank1.y, tank1.y + 40):
            sound2.play()
            bullets.pop(0)
            tank2.life -= 1           
    
    if tank1.life == 0 or tank2.life == 0:
        run = False
    if tank1.life == 0:
        isGameOver1 = True
    
    if tank2.life == 0:
        isGameOver2 = True

    if not (isGameOver1 and isGameOver2)
    screen.blit(backgroundImage, (0, 0))
    tank1.move()
    tank2.move()
    tank1.life_draw()
    tank2.life_draw()
    for bullet in bullets:
        bullet.move()
    pygame.display.flip()

pygame.quit()
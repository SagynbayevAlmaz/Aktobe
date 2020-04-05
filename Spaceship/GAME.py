import pygame
import random 

pygame.init()

screen = pygame.display.set_mode((1000, 750))

done = False

backgroundImage = pygame.image.load("Space1.jpg")
gameoverImage = pygame.image.load("GAMEOVER.jpg")

playerImage = pygame.image.load("spaceship.png")

player_x = 500
player_y = 650

enemyImage = pygame.image.load("Alien.png")

enemy_x = random.randint(0, 920)
enemy_y = random.randint(20, 50)

enemy_dx = 3
enemy_dy = 10

bulletImage = pygame.image.load("Bullet1.png")
bullet_x = 0
bullet_y = 750
bullet_dy = 10

score = 0
shoot = False
hit = False
isGameOver = False

def player(x, y):
    screen.blit(playerImage, (x, y))

def enemy(x, y):
    screen.blit(enemyImage, (x, y))

def bullet(x, y):
    screen.blit(bulletImage, (x, y))

def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    if (bullet_x >= enemy_x and bullet_x <= enemy_x + 80) and (bullet_y <= enemy_y + 100):
        return True
    return False

def death(player_x, player_y, enemy_x, enemy_y):
    if(player_x >= enemy_x and player_x  <= enemy_x + 80) and (player_y <= enemy_y + 90):
        return True
    return False

def scores(x, y):
    shrift = pygame.font.SysFont('times new roman', 25)
    text = shrift.render('SCORE: ' + str(score), True, (255, 0, 0))
    screen.blit(text, (x, y))

def GameOver():
    screen.blit(gameoverImage, (0, 0))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_LEFT] and player_x > 0: 
        player_x -= 3
    
    if pressed[pygame.K_RIGHT] and player_x < 930: 
        player_x += 3
    
    enemy_x += -enemy_dx
    if enemy_x < 0 or enemy_x > 920:
        enemy_dx = -enemy_dx
        enemy_y += enemy_dy

    if pressed[pygame.K_SPACE] and shoot is False:
        bullet_x = player_x + 30
        bullet_y = player_y
        shoot = True
    
    coll = collision(enemy_x, enemy_y, bullet_x, bullet_y)

    if coll is True:
        bullet_x = 0
        bullet_y = 750
        enemy_x, enemy_y = random.randint(0, 920) , random.randint(20, 50)
        shoot = False
        hit = True
    
    if hit is True:
        score += 1
        hit = False

    if bullet_y < 0:
        bullet_x = 0
        bullet_y = 750
        shoot = False
    
    if shoot is not False:
        bullet_y -= bullet_dy
    
    dying = death(player_x, player_y, enemy_x, enemy_y)

    if dying:
        isGameOver = True
        GameOver()
        if pressed[pygame.K_TAB]:
            isGameOver = False
            enemy_x, enemy_y = random.randint(0, 920) , random.randint(20, 50)
            score = 0
    
    if not isGameOver:
        screen.blit(backgroundImage, (0, 0))
        player(player_x, player_y)
        enemy(enemy_x, enemy_y)
        bullet(bullet_x, bullet_y)
        scores(870, 0)
        pygame.display.flip()

pygame.quit()
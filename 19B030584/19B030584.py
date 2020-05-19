import pygame
from enum import Enum
import sys
import math
import pika
import uuid
import json
import time
import random
from threading import Thread

pygame.init()

screen = pygame.display.set_mode((1000, 600))

menu_background = pygame.transform.scale(pygame.image.load('pic/menu_back.jpg'), (1000, 600))
grass = pygame.transform.scale(pygame.image.load('pic/grass.jpg'), (100, 100))
life_img1 = pygame.image.load('pic/life_red.png')
life_img2 = pygame.image.load('pic/life_blue.png')
wall_image = pygame.transform.scale(pygame.image.load('pic/wall.jpg'), (50, 50))
end_image = pygame.transform.scale((pygame.image.load('pic/multi_end.jpg')), (1000, 600))

tank_image =  pygame.transform.scale(pygame.image.load('pic/my_tank.png'), (31, 31))
enemy_image = pygame.transform.scale(pygame.image.load('pic/enemy_tank.png'), (31, 31))

menu_font1 =pygame.font.SysFont('Times New Roman', 85)
menu_font2 =pygame.font.SysFont('Times New Roman', 50)
###########################SINGLE############################
def sp():
    pygame.init()

    screen = pygame.display.set_mode((1000, 600))
    def background():
        for i in range(0, 900, 100):
            for j in range(0, 700, 100):
                screen.blit(grass, (i, j))

    
    FPS = 30
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    second = 0
    current_time = 0
    power_time = 0
    possiblity = random.randint(0, 15)

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

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
            pygame.draw.circle(screen, self.color, tank_c, int(self.width//2), 13)

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
                self.y = 600
            if self.y > 600:
                self.y = 0
            if self.x < 0:
                self.x = 1000
            if self.x > 1000:
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
            pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)
        
        def move(self):
            bul_vel = self.speedx
            bul_vel = self.speedy
            self.x += self.speedx
            self.y += self.speedy

            self.draw()

    class Bonus():

        def __init__(self):
            self.x = random.randint(100, 800)
            self.y = random.randint(100, 600)
            self.radius = 9
            self.colour = (r, g, b)
        def draw(self):
            pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)

    bonus = Bonus()
    def spawn():
        if second >= possiblity:
            bonus.draw()

    def draw_wall():
        for i in coord:
            screen.blit(wall_image, i)

    bul_vel = 15

    tank1 = Tank(200, 300, 5, (255, 0, 0), life_img1, (20, 20))
    tank2 = Tank(650, 300, 5, (0, 0, 255), life_img2, (805, 20), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)

    bullets = []

    coord = [(10, 50), (60, 50), (110, 50), (160, 50), (10, 50), (10, 100), (300, 125), (350, 125), (400, 125), (450, 125), (500, 125), (550, 125), (300, 175), (300, 225),(300, 275), (300, 325), (350, 325), (400, 325), (450, 325), (500, 325), (550, 325), (550, 175),(550, 225), (550, 275), (550, 325), (700, 400), (700, 450), (750, 400), (750, 450) ]

    sound1 = pygame.mixer.Sound('sound/shoot.mp3')
    sound2 = pygame.mixer.Sound('sound/hit.wav')

    isGameOver = False

    Single = True
    font = pygame.font.SysFont('Times New Roman', 25)
    while Single:
        mill = clock.tick(FPS)
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Single = False
            if event.type == pygame.USEREVENT:
                second += 1
                #print(second)
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Single = False
                if event.key in tank1.KEY.keys():
                    tank1.change_direction(tank1.KEY[event.key])
                if event.key in tank2.KEY.keys():
                    tank2.change_direction(tank2.KEY[event.key])

                if event.key == pygame.K_RETURN:
                    sound1.play()
                    if tank1.direction == Direction.LEFT:
                        bullet = Bullet(tank1.x - 25, tank1.y + 25, (255, 0, 0), -1 * bul_vel, 0)
                    if tank1.direction == Direction.RIGHT:
                        bullet = Bullet(tank1.x + 60, tank1.y + 25, (255, 0, 0), bul_vel, 0)
                    if tank1.direction == Direction.UP:
                        bullet = Bullet(tank1.x + 25, tank1.y - 25, (255, 0, 0), 0, -1 * bul_vel)
                    if tank1.direction == Direction.DOWN:
                        bullet = Bullet(tank1.x + 25, tank1.y + 60, (255, 0, 0), 0, bul_vel)
                    bullets.append(bullet)

                if event.key == pygame.K_SPACE:
                    sound1.play()
                    if tank2.direction == Direction.LEFT:
                        bullet = Bullet(tank2.x - 25, tank2.y + 25, (0, 0, 255), -1*bul_vel, 0)
                    if tank2.direction == Direction.RIGHT:
                        bullet = Bullet(tank2.x + 60, tank2.y + 25, (0, 0, 255), bul_vel, 0)
                    if tank2.direction == Direction.UP:
                        bullet = Bullet(tank2.x + 25, tank2.y - 25, (0, 0, 255), 0, -1*bul_vel)
                    if tank2.direction == Direction.DOWN:
                        bullet = Bullet(tank2.x + 25, tank2.y + 60, (0, 0, 255), 0, bul_vel)
                    bullets.append(bullet)   
    
        current_time = pygame.time.get_ticks()
        #print(current_time)
    
        for bull in bullets:
            if bull.x < 0 or bull.x > 900 or bull.y < 0 or bull.y > 700:
                bullets.pop(0)
    
            if bull.x in range(tank2.x, tank2.x + 50) and bull.y in range(tank2.y, tank2.y + 50):
                sound2.play()
                bullets.pop(0)
                tank2.life -= 1
            if bull.x in range(tank1.x, tank1.x + 50) and bull.y in range(tank1.y, tank1.y + 50):
                sound2.play()
                bullets.pop(0)
                tank1.life -= 1 
            for i in coord:
                if bull.x in range(i[0], i[0] + 50) and bull.y in range(i[1], i[1] + 50):
                    coord.remove(i)
                    bullets.pop(0)

        if (tank2.x <= tank1.x <= tank2.x + 50 or tank1.x <= tank2.x <= tank1.x + 50) and (tank2.y <= tank1.y <= tank2.y + 50 or tank1.y <= tank2.y <= tank1.y + 50):
            tank1.life -= 1
            tank2.life -= 1 
            tank1.x = 10
            tank1.y = 640
            tank2.x = 800
            tank2.y = 10
    
        for i in coord:
            if tank1.x in range(i[0], i[0] + 50) and tank1.y in range(i[1], i[1] + 50):
                coord.remove(i)
                tank1.life -= 1
            if tank2.x in range(i[0], i[0] + 50) and tank2.y in range(i[1], i[1] + 50):
                coord.remove(i)
                tank2.life -= 1
    
        if bonus.x in range(tank1.x , tank1.x + 50) and bonus.y in range(tank1.y, tank1.y + 50):
            for bull in bullets:
                bul_vel = 30
            tank1.speed =tank1.speed * 2
            power_time = pygame.time.get_ticks()
            print(power_time)
            bonus.x = random.randint(100, 800)
            bonus.y = random.randint(100, 600)
            second = 0
            possiblity = random.randint(0, 15)
            #print(possiblity)
    
        if bonus.x in range(tank2.x , tank2.x + 50) and bonus.y in range(tank2.y, tank2.y + 50):
            for bull in bullets:
                bul_vel = 30
            tank2.speed =tank2.speed * 2
            power_time = pygame.time.get_ticks()
            print(power_time)
            bonus.x =random.randint(100, 800)
            bonus.y = random.randint(100, 600)
            second = 0
            possiblity = random.randint(0, 15)
            #print(possiblity)
        
        if current_time - power_time > 5000:
            tank1.speed = 5
            bul_vel = 15

        if current_time - power_time > 5000:
            tank2.speed = 5
            bul_vel = 15

        if tank1.life == 0:
            isGameOver = True
            screen.blit(end_image, (0, 0))
            text1 = font.render('Blue tank won!', True, (255, 255, 0))
            text2 = font.render('Press R to Restart', True, (255, 255, 0))
            screen.blit(text1, (475, 200))
            screen.blit(text2, (450, 250))
            pygame.display.update()
        
        if tank2.life == 0:
            isGameOver = True
            screen.blit(end_image, (0, 0))
            text3 = font.render('Red tank won!', True, (255, 255, 0))
            text4 = font.render('Press R to Restart', True, (255, 255, 0))
            screen.blit(text3, (475, 200))
            screen.blit(text4, (450, 250))
            pygame.display.update()
        
        if isGameOver:
            if pressed[pygame.K_r]:
                isGameOver = False
                tank1.life = 3
                tank2.life = 3
                tank1.x, tank1.y = 200, 300
                tank2.x, tank2.y = 650, 300
                tank1.direction = 0
                tank2.direction = 0
    
        if not isGameOver:
            #screen.blit(backgroundImage, (0, 0))
            background()
            tank1.move()
            tank2.move()
            tank1.life_draw()
            tank2.life_draw()
            spawn()
            draw_wall()
            for bullet in bullets:
                bullet.move()
            # tank_wall(tank1)
            # tank_wall(tank2)
            pygame.display.flip()


######################MULTI###################
IP = '34.254.177.17'
PORT = 5672
VIRTUAL_HOST = 'dar-tanks'
USERNAME = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'


class TankRpcClient:
    def __init__(self):
        self.connection  = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,                                          
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()                      
        queue = self.channel.queue_declare(queue='',exclusive=True,auto_delete=True)  
        self.callback_queue = queue.method.queue                  
        self.channel.queue_bind(exchange='X:routing.topic',queue=self.callback_queue)
        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True) 
    
        self.response= None    
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            print(self.response)

    def call(self, key, message={}):     
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message) 
        )
        while self.response is None:
            self.connection.process_data_events()

    def check_server_status(self): 
        self.call('tank.request.healthcheck')
        return self.response['status']== '200' 

    def obtain_token(self, room_id):
        message = {
            'roomId': room_id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']
            return True
        return False

    def turn_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def fire_bullet(self, token):
        message = {
            'token': token
        }
        self.call('tank.request.fire', message)

class TankConsumerClient(Thread):

    def __init__(self, room_id):
        super().__init__()
        self.connection  = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,                                                
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()                      
        queue = self.channel.queue_declare(queue='',exclusive=True,auto_delete=True)
        event_listener = queue.method.queue
        self.channel.queue_bind(exchange='X:routing.topic',queue=event_listener,routing_key='event.state.'+room_id)
        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        print(self.response)

    def run(self):
        self.channel.start_consuming()

def mp():
    
    
    pygame.init()

    screen = pygame.display.set_mode((1000, 600))
    
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

    MOVE_KEYS = {
        pygame.K_w: UP,
        pygame.K_a: LEFT,
        pygame.K_s: DOWN,
        pygame.K_d: RIGHT
    }

    tank_image =  pygame.transform.scale(pygame.image.load('pic/my_tank.png'), (31, 31))
    enemy_image = pygame.transform.scale(pygame.image.load('pic/enemy_tank.png'), (31, 31))

    def draw_tank(id, x, y,  direction):
        font = pygame.font.SysFont('Times New Roman', 16)
        text_id = font.render(id, True, (255, 255, 0))
        screen.blit(text_id,(x-10, y-20))
        if direction == 'UP':
            screen.blit(tank_image, (x, y))
        if direction == 'DOWN':
            screen.blit(pygame.transform.rotate(tank_image, 180), (x, y))
        if direction == 'RIGHT':
            screen.blit(pygame.transform.rotate(tank_image, -90), (x, y))
        if direction == 'LEFT':
            screen.blit(pygame.transform.rotate(tank_image, 90), (x, y))

    def draw_enemy(id, x, y,  direction):
        font = pygame.font.SysFont('Times New Roman', 16)
        text_id_enemy = font.render(id, True, (255, 255, 0))
        screen.blit(text_id_enemy,(x-10, y-20))
        if direction == 'UP':
            screen.blit(enemy_image, (x, y))
        if direction == 'DOWN':
            screen.blit(pygame.transform.rotate(enemy_image, 180), (x, y))
        if direction == 'RIGHT':
            screen.blit(pygame.transform.rotate(enemy_image, -90), (x, y))
        if direction == 'LEFT':
            screen.blit(pygame.transform.rotate(enemy_image, 90), (x, y))

    def draw_bullet(colour, x, y, width, height):
        pygame.draw.rect(screen, colour, (x, y, width, height))

    
    def mp_loop():
        mainloop = True
        font = pygame.font.SysFont('Times New Roman', 16)
        while mainloop:
            screen.fill((0, 0, 0))
            #pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False
                    if event.key in MOVE_KEYS:
                        client.turn_tank(client.token, MOVE_KEYS[event.key])
                    if event.key == pygame.K_SPACE:
                        client.fire_bullet(client.token)

            kicked = event_client.response['kicked']
            winners = event_client.response['winners']
            losers  = event_client.response['losers']
    
            try:
                remaining_time = event_client.response['remainingTime']
                text_time = font.render("Remaining Time: " + str(remaining_time), True, (220, 20, 60))
                screen.blit(text_time, (840, 10))
                pygame.draw.line(screen, (255,215,0), (825, 0), (825, 600), 3)
                # pygame.draw.rect(screen, (255, 255, 255), (850, 39, 80, 23), 2)
                # pygame.draw.rect(screen, (255, 255, 255), (843, 111, 108, 25), 2)
                bullets = event_client.response['gameField']['bullets']
                tanks = event_client.response['gameField']['tanks']

                for tank in tanks:
                    tank_id = tank['id']
                    tank_score = tank['score']
                    tank_health = tank['health']
                    tank_x = tank['x']
                    tank_y = tank['y']
                    tank_direction = tank['direction']
                    if tank_id == client.tank_id:
                        draw_tank('You', tank_x, tank_y, tank_direction)
                    else:
                        draw_enemy(tank_id, tank_x, tank_y, tank_direction)
                
                for bullet in bullets:
                    bullet_x = bullet['x']
                    bullet_y = bullet['y']
                    bullet_width = bullet['width']
                    bullet_height = bullet['height']
                    if bullet['owner'] == client.tank_id:
                        draw_bullet((255, 0, 0), bullet_x, bullet_y, bullet_width, bullet_height)
                    else:
                        draw_bullet((0, 0, 255), bullet_x, bullet_y, bullet_width, bullet_height)
                
                scores = {tank['id']: [tank['score'], tank['health']] for tank in tanks}
                sorted_scores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
                i = 100
                for score in sorted_scores:
                    if score[0] == client.tank_id: color = (0, 153, 20)
                    else: color = (176, 0, 0)
                    health_score = font.render(score[0] + ':    ' + str(score[1][0]) + '    ' +
                                                                str(score[1][1]), True, color)
                    health_scoreRect = health_score.get_rect()
                    health_scoreRect.center = (920, i)
                    screen.blit(health_score, health_scoreRect)
                    i += 30
            except Exception as e:
                pass


            font2 = pygame.font.SysFont('Times New Roman', 25)
            for tank in winners:
                if client.tank_id == tank['tankId']:
                    screen.blit(end_image, (0, 0))
                    text1 = font2.render('You won!', True, (0, 255, 0))
                    text2 = font2.render('Your score is:' + ' ' + str(tank['score']), True, (0, 255, 0))
                    screen.blit(text1, (500, 200))
                    screen.blit(text2, (490, 230))
                    pygame.display.flip()
                    time.sleep(7)
                    mainloop = False
                    menu()
            
            for tank in kicked:
                if client.tank_id == tank['tankId']:
                    screen.blit(end_image, (0, 0))
                    text1 = font2.render('You have been kicked for AFK', True, (0, 255, 0))
                    text2 = font2.render('Your score is:' + ' ' + str(tank['score']), True, (0, 255, 0))
                    screen.blit(text1, (500, 200))
                    screen.blit(text2, (490, 230))
                    pygame.display.flip()
                    time.sleep(7)
                    mainloop = False
                    menu()
            
            for tank in losers:
                if client.tank_id == tank['tankId']:
                    screen.blit(end_image, (0, 0))
                    text1 = font2.render('You lose (', True, (0, 255, 0))
                    text2 = font2.render('Your score is:' + ' ' + str(tank['score']), True, (0, 255, 0))
                    screen.blit(text1, (500, 200))
                    screen.blit(text2, (490, 230))
                    pygame.display.flip()
                    time.sleep(7)
                    mainloop = False
                    menu()

            pygame.display.flip()

        client.connection.close()
        event_client.channel.stop_consuming()
        pygame.quit()

    client = TankRpcClient()
    client.check_server_status()
    client.obtain_token('room-5')
    event_client = TankConsumerClient('room-5')
    event_client.start()
    mp_loop()

############################AI#####################

########################MAIN MENU#######################

def menu():
    screen = pygame.display.set_mode((1000, 600))
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    sp()
                if event.key == pygame.K_m:
                    mp()
        
        screen.blit(menu_background, (0, 0))
        text1 = menu_font1.render('BATTLE CITY', True, (255, 255, 255))
        text2 = menu_font2.render('Press S to play SinglePlayer', True, (255, 255, 255))
        text3 = menu_font2.render('Press M to play MultiPlayer', True, (255, 255, 255))
        text4 = menu_font2.render('Press A to play AI', True, (255, 255, 255))
        screen.blit(text1, (265, 50))
        screen.blit(text2, (260, 225))
        screen.blit(text3, (260, 300))
        screen.blit(text4, (350, 375))

        pygame.display.update()

menu()

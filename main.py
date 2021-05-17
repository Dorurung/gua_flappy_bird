import pygame, random
import socket               # Import socket module

pygame.init()

size = width, height = 1280, 720
gua_speed = [0, 0.0]
background_speed = [-1, 0]
wall_speed = [-2, 0]
black = 0, 0, 0
wall_gen = 0

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('맑은 고딕', 30)
myfont2 = pygame.font.SysFont('맑은 고딕', 100)

screen = pygame.display.set_mode(size)

gua_head = pygame.transform.scale(pygame.image.load('gua_head.png'), (51, 65))
gua_blush = pygame.transform.scale(pygame.image.load('gua_blush.png'), (51, 65))
gua_smile = pygame.transform.scale(pygame.image.load('gua_smile.png'), (51, 65))
background = pygame.transform.scale(pygame.image.load('background.png'), (1280, 720))
background2 = pygame.transform.scale(pygame.image.load('background.png'), (1280, 720))
wall_head = pygame.image.load('wall_head.png')
wall_body = pygame.image.load('wall_body.png')

gua_face = gua_head

background_rect = background.get_rect()
background_rect2 = background2.get_rect().move([1280, 0])

clock = pygame.time.Clock()
gua_head_rect = gua_head.get_rect()
state = 'gameover'
wall_list = []
difficulty = 0

def gameinit():
    global gua_head_rect
    global score
    global state
    global wall_list
    global difficulty
    global wall_gen
    global gua_speed
    global wall_speed
    gua_head_rect.x = 100
    gua_head_rect.y = 0
    score = 0
    state = 'gamestart'
    wall_list = []
    difficulty = 0
    wall_gen = 100
    gua_speed = [0, 0.0]
    wall_speed = [-2, 0.0]

gameinit()

class Wall():
    def __init__(self, hole_position, hole_height):
        self.image_head2 = pygame.image.load('wall_head.png')
        self.image_body2 = pygame.transform.scale(pygame.image.load('wall_body.png'), (34, hole_position - 91 if hole_position - 91 > 0 else 1))
        self.image_head = pygame.transform.flip(pygame.image.load('wall_head.png'), False, True)
        self.image_body = pygame.transform.scale(pygame.transform.flip(pygame.image.load('wall_body.png'), False, True), (34, 720 - hole_position - hole_height - 91 if 720 - hole_position - hole_height - 91 > 0 else 1))
        self.image_head_rect = self.image_head.get_rect()
        self.image_head_rect.x = 1280
        self.image_head_rect.y = hole_position + hole_height
        self.image_body_rect = self.image_body.get_rect()
        self.image_body_rect.x = 1280
        self.image_body_rect.y = hole_position + hole_height + 91
        self.image_head_rect2 = self.image_head2.get_rect()
        self.image_head_rect2.x = 1280
        self.image_head_rect2.y = hole_position - 91
        self.image_body_rect2 = self.image_body2.get_rect()
        self.image_body_rect2.x = 1280
        self.image_body_rect2.y = 0
        self.image_list = [(self.image_head, self.image_head_rect), (self.image_head2, self.image_head_rect2), (self.image_body, self.image_body_rect), (self.image_body2, self.image_body_rect2)]
    
    def move(self, delta):
        for _, rect in self.image_list:
            rect.move_ip(delta)
    
    def blit(self, screen):
        for image, rect in self.image_list:
            screen.blit(image, rect)
    
    def collide_detect(self, player):
        for _, rect in self.image_list:
            if player.colliderect(rect):
                return True
        return False


while 1:
    clock.tick(60)
    if state == 'gamestart':
        score += 1 * (difficulty+1)
        wall_gen += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.close
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gua_speed[1] = -7.5
                if event.key == pygame.K_RETURN:
                    if difficulty < 5:
                        difficulty += 1
        
        wall_speed = [-2 - difficulty, 0]
        background_speed = [(-2 - difficulty) * 0.5, 0]

        if score > 1000 and difficulty < 1:
            difficulty = 1
        if score > 3000 and difficulty < 2:
            difficulty = 2
        if score > 6000 and difficulty < 3:
            difficulty = 3
        if score > 10000 and difficulty < 4:
            difficulty = 4
        if score > 15000 and difficulty < 5:
            difficulty = 5
        

        gua_head_rect = gua_head_rect.move(gua_speed)
        if gua_speed[1] < 0:
            gua_face = gua_smile
        else:
            gua_face = gua_head
        background_rect = background_rect.move(background_speed)
        background_rect2 = background_rect2.move(background_speed)
        if background_rect.x < -1280:
            background_rect.move_ip([2560, 0])
        if background_rect2.x < -1280:
            background_rect2.move_ip([2560, 0])
        gua_speed[1] += 0.25

        if wall_gen > 20 * (5 - difficulty) + 70:
            wall_gen = 0
            wall_list.append(Wall(random.randint(10, 510 - (6 - difficulty) * 20), 200 + (6 - difficulty) * 20))

        for wall_instance in wall_list:
            wall_instance.move(wall_speed)
            if wall_instance.collide_detect(gua_head_rect):
                state = 'gameover'
            if wall_instance.image_head_rect.x < -34:
                wall_list.remove(wall_instance)

        if gua_head_rect.y > 720 or gua_head_rect.y < -gua_head_rect.height:
            state = 'gameover'
        
        if state == 'gameover':
            try:
                s = socket.socket()         # Create a socket object
                host = '119.202.82.135' # Get local machine name
                port = 12345                # Reserve a port for your service.
                s.connect((host, port))
                s.send(str(score).encode())
                leaderscore = s.recv(1024).decode()
                s.close()                     # Close the socket when done
            except Exception as e:
                print(e)
                leaderscore = None

    elif state == 'gameover':
        gua_face = gua_blush
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameinit()

    screen.blit(background, background_rect)
    screen.blit(background2, background_rect2)
    screen.blit(gua_face, gua_head_rect)
    for wall_instance in wall_list:
        wall_instance.blit(screen)
    textsurface = myfont.render(f'SCORE: {score}', False, (0, 0, 0))
    screen.blit(textsurface, (10, 10))
    textsurface = myfont.render(f'DIFFICULTY: {difficulty + 1 if difficulty < 5 else "MAX"}', False, (0, 0, 0))
    screen.blit(textsurface, (10, 30))
    textsurface = myfont.render(f'CONTROL: SPACE - JUMP, ENTER - INCREASE DIFFICULTY', False, (0, 0, 0))
    screen.blit(textsurface, (10, 50))
    if state == 'gameover':
        textsurface2 = myfont2.render(f'GAME OVER', False, (0, 0, 0))
        screen.blit(textsurface2, (400, 300))
        textsurface = myfont.render(f'RESTART: ENTER', False, (0, 0, 0))
        screen.blit(textsurface, (505, 400))
        if leaderscore != None:
            leaderstring = 'RANKING'
            textsurface = myfont.render(leaderstring, False, (0, 0, 0))
            screen.blit(textsurface, (1000, 100))
            for rank, scores in enumerate([int(str) for str in leaderscore.split()]):
                leaderstring = f'{rank+1}. {scores}'
                textsurface = myfont.render(leaderstring, False, (0, 0, 0))
                screen.blit(textsurface, (1000, 120+rank*20))
    pygame.display.flip()
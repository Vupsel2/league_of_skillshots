import pygame
import random
import math

pygame.init()
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
FPS = pygame.time.Clock()

HEIGHT = 900
WIDTH = 1350

THRESHOLD_DISTANCE=15
COLOR_WHITE=(0,0,0)




main_display = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.SysFont('arial', 36)
bg=pygame.transform.scale(pygame.image.load('BG.png') , (WIDTH,HEIGHT))
last_direction_vector = pygame.math.Vector2(0, 0)


player_size = (60, 80)
player = pygame.Surface(player_size)

player.fill((240, 248, 255))
bonus_image = pygame.transform.scale(pygame.image.load('Manik.png'), (70, 55))

def create_bonus():
    bonus_size = (70, 55)
    bonus_rect = pygame.Rect(random.randrange(0, HEIGHT), random.randrange(0, WIDTH), *bonus_size)
    
    return {'surface': bonus_image, 'rect': bonus_rect}

    
def create_laser():
    sides = ['top', 'bottom', 'left', 'right']
    sidestart = random.choice(sides)

    if sidestart == 'top':
        start_point = (random.randrange(50, WIDTH-50), 0)
    elif sidestart == 'bottom':
        start_point = (random.randrange(50, WIDTH-50), HEIGHT)
    elif sidestart == 'left':
        start_point = (0, random.randrange(50, HEIGHT-50))
    else:
        start_point = (WIDTH, random.randrange(50, HEIGHT-50))

    direction = random.choice([-1, 1])  # -1 для противоположной стороны, 1 для той же стороны
    if sidestart in ['top', 'bottom']:
        sidestop = random.choice(['left', 'right'])
        stop_point = (0 if sidestop == 'left' else WIDTH, random.randrange(50, HEIGHT-50))
    else:
        sidestop = random.choice(['top', 'bottom'])
        stop_point = (random.randrange(50, WIDTH-50), 0 if sidestop == 'top' else HEIGHT)
        
    return {'start': start_point, 'stop': stop_point, 'creation_time': pygame.time.get_ticks()}



enemy_appear_timer = None  # Таймер появления врага
possible_enemy_speeds = [4, 5, 6, 7]
def create_enemy():
    enemy_size = (90, 60)
    enemy = pygame.Surface(enemy_size)
    side = random.choice(['top', 'bottom', 'left', 'right'])
    
    if side == 'top':
        enemy_rect = pygame.Rect(random.randint(50, WIDTH - enemy_size[0]-50), -enemy_size[1], *enemy_size)
        enemy_move = [random.randrange(-5,5), random.choice(possible_enemy_speeds)]
    elif side == 'bottom':
        enemy_rect = pygame.Rect(random.randint(50, WIDTH - enemy_size[0]-50), HEIGHT, *enemy_size)
        enemy_move = [-random.randrange(-5,5), -random.choice(possible_enemy_speeds)]
    elif side == 'left':
        enemy_rect = pygame.Rect(-enemy_size[0], random.randint(50, HEIGHT - enemy_size[1]-50), *enemy_size)
        enemy_move = [random.choice(possible_enemy_speeds), random.randrange(-5,5)]
    else:
        enemy_rect = pygame.Rect(WIDTH, random.randint(50, HEIGHT - enemy_size[1]-50), *enemy_size)
        enemy_move = [-random.choice(possible_enemy_speeds), -random.randrange(-5,5)]
    return [enemy,enemy_rect, enemy_move]

CREATE_BONUS=pygame.USEREVENT+1
pygame.time.set_timer(CREATE_BONUS,3000)
CREATE_ENEMY=pygame.USEREVENT+2
spawn_timer = 1000
spawn_laser=6000
pygame.time.set_timer(CREATE_ENEMY, spawn_timer)
CREATE_LASER=pygame.USEREVENT+3
pygame.time.set_timer(CREATE_LASER,spawn_laser)


bonuses=[]
enemies=[]
HIT_SPEED=10
PLAYER_SPEED=6
player_rect = player.get_rect()
player_rect.center = (WIDTH // 2, HEIGHT // 2)
playing = True

score=0
image_index= 0
moving_to = None
mouse_held = False

cd_time=0
hit_start_pos = None
hit_distance = 400
hit_out=None
hit_go=None

cdbar_size= (80,20)
cdbar=pygame.Surface(cdbar_size)
cdbar.fill((0, 250, 0))
cdbar_rect=cdbar.get_rect()
# Создание маски для изображения персонажа

lasers=[]

start_time1 = pygame.time.get_ticks()
start_time2 = pygame.time.get_ticks()
start_time3 = pygame.time.get_ticks()
start_time4 = pygame.time.get_ticks()
while playing:
    current_time = pygame.time.get_ticks()
    FPS.tick(240)
   # print(spawn_timer)
    player=pygame.transform.scale(pygame.image.load('Goose.png') , (60,80))
    hit=pygame.transform.scale(pygame.image.load('hit.png') , (40,60))
    player_original_image = player.copy()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             playing = False  
        if event.type== CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
            pygame.time.set_timer(CREATE_ENEMY, spawn_timer)  # Обновляем таймер спавна врагов
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # ПКМ нажата
            moving_to = event.pos  # Запоминаем начальную точку
            mouse_held = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:  # ПКМ отпущена
            mouse_held = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if current_time-cd_time>=3:
                    hit_out=True
                    hit_go=pygame.mouse.get_pos()
                    hit_size = (20, 40)
                    hit_rect = pygame.Rect(player_rect.x, player_rect.y, *hit_size)
                    hit = pygame.Surface(hit_size)
                    cd_time=current_time        
        
            if event.key == pygame.K_s:
                moving_to=None
        if current_time>=50000:
             if event.type == CREATE_LASER:
                 lasers.append(create_laser())
                 pygame.time.set_timer(CREATE_LASER, spawn_laser)
                 
    
        
    if current_time<=50000:
        if (current_time - start_time1) >= 2000:
            spawn_timer -= 25  
            pygame.time.set_timer(CREATE_ENEMY, spawn_timer)
            start_time1 = current_time  
        if (current_time - start_time2) >= 17000:  
            possible_enemy_speeds.append(possible_enemy_speeds[-1]+1)
            start_time2 = current_time 
        if (current_time - start_time3) >= 20000:
            possible_enemy_speeds.pop(0)
            start_time3 = current_time  
    if current_time>=50000:
        if current_time<=60000:
            if (current_time - start_time4) >= 5000:
                spawn_laser -= 500  
                pygame.time.set_timer(CREATE_LASER, spawn_laser)
                start_time4 = current_time
            
            
        
    if hit_go:
        if hit_start_pos is None:
            hit_start_pos = hit_rect.center
            direction_vector1 = pygame.math.Vector2(hit_go[0] - hit_rect.centerx, hit_go[1] - hit_rect.centery)
            if direction_vector1.length_squared() > 0:
                direction_vector1.normalize_ip()
            
        hit_mask = pygame.mask.from_surface(hit)
        hit_orig=hit.copy()
        angle_hit = -math.degrees(math.atan2(direction_vector1.y, direction_vector1.x))
        hit_rect.x += direction_vector1.x * HIT_SPEED
        hit_rect.y += direction_vector1.y * HIT_SPEED
        
        
        distance_traveled = math.sqrt((hit_rect.centerx - hit_start_pos[0])**2 + (hit_rect.centery - hit_start_pos[1])**2)
        if distance_traveled >= hit_distance:
            hit_out = False
            hit_go = None
            hit_start_pos = None
        hit = pygame.transform.rotate(hit_orig, angle_hit)
    
    if mouse_held:
        moving_to = pygame.mouse.get_pos()  # Обновляем точку по позиции курсора

            
    if moving_to:
        # Вычисляем вектор направления движения к точке
         
        direction_vector = pygame.math.Vector2(moving_to[0] - player_rect.centerx, moving_to[1] - player_rect.centery)
        if direction_vector.length_squared() > 0:
            direction_vector.normalize_ip()
        
        angle = -math.degrees(math.atan2(direction_vector.y, direction_vector.x))
        player = pygame.transform.rotate(player_original_image, angle)

        last_direction_vector = direction_vector
        
        # Двигаем персонажа в заданном направлении
        player_rect.x += direction_vector.x * PLAYER_SPEED
        player_rect.y += direction_vector.y * PLAYER_SPEED

        # Проверяем, достиг ли персонаж точки, и сбрасываем moving_to
        distance_to_target = math.sqrt((player_rect.centerx - moving_to[0])**2 + (player_rect.centery - moving_to[1])**2)
        if distance_to_target <= THRESHOLD_DISTANCE:
            moving_to = None
        
        

    
    main_display.blit(bg,(0,0))      
    keys = pygame.key.get_pressed()
    main_display.blit(cdbar, cdbar_rect)
    if hit_out:
        main_display.blit(hit, hit_rect.topleft)
    if current_time>=50000:
        
        for laser in lasers:
            if current_time - laser['creation_time']<=2500:
                color=(255, 102, 0)
            else:
                color=(200, 0, 0)
            pygame.draw.line(main_display, color, laser['start'], laser['stop'], 90)
            if current_time - laser['creation_time'] >= 5000:
                lasers.remove(laser)
    for bonus in bonuses:
        main_display.blit(bonus['surface'], bonus['rect'].topleft)
        bonus_mask = pygame.mask.from_surface(bonus['surface'])
        
    for enemy in enemies:
        
        enemy[0] = pygame.transform.scale(pygame.image.load('enemy1.png'), (90, 60))
        enemy_orig = enemy[0].copy()
        enemy[1] = enemy[1].move(enemy[2])
        
        # Вычисляем угол поворота врага на основе его вектора движения
        vec = pygame.math.Vector2(enemy[2])
        vec.normalize_ip()
        angle_enemy = vec.angle_to(pygame.math.Vector2(1, 0))  # Угол между вектором и направлением (1, 0)
        
        # Поворачиваем изображение врага на вычисленный угол
        enemy[0] = pygame.transform.rotate(enemy_orig, angle_enemy)
        
        main_display.blit(enemy[0], enemy[1].topleft)
        enemy_mask = pygame.mask.from_surface(enemy[0])

    if last_direction_vector.length_squared() > 0.1:
        angle = -math.degrees(math.atan2(last_direction_vector.y, last_direction_vector.x))
        rotated_player = pygame.transform.rotate(player_original_image, angle)
        player_rect = rotated_player.get_rect(center=player_rect.center)
        main_display.blit(rotated_player, player_rect.topleft)
        player_mask = pygame.mask.from_surface(rotated_player)

    else:
        main_display.blit(player_original_image, player_rect.topleft)
        player_mask = pygame.mask.from_surface(player)
        
    
    main_display.blit(font.render(str(score), True, COLOR_WHITE), (WIDTH-50, 20))
    pygame.display.flip()
   
    for enemy in enemies:
       if player_mask.overlap(enemy_mask,(enemy[1].x-player_rect.x,enemy[1].y-player_rect.y)):
           playing=None
            
        
         
        if enemy[1].right<0 or enemy[1].bottom<0 or enemy[1].top>HEIGHT or enemy[1].left>WIDTH  :
            enemies.pop(enemies.index(enemy))
    for laser in lasers:
        if current_time - laser['creation_time']>2500:
            if player_rect.clipline(laser['start'], laser['stop']):
                playing=True
    for bonus in bonuses:
        if hit_out:
            if hit_mask.overlap(bonus_mask,(hit_rect.x-bonus['rect'].x,hit_rect.y-bonus['rect'].y)):
                score+=1
                bonuses.pop(bonuses.index(bonus))
                hit_out=None
        
        if player_mask.overlap(bonus_mask,(bonus['rect'].x-player_rect.x,bonus['rect'].y-player_rect.y)):
            score+=1
            bonuses.pop(bonuses.index(bonus))
    

'''
'''

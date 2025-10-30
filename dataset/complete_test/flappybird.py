#flappy bird game using pygame and github copilot :D. 
#i am impressed with copilot as i have a VERY basic understanding of coding.
#i am very impressed with the way she has helped me to learn python


#imports
#-----------------------------------------------------------------------------------------------------------------------
import pygame, sys, random


#set up pygame
#-----------------------------------------------------------------------------------------------------------------------
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
display_width = 288
display_height = 576
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
floor_x_pos = 0
gravity = 0.25
bird_movement = 0
bird_startx = 50
bird_starty = 250
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, random.randint(1200, 1600))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 150)
pipe_height = [180,288,372]
game_over = False
font = pygame.font.Font('assets/flappy.ttf', 20)
score = 0
point_timer = 0
high_score = 0
new_high_score = False
#load the saved high score
with open('assets/high_score.txt', 'r') as f:
    high_score = float(f.read())
    f.close()
game_start = True

#load images 
background_day = pygame.image.load('assets/background-day.png').convert()
background_night = pygame.image.load('assets/background-night.png').convert()
floor_surface = pygame.image.load('assets/base.png').convert()
bluebird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bluebird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bluebird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bluebird_frames = [bluebird_midflap, bluebird_upflap, bluebird_downflap]
bluebird_index = 1
bluebird_surface = bluebird_frames[bluebird_index]
bluebird_rect = bluebird_surface.get_rect(center=(bird_startx, bird_starty))
pipe_green = pygame.image.load('assets/pipe-green.png').convert()
pipe_red = pygame.image.load('assets/pipe-red.png').convert()
redbird_downflap = pygame.image.load('assets/redbird-downflap.png').convert_alpha()
redbird_midflap = pygame.image.load('assets/redbird-midflap.png').convert_alpha()
redbird_upflap = pygame.image.load('assets/redbird-upflap.png').convert_alpha()
yellowbird_downflap = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
yellowbird_midflap = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
yellowbird_upflap = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
game_over_screen = pygame.image.load('assets/gameover.png').convert_alpha()
game_over_rect = game_over_screen.get_rect(center = (display_width/2, display_height/2))
start_screen = pygame.image.load('assets/message.png').convert_alpha()
start_rect = start_screen.get_rect(center = (display_width/2, display_height/2))
#load sounds
die = pygame.mixer.Sound('assets/sfx_die.wav')
hit = pygame.mixer.Sound('assets/sfx_hit.wav')
point = pygame.mixer.Sound('assets/sfx_point.wav')
swoosh = pygame.mixer.Sound('assets/sfx_swooshing.wav')
wing = pygame.mixer.Sound('assets/sfx_wing.wav')


#my functions
#-----------------------------------------------------------------------------------------------------------------------
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 500))
    screen.blit(floor_surface, (floor_x_pos + display_width, 500))
def create_pipe():
    random_height = random.choice(pipe_height)
    bottom_pipe = pipe_green.get_rect(midtop = (display_width+50, random_height))
    top_pipe = pipe_green.get_rect(midbottom = (display_width+50, random_height-110))
    return bottom_pipe, top_pipe
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes  
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 490:
            screen.blit(pipe_green, pipe)
        else: 
            flipped_pipe = pygame.transform.flip(pipe_green, False, True)
            screen.blit(flipped_pipe, pipe)
def delete_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx < -50:
            pipes.remove(pipe)
    return pipes
def check_collision(pipes):
    if bluebird_rect.top <= -10 or bluebird_rect.bottom >= 500:
        die.play()
        return True
    for pipe in pipes:
        if bluebird_rect.colliderect(pipe):
            die.play()
            return True  
    return False
def rotate_bird(bluebird_surface):
    rotated_bird = pygame.transform.rotozoom(bluebird_surface, -bird_movement*3, 1)
    return rotated_bird

def display_score(game_state):
    if game_state == 'game':
        #print the score but limit the number of decimal places to 2
        display_score = font.render(str(round(score, 2)), True, (255, 255, 255))
        score_rect = display_score.get_rect(center = (display_width/2, 40))
        screen.blit(display_score, score_rect)
    if game_state == 'game_over':
        #print the score but limit the number of decimal places to 2
        display_score = font.render('Score:  '+str(round(score, 2)), True, (255, 255, 255))
        score_rect = display_score.get_rect(center = (display_width/2, 40))
        screen.blit(display_score, score_rect)
        #print the high score but limit the number of decimal places to 2
        display_high_score = font.render('High Score:  '+str(round(high_score, 2)), True, (255, 255, 255))
        high_score_rect = display_high_score.get_rect(center = (display_width/2, 100))
        screen.blit(display_high_score, high_score_rect)

#main loop
#-----------------------------------------------------------------------------------------------------------------------
while True:
    #check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not game_start:
                bird_movement = -5
                wing.play()
            if event.key == pygame.K_SPACE and game_over and not game_start:
                game_over = False
                bird_movement = 0
                bluebird_rect.center = (bird_startx, bird_starty)
                pipe_list = []
                score = 0
                new_high_score = False
            if event.key == pygame.K_SPACE and game_start:
                game_start = False
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == SPAWNPIPE and not game_start:
            pipe_list.extend(create_pipe())
            pygame.time.set_timer(SPAWNPIPE, random.randint(1250, 1900))
        if event.type == BIRDFLAP:
            bluebird_index += 1
            if bluebird_index >= 3:
                bluebird_index = 0
            bluebird_surface = bluebird_frames[bluebird_index]

    #update and then draw the game visuals with higher layers last to make them on top  
    #set up background
    screen.blit(background_day, (0,0))

    #game and game over loop    
    if game_over == False and game_start == False:
        #update/draw bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bluebird_surface)
        bluebird_rect.centery += bird_movement
        screen.blit(rotated_bird, bluebird_rect)
        game_over = check_collision(pipe_list)
        #update/draw pipes
        pipe_list = move_pipes(pipe_list)
        pipe_list = delete_pipes(pipe_list)
        draw_pipes(pipe_list)
        #update score
        score += 0.01
        point_timer += 1
        if point_timer == 100:
                point_timer = 0
                point.play()
        display_score('game')
    else:
        if score > high_score:
            high_score = score
            point.play()
            new_high_score = True
            #save the high score to a file
            with open('assets/high_score.txt', 'w') as f:
                f.write(str(high_score))
                f.close()
        if game_start == False:
            display_score('game_over')
            screen.blit(game_over_screen, game_over_rect)
            if new_high_score:
                #congratulate the player on a new high score
                grats = font.render('New High Score!', True, (255, 255, 255))
                grats_rect = grats.get_rect(center = (display_width/2, 80))
                screen.blit(grats, grats_rect)
    #show greeting screen   
    if game_start == True:
        screen.blit(start_screen, start_rect)

    #update/draw floor
    floor_x_pos -= 2
    if floor_x_pos <= -display_width:
        floor_x_pos = 0
    draw_floor()

    pygame.display.update()
    clock.tick(60)


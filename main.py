import pygame
import pygame.freetype
from objects import Ship, Pipe
from algorithm import Algorithm

mode = 'ai' # ai or human

pygame.init()
window_width = 1280
window_height = 720

# screen, clock
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True

# font
font = pygame.freetype.SysFont("Arial", 24)

# player
player = Ship(screen.get_height())
player_pos = pygame.Vector2(screen.get_width() / 4, screen.get_height() - player.radius)
dt = 0

# pipes
pipetick = 0
pipes = []

# scores
score = 0
highscore = 0

# ai algorithm
model = Algorithm()

def add_pipe():
    pipe = Pipe(screen.get_width(), screen.get_height())
    pipes.append(pipe)

def update_pipes():
    for i, pipe in enumerate(pipes):
        pipe.update_pos()

        pygame.draw.rect(screen, "black", pipe.toprect)
        pygame.draw.rect(screen, "black", pipe.botrect)


    for i, pipe in enumerate(pipes):
        if pipe.pos < -pipe.width:
            del pipes[i]

def intersects(rect, r, center):
    circle_distance_x = abs(center[0]-rect.centerx)
    circle_distance_y = abs(center[1]-rect.centery)
    if circle_distance_x > rect.w/2.0+r or circle_distance_y > rect.h/2.0+r:
        return False
    if circle_distance_x <= rect.w/2.0 or circle_distance_y <= rect.h/2.0:
        return True
    corner_x = circle_distance_x-rect.w/2.0
    corner_y = circle_distance_y-rect.h/2.0
    corner_distance_sq = corner_x**2.0 +corner_y**2.0
    return corner_distance_sq <= r**2.0

def get_nearest_pipe_info():
    if len(pipes) <= 0:
        return 0, screen.get_height(), screen.get_width()    

    for pipe in pipes:
        if pipe.pos + pipe.width > player_pos.x:
            nearest_pipe_topend = pipe.topend
            nearest_pipe_bottomend = pipe.bottomend
            nearest_pipe_x = pipe.pos
            break

    return nearest_pipe_topend, nearest_pipe_bottomend, nearest_pipe_x

def update_score():
    global score, highscore
    highscore = max(highscore, score)
    score = 0

def reset():
    pipes.clear()
    player.reset_pos()

def check_hit(player_pos):
    for i, pipe in enumerate(pipes):
        if intersects(pipe.toprect, player.radius, player_pos) or intersects(pipe.botrect, player.radius, player_pos):
            return True
    
    return False

def normalize_values(player_y, pipe_topend, pipe_bottomend, pipe_x):
    return [player_y/window_width,  pipe_topend/window_width, pipe_bottomend/window_width, pipe_x/window_height]
            
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    nearest_pipe_topend, nearest_pipe_bottomend, nearest_pipe_x = get_nearest_pipe_info()
    # print(nearest_pipe_x)
    # print(action)

    keys = pygame.key.get_pressed()

    if mode == 'human':
        action = keys[pygame.K_SPACE]
    elif mode == 'ai':
        action = (model.get_action(normalize_values(player_pos.y, nearest_pipe_topend, nearest_pipe_bottomend, nearest_pipe_x)) > 0)
    else:
        raise Exception("Error: Invalid mode")

    if action:
        player.update_pos('up', dt)
    else:
        player.update_pos('down', dt)
    
    player_pos.y = player.pos
    pygame.draw.circle(screen, "red", player_pos, player.radius)

    pipetick += 1
    if pipetick % 150 == 0:
        add_pipe()
        pipetick = 0

    score += 1
    
    update_pipes()
    font.render_to(screen, (10, 10), "Score: {}".format(score), (255, 255, 255))
    font.render_to(screen, (10, 40), "Highscore: {}".format(highscore), (255, 255, 255))
    pygame.display.flip()

    if check_hit(player_pos):
        pygame.time.wait(500)
        update_score()
        model.get_score(score)
        model.next_brain()
        reset()
    
    dt = clock.tick(60) / 1000


pygame.quit()
import pygame
import pygame.freetype
from objects import Ship, Pipe
from algorithm import Algorithm

class Game():
    def __init__(self):
        pygame.init()
        self.window_width = 1280
        self.window_height = 720

        # screen, clock
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.running = True

        # font
        self.font = pygame.freetype.SysFont("Arial", 24)

        # player
        self.player = Ship(self.screen.get_height())
        self.player_pos = pygame.Vector2(self.screen.get_width() / 4, self.screen.get_height() - self.player.radius)
        self.dt = 0

        # pipes
        self.pipetick = 0
        self.pipes = []

        # scores
        self.score = 0
        self.highscore = 0

        # tracking direction change
        self.prev_action = None
        self.changes = 0

    def add_pipe(self):
        pipe = Pipe(self.screen.get_width(), self.screen.get_height())
        self.pipes.append(pipe)

    def update_pipes(self):
        for i, pipe in enumerate(self.pipes):
            pipe.update_pos()

            pygame.draw.rect(self.screen, "black", pipe.toprect)
            pygame.draw.rect(self.screen, "black", pipe.botrect)


        for i, pipe in enumerate(self.pipes):
            if pipe.pos < -pipe.width:
                del self.pipes[i]

    def intersects(self, rect, r, center):
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

    def get_nearest_pipe_info(self):
        if len(self.pipes) <= 0:
            return 0, self.screen.get_height(), self.screen.get_width()    

        for pipe in self.pipes:
            if pipe.pos + pipe.width > self.player_pos.x:
                nearest_pipe_topend = pipe.topend
                nearest_pipe_bottomend = pipe.bottomend
                nearest_pipe_x = pipe.pos
                break

        return nearest_pipe_topend, nearest_pipe_bottomend, nearest_pipe_x

    def update_score(self):
        self.highscore = max(self.highscore, self.score)
        self.score = 0

    def reset(self):
        self.prev_action = None
        self.changes = 0
        self.pipes.clear()
        self.player.reset_pos()

    def check_hit(self, player_pos):
        for i, pipe in enumerate(self.pipes):
            if self.intersects(pipe.toprect, self.player.radius, player_pos) or self.intersects(pipe.botrect, self.player.radius, player_pos):
                return True
        
        return False

    def normalize_values(self, player_y, pipe_topend, pipe_bottomend, pipe_x):
        return [player_y/self.window_width,  pipe_topend/self.window_width, pipe_bottomend/self.window_width, pipe_x/self.window_height]
    
    def run(self, iters, mode='human', brain=None):
        scores = []
        dir_changes = []

        for _ in range(iters):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                self.screen.fill("purple")

                nearest_pipe_topend, nearest_pipe_bottomend, nearest_pipe_x = self.get_nearest_pipe_info()
                # print(nearest_pipe_x)
                # print(action)

                keys = pygame.key.get_pressed()

                if mode == 'human':
                    action = keys[pygame.K_SPACE]
                elif mode == 'ai':
                    action = (brain.forward(self.normalize_values(self.player_pos.y, nearest_pipe_topend, nearest_pipe_bottomend, nearest_pipe_x)) > 0)
                else:
                    raise Exception("Error: Invalid mode")

                if action:
                    self.player.update_pos('up', self.dt)
                else:
                    self.player.update_pos('down', self.dt)

                if self.prev_action != None:
                    if self.prev_action != action:
                        self.changes += 1
                    
                    
                self.prev_action = action
                
                self.player_pos.y = self.player.pos
                pygame.draw.circle(self.screen, "red", self.player_pos, self.player.radius)

                self.pipetick += 1
                if self.pipetick % 150 == 0:
                    self.add_pipe()
                    self.pipetick = 0

                self.score += 1
                
                self.update_pipes()
                self.font.render_to(self.screen, (10, 10), "Score: {}".format(self.score), (255, 255, 255))
                self.font.render_to(self.screen, (10, 40), "Highscore: {}".format(self.highscore), (255, 255, 255))
                pygame.display.flip()

                if self.check_hit(self.player_pos):
                    pygame.time.wait(500)
                    self.update_score()
                    scores.append(self.score)
                    dir_changes.append(self.changes)

                    self.reset()
                    break
                
                self.dt = self.clock.tick(60) / 1000

        pygame.quit()
        return scores, dir_changes
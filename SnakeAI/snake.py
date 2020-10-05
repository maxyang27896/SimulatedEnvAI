# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 22:16:54 2020

@author: MY2
"""

import pygame
import random
import tkinter as tk
from tkinter import messagebox
import numpy as np
import math
import matplotlib.pyplot as plt

white = (255, 255, 255) 
green = (0, 255, 0) 
red = (255,0,0)
black = (0, 0, 0)

class cube:
    '''
    Cube class which holds a position and a direction
    Used for drawing each section of the snake 
    '''
    def __init__(self, start, dirnx=1, dirny=0, colour=(255,0,0)):
        # Initial position and direction of a cube
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.colour = colour
        
        # Some paameters of pygame window
        self.width = 500
        self.rows = 20
        self.gaps  = self.width // self.rows
    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + dirnx, self.pos[1] + dirny)
        
        # have move out of bound logic here
        if self.dirnx == -1 and self.pos[0] < 0: 
            self.pos = (self.rows-1, self.pos[1])
        elif self.dirnx == 1 and self.pos[0] > self.rows-1: 
            self.pos = (0, self.pos[1])
        elif self.dirny == 1 and self.pos[1] > self.rows-1: 
            self.pos = (self.pos[0], 0)
        elif self.dirny == -1 and self.pos[1] < 0: 
            self.pos = (self.pos[0],self.rows-1)
    
    def draw(self, surface, eyes=False):
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.colour, (i*self.gaps+1, j*self.gaps+1, self.gaps-2, self.gaps-2))
        
        if eyes:
            centre = self.gaps//2
            radius = 3
            circleMiddle = (i*self.gaps+centre-radius,j*self.gaps+8)
            circleMiddle2 = (i*self.gaps + self.gaps -radius*2, j*self.gaps+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)       
        
    
class snake:
    body = []
    turns = {}
    def __init__(self, pos):
        self.colour = red
        self.action_size = 3
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = self.head.dirnx
        self.dirny = self.head.dirny
        self.addCube()
        self.addCube()
        self.addCube()
        self.addCube()
        self.addCube()
        self.addCube()
        self.addCube()
        self.addCube()
        self.addCube()
        self.addCube()
        
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)
    
    def move(self):
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and (self.dirnx, self.dirny) != (1, 0):
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
        if keys[pygame.K_RIGHT] and (self.dirnx, self.dirny) != (-1, 0):
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
        if keys[pygame.K_UP] and (self.dirnx, self.dirny) != (0, 1):
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
        if keys[pygame.K_DOWN] and (self.dirnx, self.dirny) != (0, -1):
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        
        
        for i, c in enumerate(self.body):
            # For turning the snake
            if c.pos in self.turns:
                p = c.pos
                c.move(self.turns[c.pos][0], self.turns[c.pos][1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            # If snake moves out of grid
            else:
                c.move(c.dirnx,c.dirny)
                
    def move_random(self):
        
        # get current direction 
        dir_x = self.dirnx
        dir_y = self.dirny
        
        # Take an action
        action = random.randrange(self.action_size)
        
        # Go left
        if action == 1:
            if self.dirnx == 0:
                self.dirnx = 1 * dir_y
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            else: 
                self.dirnx = 0
                self.dirny = -1 * dir_x
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        # Go right
        elif action == 2:
            if self.dirnx == 0:
                self.dirnx = -1 * dir_y
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            else: 
                self.dirnx = 0
                self.dirny = 1 * dir_x
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        else:
            # keep the snack on track
            pass
        
        
        for i, c in enumerate(self.body):
            # For turning the snake
            if c.pos in self.turns:
                p = c.pos
                c.move(self.turns[c.pos][0], self.turns[c.pos][1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            # If snake moves out of grid
            else:
                c.move(c.dirnx,c.dirny)
                
    
    def addCube(self):
        last_cube = self.body[-1]
        new_pos = (last_cube.pos[0] - last_cube.dirnx, last_cube.pos[1] - last_cube.dirny)
        new_cube = cube(new_pos, dirnx=last_cube.dirnx, dirny=last_cube.dirny)
        self.body.append(new_cube)
        
    def reset(self, pos):        
        self.body = []
        self.turns ={}
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = self.head.dirnx
        self.dirny = self.head.dirny
        self.addCube()

        
class CreateDisplay:
    
    def __init__(self):
        self.width = 500
        self.rows = 20
        self.text_width =  self.rows*2
        self.gaps  = self.width // self.rows
        
        random_pos = (random.randrange(self.rows), random.randrange(self.rows))
        self.s = snake(random_pos)
        self.snack = cube(self.random_snack(), colour=green)
        
        self.game_num = 0
        pygame.init() 
        
    def drawGrid(self, surface):
        x = 0
        y = 0   
        
        for l in range(0, self.rows):
            x = x + self.gaps
            y = y + self.gaps
            
            pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, self.width))
            pygame.draw.line(surface, (255, 255, 255), (0, y), (self.width, y))
            
    def random_snack(self):
        while True:
            x = random.randrange(self.rows)
            y = random.randrange(self.rows)
            if not ((x,y) in self.s.body):
                return (x,y)
    
    def redraw_window(self, surface):
        surface.fill(black)
        self.s.draw(surface)
        self.snack.draw(surface)
        self.drawGrid(surface)
        
        font = pygame.font.Font('freesansbold.ttf', 20) 
        text_score = font.render('Score:  ' + str(len(self.s.body)- 2), True, white) 
        textRect = text_score.get_rect()  
        textRect.center = (45, self.width + self.text_width//2) 
        surface.blit(text_score, textRect)
        
        text_game_num = font.render('Game:  ' + str(self.game_num), True, white)
        textRect = text_game_num.get_rect()  
        textRect.center = (400, self.width + self.text_width//2) 
        surface.blit(text_game_num, textRect)
        
        pygame.display.update()
        
    def message_box(subject, content):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)
        try:
            root.destroy()
        except:
            pass
    
    def check_intercept(self, head_pos, body_pos, line):
        delta_x = head_pos[0] - body_pos[0]
        delta_y = head_pos[1] - body_pos[1]
        if line == 0:
            if delta_x == 0:
                vision_index = line + 4*max(0, -np.sign(delta_y))
                return (abs(delta_y), vision_index)
            else:
                return (None, None)
        elif line == 1:
            if delta_x == - delta_y:
                dist = np.sqrt((delta_x**2) + (delta_y**2))
                vision_index = line + 4*max(0, np.sign(delta_x))
                return (dist, vision_index)
            else:
                return (None, None)
        elif line == 2:
            if delta_y == 0:
                vision_index = line + 4*max(0, np.sign(delta_x))
                return (abs(delta_x), vision_index)
            else:   
                return (None, None)
        else:  
            if delta_x == delta_y:
                dist = np.sqrt((delta_x**2) + (delta_y**2))
                vision_index = line + 4*max(0, np.sign(delta_y))
                return (dist, vision_index)
            else:
                return (None, None)

    
    def look_for_body(self):
        vision = np.zeros(8)         
        line = list(range(4))
        for b in self.s.body[1:]:
            for l in line:
                dist, vision_index = self.check_intercept(self.s.head.pos, b.pos, line[l])
                if dist != None:
                    if vision[vision_index]:
                        vision[vision_index] = min(vision[vision_index], dist)
                    else:
                        vision[vision_index] = dist 
        return vision
    

    def look_for_wall(self):
        
        def get_c(x, y, m):
            return y - m*x
    
        def intercept_line(m, c, x, y=False):
            if type(y) == bool:
                return [x, m*x + c]
            if type(x) == bool:
                return [(y - c)/m, y]
    
        vision = np.zeros(8)
        x = self.s.head.pos[0]
        y = self.s.head.pos[1]
        vision_line = [[-1, get_c(x, y, -1)],
                       [1, get_c(x, y, 1)]]
        walls = [[False, 0], [19, False], [False, 19], [0, False]]  # [y = 0, x = 19, y = 19, x = 0]
        
        X1 = intercept_line(vision_line[0][0], vision_line[0][1], walls[0][0], walls[0][1])
        X2 = intercept_line(vision_line[0][0], vision_line[0][1], walls[1][0], walls[1][1])
        X = X1 if (0 <= X1[0] < 20 and 0 <= X1[1] < 20) else X2
        vision[1] = np.sqrt(((X[0]-x)**2) + ((X[1]-y)**2))
        
        X1 = intercept_line(vision_line[0][0], vision_line[0][1], walls[2][0], walls[2][1])
        X2 = intercept_line(vision_line[0][0], vision_line[0][1], walls[3][0], walls[3][1])
        X = X1 if (0 <= X1[0] < 20 and 0 <= X1[1] < 20) else X2
        X = X1 if (0 <= X1[0] < 20 and 0 <= X1[1] < 20) else X2
        vision[5] = np.sqrt(((X[0]-x)**2) + ((X[1]-y)**2))
        
        X1 = intercept_line(vision_line[1][0], vision_line[1][1], walls[1][0], walls[1][1])
        X2 = intercept_line(vision_line[1][0], vision_line[1][1], walls[2][0], walls[2][1])
        X = X1 if (0 <= X1[0] < 20 and 0 <= X1[1] < 20) else X2
        vision[3] = np.sqrt(((X[0]-x)**2) + ((X[1]-y)**2))
        
        X1 = intercept_line(vision_line[1][0], vision_line[1][1], walls[0][0], walls[0][1])
        X2 = intercept_line(vision_line[1][0], vision_line[1][1], walls[3][0], walls[3][1])
        X = X1 if (0 <= X1[0] < 20 and 0 <= X1[1] < 20) else X2
        vision[7] = np.sqrt(((X[0]-x)**2) + ((X[1]-y)**2))
                
        vision[0] = self.s.head.pos[1]
        vision[2] = self.rows - 1 - self.s.head.pos[0]
        vision[4] = self.rows - 1 - self.s.head.pos[1]
        vision[6] = self.s.head.pos[0]
        
        return vision

    def get_inter_snake(self, n):
        total_len = len(self.s.body)
        index_frac = np.linspace(0, total_len-1, n)
        
        new_x = np.zeros(n)
        new_y = np.zeros(n)
        new_x[0], new_y[0] = self.s.body[0].pos
        new_x[-1], new_y[-1] = self.s.body[-1].pos
        for i in range(1, n-1):
            frac, index = math.modf(index_frac[i])
            x1, y1 = self.s.body[int(index)].pos
            x2, y2 = self.s.body[int(index)+1].pos
            delta_x = x2 - x1
            delta_y = y2 - y1
            if abs(delta_x) >= self.rows-1 or abs(delta_y) >= self.rows-1:
                new_x[i], new_y[i] = x2, y2
                continue
            if delta_x == 0:
                new_x[i] = x2
                new_y[i] = (delta_y)*frac + y1
            elif delta_y == 0 :
                new_x[i] = x1 + frac*(delta_x)
                new_y[i] = y2
            else:
                new_x[i] = x1 + frac*(delta_x)
                new_y[i] = (delta_y)*frac + y1
        return new_x,new_y
            
        
    
    def main_run(self):
        win = pygame.display.set_mode((self.width , self.width+ self.text_width))
        flag = True
        clock = pygame.time.Clock()      
       
        while flag:
            # Configure game speed
            pygame.time.delay(50)
            clock.tick(10)
            
            # Take a step
            self.s.move_random()
            vision = self.look_for_wall()
            print(vision)
            # x, y = self.get_inter_snake(20)
            # plt.plot(x,y, 'x')
            # plt.show()
            
            # If eats fruit
            if self.s.body[0].pos == self.snack.pos:
                self.snack = cube(self.random_snack(), colour =(0, 255, 0))
                self.s.addCube()
            
            # If eats its own tail, end game
            all_pos = [x.pos for x in self.s.body if x!=self.s.body[0]]
            if self.s.body[0].pos in all_pos:
                print('Score: ', len(self.s.body) - 2)
                self.message_box('You Lost!, Play again...')
                self.s.reset((10,10))
                self.game_num += 1
            
            # Render display
            self.redraw_window(win)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

display = CreateDisplay()
display.main_run()
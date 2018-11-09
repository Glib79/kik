# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 11:38:59 2018

@author: Grzegorz Libera
"""

class Tile(object):
    """ Tile object """
    
    def __init__(self, data):
        """
        Initiate of tile object
        input
        data - list with colors on tile (rgby) and dots on tile eg [r, g, b, y, g, b, r, y, 0, 1, 1, 0, 1, 0, 1, 0]
        """
        self.colors_1 = data[:4]
        self.colors_2 = data[4:8]
        self.dots_1 = []
        for d in data[8:12]:
            self.dots_1.append(int(d))
        self.dots_2 = []
        for d in data[12:]:
            self.dots_2.append(int(d))
        self.size = 80
        self.side = 1
        self.rotate = 0
        self.position = [0, 0]
    
    def flip_tile(self):
        """
        flips tile
        """
        if self.side == 1:
            self.side = 2
        else:
            self.side = 1
    
    def rotate_tile(self, direction):
        """
        rotate tile
        input
        direction - string (l, r); r - rotate right, l - rotate left
        """
        if direction == 'l':
            self.rotate += 1
            if self.rotate > 3:
                self.rotate = 0
        elif direction == 'r':
            self.rotate -= 1
            if self.rotate < 0:
                self.rotate = 3
                
    def get_tile(self):
        """
        return
        tuple with 2 lists colors and dots from proper site and proper order ready to draw
        """
        if self.side == 1:
            col = self.colors_1
            dot = self.dots_1
        else:
            col = self.colors_2
            dot = self.dots_2
        colors = col[self.rotate:] + col[:self.rotate]
        dots = dot[self.rotate:] + dot[:self.rotate]
        return colors, dots
            
    def draw(self, screen, pygame):
        """
        Draw a tile
        """
        t_colors, t_dots = self.get_tile()
        x = self.position[0]
        y = self.position[1]
        radius = int(self.size/10)
        points = [(x, y), (x+self.size, y), (x+self.size/2, y+self.size/2)]
        pygame.draw.polygon(screen, Tile.colors(t_colors[0]), points)
        points = [(x+self.size, y), (x+self.size, y+self.size), (x+self.size/2, y+self.size/2)]
        pygame.draw.polygon(screen, Tile.colors(t_colors[1]), points)
        points = [(x, y+self.size), (x+self.size, y+self.size), (x+self.size/2, y+self.size/2)]
        pygame.draw.polygon(screen, Tile.colors(t_colors[2]), points)
        points = [(x, y), (x, y+self.size), (x+self.size/2, y+self.size/2)]
        pygame.draw.polygon(screen, Tile.colors(t_colors[3]), points)
        pygame.draw.rect(screen, Tile.colors('gray'), pygame.Rect(x, y, self.size, self.size), 2)
        pygame.draw.line(screen, Tile.colors('gray'), (x,y), (x+self.size-1, y+self.size), 2)
        pygame.draw.line(screen, Tile.colors('gray'), (x,y+self.size), (x+self.size-1, y), 2)
        if t_dots[0] == 1:
           pygame.draw.circle(screen, Tile.colors('gray'), (int(x+self.size*0.5), int(y+self.size*0.2)), radius) 
        if t_dots[1] == 1:
           pygame.draw.circle(screen, Tile.colors('gray'), (int(x+self.size*0.8), int(y+self.size*0.5)), radius) 
        if t_dots[2] == 1:
           pygame.draw.circle(screen, Tile.colors('gray'), (int(x+self.size*0.5), int(y+self.size*0.8)), radius) 
        if t_dots[3] == 1:
           pygame.draw.circle(screen, Tile.colors('gray'), (int(x+self.size*0.2), int(y+self.size*0.5)), radius) 
        
    def set_position(self, x, y):
        """ Set a tile position """
        self.position[0] = x
        self.position[1] = y
    
    def set_size(self, size):
        """ Set tile size """
        self.size = size
    
    def is_clicked(self, pos):
        """ Check if position is on the tile """
        ret = True
        if pos[0] < self.position[0] or pos[0] > self.position[0] + self.size:
            ret = False
        if pos[1] < self.position[1] or pos[1] > self.position[1] + self.size:
            ret = False
        return ret
    
    def get_mouse_pos(self, pos):
        """ Return relative position on tile """
        return pos[0] - self.position[0], pos[1] - self.position[1]        
    
    @staticmethod
    def colors(color):
        """ Return tuple with rgb color """
        if color == 'r':
            return (255, 0, 0)
        elif color == 'ri':
            return (255, 100, 100)
        elif color == 'g':
            return (0, 255, 0)
        elif color == 'gi':
            return (100, 255, 100)
        elif color == 'b':
            return (0, 0, 255)
        elif color == 'bi':
            return (100, 100, 255)
        elif color == 'y':
            return (255, 255, 0)
        elif color == 'yi':
            return (255, 255, 100)
        elif color == 'gray':
            return (100, 100, 100)           
        elif color == 'gray_light':
            return (150, 150, 150)           
        elif color == 'white':
            return (255, 255, 255)           
        elif color == 'whitei':
            return (100, 100, 100)           

if __name__ == "__main__":
    print("This is a module with Tiles for kik game.")
    input("\nPress the enter key to exit.")                
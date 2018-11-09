# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 20:42:33 2018

@author: Grzegorz Libera
"""
import random

class Table(object):
    """ Object Table """
    def __init__(self, data, tile, pos):
        """ 
        Initialize Table
        input
        data - string - file name with tiles data
        tile - tile library
        pos - list - start position 
        """
        self.t_size = 40
        self.pos = pos
        self.base_pos = pos[:]
        self.tiles = [] #aviable tiles
        with open(data, 'r') as file: 
            try:
                for l in file.readlines():
                    self.tiles.append(tile.Tile(l.strip().split(',')))
                   # if len(self.tiles) > 16:
                   #     break
            except Exception as e: 
                print("Error:", e)
        self.start_tiles = [] #start tiles 
        for t in range(4):
            self.start_tiles.append(self.tiles.pop(0))
    
        random.shuffle(self.tiles)
        random.shuffle(self.start_tiles)
        
        self.table = {} #dictionary with played tiles
        self.posible_moves = [] #list with possible moves
        self.set_on_table((-1, -1), self.start_tiles[0])
        self.set_on_table((1, -1), self.start_tiles[1])
        self.set_on_table((1, 1), self.start_tiles[2])
        self.set_on_table((-1, 1), self.start_tiles[3])
        
        self.end = False
        
    def deal(self, hands, n_tiles):
        """ 
        Deals n_tiles tiles to each hand in hands
        hands - list - list of hands
        n_tiles - int - number of tiles to deal
        """
        for i in range(n_tiles):
            for h in hands:
                if self.tiles:
                    h.add_tile(self.tiles.pop(0))
    
    def set_on_table(self, coor, tile):
        """
        Set tile on table
        input
        coor - tile coordinates on table eg (1, 1)
        tile - tile object
        """
        tile.set_size(self.t_size)
        self.table[coor] = tile
        if coor in self.posible_moves:
            self.posible_moves.remove(coor)
        self.calculate_pm(coor)
    
    def change_position(self, x, y):
        """ 
        Change a table position 
        input
        x, y - int - how many tiles should be table move
        """
        self.pos[0] += x * self.t_size
        self.pos[1] += y * self.t_size
        
    def calculate_pm(self, coor):
        """ Calculates posible moves around pos """
        if not self.table.get((coor[0]-1, coor[1]), False) and not (coor[0]-1, coor[1]) in self.posible_moves:
            self.posible_moves.append((coor[0]-1, coor[1]))
        if not self.table.get((coor[0]+1, coor[1]), False) and not (coor[0]+1, coor[1]) in self.posible_moves:
            self.posible_moves.append((coor[0]+1, coor[1]))
        if not self.table.get((coor[0], coor[1]-1), False) and not (coor[0], coor[1]-1) in self.posible_moves:
            self.posible_moves.append((coor[0], coor[1]-1))
        if not self.table.get((coor[0], coor[1]+1), False) and not (coor[0], coor[1]+1) in self.posible_moves:
            self.posible_moves.append((coor[0], coor[1]+1))
    
    def is_on_pos_move(self, pos):
        """ 
        Check if position is on one of posible moves 
        input
        pos - tuple with position (x,y)
        return
        Tuple with coordinates of possible move (0,0)
        False - if pos isn't in possible moves
        """
        for m in self.posible_moves:
            if pos[0] >= self.pos[0] + m[0] * self.t_size and pos[0] <= self.pos[0] + m[0] * self.t_size + self.t_size and \
             pos[1] >= self.pos[1] + m[1] * self.t_size and pos[1] <= self.pos[1] + m[1] * self.t_size + self.t_size:
                return m
        return False
   
    def is_on_correct_move(self, coor, tile):
        """ 
        Check if tile is on correct move
        input
        coor - coordinate of possible move
        tile - tile to set on table
        return int earned points or False if move isn't correct and dictionary with points for closed fields
        """
        b_col, b_dot = tile.get_tile()
        points = 0
        check_f = {}
        points_for_colors = {}
        if (coor[0], coor[1]-1) in self.table:
            c_col, c_dot = self.table[(coor[0], coor[1]-1)].get_tile()
            if b_col[0] != c_col[2]:
                return False, points_for_colors
            else:
                points += 1 #point for edge
                check_f[0] = b_col[0] #need to check if field is closed
                if b_dot[0]:
                    points += 1 #point for dot
                if c_dot[2]:
                    points += 1 #point for dot
        if (coor[0]+1, coor[1]) in self.table:
            c_col, c_dot = self.table[(coor[0]+1, coor[1])].get_tile()
            if b_col[1] != c_col[3]:
                return False, points_for_colors
            else:
                points += 1 #point for edge
                check_f[1] = b_col[1] #need to check if field is closed
                if b_dot[1]:
                    points += 1 #point for dot
                if c_dot[3]:
                    points += 1 #point for dot
        if (coor[0], coor[1]+1) in self.table:
            c_col, c_dot = self.table[(coor[0], coor[1]+1)].get_tile()
            if b_col[2] != c_col[0]:
                return False, points_for_colors
            else:
                points += 1 #point for edge
                check_f[2] = b_col[2] #need to check if field is closed
                if b_dot[2]:
                    points += 1 #point for dot
                if c_dot[0]:
                    points += 1 #point for dot
        if (coor[0]-1, coor[1]) in self.table:
            c_col, c_dot = self.table[(coor[0]-1, coor[1])].get_tile()
            if b_col[3] != c_col[1]:
                return False, points_for_colors
            else:
                points += 1 #point for edge
                check_f[3] = b_col[3] #need to check if field is closed
                if b_dot[3]:
                    points += 1 #point for dot
                if c_dot[1]:
                    points += 1 #point for dot
        
        f_colors_checked = []
        points_for_colors = {}
        for s in check_f:
            if not check_f[s] in f_colors_checked:
                f_colors_checked.append(check_f[s])
                self.checked = [] #clear a list of checked tiles
                fp = self.is_field(coor, s, tile)
                if not fp is False and fp > 1:
                    points += fp
                    points_for_colors[check_f[s]] = int(fp)
        
        return int(points), points_for_colors
    
    def is_field(self, coor, side, s_tile = False):
        """
        Check if field is closed
        input
        coor - coordinates of tile to check
        side - tile side to start checking
        s_tile - start tile
        returns false if it isn't closed or earned points if it is
        """
        points = 0
        #if this tile was already checked we don't need to check it again
        if coor in self.checked:
            return 0
        #if tile doesn't exist field isn't closed
        tile = self.table.get(coor, False)
        if not tile and s_tile:
            tile = s_tile
        if not tile:
            return False
        #tile exists so we mark it as checked
        self.checked.append(coor)
        #get tile data
        colors, dots = tile.get_tile()
        #first side
        points += 0.5
        #next tile on first side we need to check only in first tile, but we check it always for shure
        ep = self.is_field(self.get_coor_to_check(coor, side), self.get_side(side, 2))
        if ep is False:
            return False
        else:
            points += ep
            
        check_os = False #should we check oposite side
        #second side
        n_side = self.get_side(side, 1)
        if colors[side] == colors[n_side]:
            points += 0.5
            ep = self.is_field(self.get_coor_to_check(coor, n_side), self.get_side(n_side, 2))
            if ep is False:
                return False
            else:
                points += ep
                check_os = True
        #fourth side
        n_side = self.get_side(side, 3)
        if colors[side] == colors[n_side]:
            points += 0.5
            ep = self.is_field(self.get_coor_to_check(coor, n_side), self.get_side(n_side, 2))
            if ep is False:
                return False
            else:
                points += ep
                check_os = True
        #oposite side
        if check_os:
            n_side = self.get_side(side, 2)
            if colors[side] == colors[n_side]:
                points += 0.5
                ep = self.is_field(self.get_coor_to_check(coor, n_side), self.get_side(n_side, 2))
                if ep is False:
                    return False
                else:
                    points += ep
        
        return points
    
    def get_coor_to_check(self,coor, side):
        """
        Helper function with returns coordinates of tile in proper site
        input
        coor - coordinates of tile
        side - side of tile
        """
        if side == 0:
            return (coor[0], coor[1]-1)
        elif side == 1:
            return (coor[0]+1, coor[1])
        elif side == 2:
            return (coor[0], coor[1]+1)
        elif side == 3:
            return (coor[0]-1, coor[1])
        
        raise ValueError("Wrong side number")
    
    def get_side(self, side, shift):
        """Returns shifted side"""
        side += shift
        if side > 3:
            side %= 4
        if side < 0:
            side = 4 + side
        return side
    
    def get_left_tiles(self):
        """Return number of left tiles"""
        return len(self.tiles)
    
    def draw(self, screen, pygame):
        """ Draw table """
        for t in self.table:
            self.table[t].set_position(self.pos[0] + t[0] * self.t_size, self.pos[1] + t[1] * self.t_size)
            self.table[t].draw(screen, pygame)
        #draw posible moves
        for m in self.posible_moves:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.pos[0] + m[0] * self.t_size, self.pos[1] + m[1] * self.t_size, self.t_size, self.t_size), 1)

if __name__ == "__main__":
    print("This is a module with Table for kik game.")
    input("\nPress the enter key to exit.")  
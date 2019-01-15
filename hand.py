# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 15:58:40 2018

@author: Grzegorz Libera
"""

class Hand(object):
    """ Hand object """
    chnd = 0
    
    def __init__(self, start_pos, player):
        """ Hand initiation """
        Hand.chnd += 1
        self.tiles = []
        self.size = 80
        self.chosen = 0
        self.start_position = start_pos
        self.name = player[0] if player[0] != '' else 'Player ' + str(Hand.chnd)
        self.type = player[1]
        self.color = player[2]
        self.space = 20
        self.points = 0
        self.end = False

    def __len__(self):
        """ Return number of tiles on hand """
        return len(self.tiles)
    
    def add_tile(self, tile):
        """ Add tile, and set it's position"""
        tile.set_size(self.size)
        pos = self.get_pos_on_hand(len(self.tiles))
        tile.set_position(pos[0], pos[1])
        self.tiles.append(tile)
    
    def add_points(self, points):
        """ Add points"""
        self.points += points
        
    def rem_chosen_tile(self):
        """ Remove chosen tile from hand """
        if self.tiles:
            del self.tiles[self.chosen]
            
        if self.tiles:
            self.chosen = 0
            pos = self.get_pos_on_hand(0)
            self.get_chosen().set_position(pos[0], pos[1])
        else:
            self.end = True
    
    def set_chosen(self, chosen):
        """ Set chosen tile """
        self.chosen = chosen
    
    def get_pos_on_hand(self, nr):
        """ Return tile position on hand """
        return (self.start_position[0], self.start_position[1] + (self.size + self.space) * nr)
        
    
    def get_chosen(self):
        """ Return chosen tile """
        return self.tiles[self.chosen]
    
    def get_hand(self):
        """ Return all tiles on hand """
        return self.tiles
    
    def is_end(self):
        return self.end
    
    def find_best_move(self, table):
        """ Finding the best move """
        best_pos = [] #tile nr, tile site, tile rotation, () - position on table
        best_points = 0
        best_pfc = {}
        
        for t in range(len(self.tiles)):
            for s in range(2):
                for r in range(4):
                    for p in table.posible_moves:
                        points, pfc = table.is_on_correct_move(p, self.tiles[t])
#                        if points:
#                           print([t,s,r,p], end=" ")
#                            print(points,  end=" ")
#                            print(pfc,  end=" ")
#                            print(self.tiles[t].get_tile())
                        if points and points > best_points:
                            best_pos = [t, s, r, p]
                            best_points = points
                            best_pfc = pfc
                    self.tiles[t].rotate_tile('l')
                self.tiles[t].flip_tile()
                        
        return best_pos, best_points, best_pfc
        
    def draw(self, screen, pygame):
        """ Draw hand """
        for t in range(len(self.tiles)):
            self.tiles[t].draw(screen, pygame)
            if t == self.chosen:
                pygame.draw.rect(screen, (255,0,255), pygame.Rect(self.tiles[t].position[0], self.tiles[t].position[1], self.tiles[t].size, self.tiles[t].size), 2)


if __name__ == "__main__":
    print("This is a module with Hand for kik game.")
    input("\nPress the enter key to exit.")  
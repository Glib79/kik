# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 16:59:45 2018

@author: Grzegorz Libera
"""

import tile
import datetime

class SceneBase:
    """
    Abstraction scene class 
    """
    def __init__(self, pygame):
        self.next = self
        self.pygame = pygame
        self.started = False # determine if object needs some data
    
    def ProcessInput(self, events, pressed_keys):
        """
        This method will receive all the events that happened since the last frame.
        """
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        """
        Game logic for the scene.
        """
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        """
        Rrender code. It will receive the main screen Surface as input.
        """
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        """
        Set next scene
        """
        self.next = next_scene
    
    def Terminate(self):
        """
        Finish the game
        """
        self.SwitchToScene(None)
        
    def get_high_score(self, pickle):
        """
        Gets high score data from file
        """
        try:
            f =  open("hs.dat", "rb")
            hs = pickle.load(f)
            f.close()
        except (EOFError, FileNotFoundError) as e:
            hs = []
            
        return hs
    
    def render_high_score(self, screen, hs, myfont, pos_params):
        """
        Prepare high score data to render
        input
        screen - pygame screen
        hs - high score
        myfont - pygame font
        pos_params - params for find_pos() function
        """
        x_start, y_start = self.find_pos(pos_params)
        
        y_move = 15
        x = [x_start, x_start + 15, x_start + 70] #position for number, points, name
        position = 0
        texts = []
        texts.append([myfont.render("HIGH SCORE", 1, (255,255,255)), (x_start + 30, y_start)]) #high score title
        y_start += 10
        for h in hs:
            position += 1
            texts.append([myfont.render(str(position), 1, (255,255,255)) ,(x[0], y_start + (position * y_move))])
            texts.append([myfont.render(str(h[0]), 1, (255,255,255)) ,(x[1], y_start + (position * y_move))])
            texts.append([myfont.render(str(h[1]), 1, (255,255,255)) ,(x[2], y_start + (position * y_move))])  
            
        for i in texts:
            screen.blit(i[0], i[1])
            
    def find_pos(self, params):
        """
        Finds position on screen for element
        input
        params - tuple with 4 parameters
            1 - x axis base eg. l - for left, c - for center, r - for right
            2 - x axis shift eg. 10, -20
            3 - y axis base eg. t - for top, c - for center, b - for bottom
            4 - y axis shift eg. 10, -20
            eg. ('c', -20, 't', '-10') - means set point -20px form screen center in x axis and -10px form top screen in y axis 
        output
        list with 2 coordinates x and y eg. [100, 150]
        """
        w, h = self.pygame.display.get_surface().get_size()
        x = 0
        y = 0
        
        if params[0] == 'l':
            x = params[1]
        elif params[0] == 'c':
            x = round(w/2) + params[1]
        elif params[0] == 'r':
            x = w + params[1]

        if params[2] == 't':
            y = params[3]
        elif params[2] == 'c':
            y = round(h/2) + params[3]
        elif params[2] == 'b':
            y = h + params[3]
        
        return [x, y]

class StartScene(SceneBase):
    """
    Start the game
    """
    def __init__(self, pygame):
        SceneBase.__init__(self, pygame)
        self.myfont = None
        self.texts = []
        self.texts.append(["", ('c', -270, 'c', -40)]) #place for title
        self.texts.append(["", ('c', 180, 'c', 20)]) #place for subtitle
        self.texts.append(["", ('c', -120, 'b', -40)]) #place for instruction
    
        self.tiles = []
        self.tiles.append(tile.Tile(['r','g','g','g','g','b','r','y',1,1,0,0,0,0,1,1]))
        self.tiles.append(tile.Tile(['r','b','b','b','g','b','y','r',1,1,0,0,1,1,0,0]))
        self.tiles.append(tile.Tile(['r','y','y','y','g','y','b','r',1,1,0,0,0,0,1,1]))
        self.tiles.append(tile.Tile(['b','r','g','g','r','g','g','g',1,0,0,1,1,1,0,0]))
        self.tiles.append(tile.Tile(['b','r','y','y','r','b','b','b',0,1,1,0,1,0,0,1]))
        self.tiles.append(tile.Tile(['r','y','g','g','r','y','y','y',0,1,1,0,0,0,1,1]))
        self.tiles.append(tile.Tile(['r','g','b','y','b','r','r','r',1,0,1,0,1,0,0,1]))
        self.tiles.append(tile.Tile(['r','b','g','y','b','g','g','g',0,0,1,1,0,0,1,1]))
        self.tiles.append(tile.Tile(['r','b','y','g','b','y','y','y',1,0,0,1,1,0,0,1]))
        self.tiles.append(tile.Tile(['g','r','b','b','r','r','y','y',1,0,1,0,0,1,1,0]))
        self.tiles.append(tile.Tile(['g','r','y','y','g','g','b','b',0,1,0,1,0,1,1,0]))
        self.tiles.append(tile.Tile(['r','b','g','g','g','g','y','y',1,0,0,1,0,1,1,0]))

       
        for t in self.tiles:
            t.set_size(100)
            
        self.tiles[4].rotate_tile('r')
        self.tiles[4].rotate_tile('r')
        self.tiles[1].flip_tile()
        self.tiles[2].rotate_tile('l')
        self.tiles[5].rotate_tile('l')
        self.tiles[5].rotate_tile('l')
        self.tiles[6].rotate_tile('r')
        self.tiles[8].rotate_tile('r')
        self.tiles[7].rotate_tile('r')
        self.tiles[7].rotate_tile('r')
        self.tiles[11].rotate_tile('l')
        self.tiles[9].flip_tile()
        self.tiles[9].rotate_tile('r')

    def set_myfont(self, myfont):
        self.myfont = myfont
        titlefont = self.pygame.font.SysFont("monospace", 50)
        stitlefont = self.pygame.font.SysFont("monospace", 10)
        self.texts[0][0] = titlefont.render("Squares and Colors", 1, (255,255,255))
        self.texts[1][0] = stitlefont.render("Game by G.", 1, (255,255,255))
        self.texts[2][0] = self.myfont.render("Press space to continue", 1, (255,255,255))

        self.started = True
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == self.pygame.KEYDOWN:
                if event.key == self.pygame.K_SPACE:
                    self.SwitchToScene(SetScene(self.pygame))

    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill((0, 0, 0))
        
        x, y = self.find_pos(('c', -390, 'c' , -160))
        self.tiles[0].set_position(x, y)
        self.tiles[1].set_position(x, y+100)
        self.tiles[2].set_position(x, y+200)
        self.tiles[3].set_position(x+100, y)
        self.tiles[4].set_position(x+200, y)
        self.tiles[5].set_position(x+100, y+200)
        self.tiles[6].set_position(x, y+300)
        self.tiles[7].set_position(x, y-100)
        self.tiles[8].set_position(x+100, y-100)
        self.tiles[9].set_position(x-100, y+200)
        self.tiles[10].set_position(x-100, y+100)
        self.tiles[11].set_position(x-100, y)
        
        for t in self.tiles:
            t.draw(screen, self.pygame)
        
        for i in self.texts:
            screen.blit(i[0], self.find_pos(i[1]))
            
class SetScene(SceneBase):
    """
    Scene with game settings
    """
    def __init__(self, pygame):
        SceneBase.__init__(self, pygame)
        self.myfont = None
        self.pickle = None
        self.players = []
        self.texts = []
        self.texts.append(["", ('c', -120, 't', 10)]) #place for title
        self.texts.append(["", ('c', -200, 'b', -40)]) #place for instruction
        self.input_boxes = []
        self.toggle_boxes = []
        self.hs = []
        
        self.font = self.pygame.font.Font(None, 32)
        
        self.tlist = ['Player', 'Computer', 'None']
    
    def set_myfont(self, myfont, players, pickle):
        self.myfont = myfont
        self.pickle = pickle
        self.players = players
        self.texts[0][0] = self.myfont.render("Set player data", 1, (255,255,255))
        self.texts[1][0] = self.myfont.render("Press space to start game or i for instructions", 1, (255,255,255))
        
        xib, y = self.find_pos(('c', -85, 't', 50))
        xtb, y = self.find_pos(('c', -215, 't', 50))

        #self.texts.append([self.myfont.render("Player 1", 1, (255,255,255)), (10, 55)])
        self.input_boxes.append(InputBox(self.pygame, xib, 50, 300, 32, 'white', players[0][0]))
        self.toggle_boxes.append(ToggleBox(self.pygame, xtb, 50, 120, 32, players[0][2], self.tlist, players[0][1]))
        
        #self.texts.append([self.myfont.render("Player 2", 1, (255,255,255)), (10, 95)])
        self.input_boxes.append(InputBox(self.pygame, xib, 90, 300, 32, 'white', players[1][0]))
        self.toggle_boxes.append(ToggleBox(self.pygame, xtb, 90, 120, 32, players[1][2], self.tlist, players[1][1]))
        
        #self.texts.append([self.myfont.render("Player 3", 1, (255,255,255)), (10, 135)])
        self.input_boxes.append(InputBox(self.pygame, xib, 130, 300, 32, 'white', players[2][0]))
        self.toggle_boxes.append(ToggleBox(self.pygame, xtb, 130, 120, 32, players[2][2], self.tlist, players[2][1]))
        
        #self.texts.append([self.myfont.render("Player 4", 1, (255,255,255)), (10, 175)])
        self.input_boxes.append(InputBox(self.pygame, xib, 170, 300, 32, 'white', players[3][0]))
        self.toggle_boxes.append(ToggleBox(self.pygame, xtb, 170, 120, 32, players[3][2], self.tlist, players[3][1]))
        
        self.hs = self.get_high_score(self.pickle)
    
        self.started = True
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            #toggle boxes
            for box in self.toggle_boxes:
                box.handle_event(event)
            #input boxes
            box_active = False
            for box in self.input_boxes:
                box.handle_event(event)
                if box.active == True:
                    box_active = True
            #other events
            if not box_active and event.type == self.pygame.KEYDOWN:
                if event.key == self.pygame.K_SPACE:
                    self.SwitchToScene(GameScene(self.pygame))
                if event.key == self.pygame.K_i:
                    self.SwitchToScene(KeyScene(self.pygame))

    def Update(self):
        xib, y = self.find_pos(('c', -85, 't', 50))
        for box in self.input_boxes:
            box.update(xib, y)
            y += 40

        xtb, y = self.find_pos(('c', -215, 't', 50))        
        for box in self.toggle_boxes:
            box.update(xtb, y)
            y += 40
    
    def Render(self, screen):
        screen.fill((0, 0, 0))
        
        for box in self.input_boxes:
            box.draw(screen)

        for box in self.toggle_boxes:
            box.draw(screen)
            
        for i in self.texts:
            screen.blit(i[0], self.find_pos(i[1]))    

        self.render_high_score(screen, self.hs, self.myfont, ('c', -70, 'b', -200))


class InputBox:
    """
    Class for input box
    """
    def __init__(self, pygame, x, y, w, h, color, text=''):
        self.pygame = pygame
        self.rect = self.pygame.Rect(x, y, w, h)
        ci = tile.Tile.colors(color + 'i')
        self.c_inactive = self.pygame.Color(ci[0], ci[1], ci[2], 0)
        ca = tile.Tile.colors(color)
        self.c_active = self.pygame.Color(ca[0], ca[1], ca[2], 0)
        self.font = self.pygame.font.Font(None, 32)
        self.color = self.c_inactive
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.allow_keys = (32,39,44,45,46,47,48,49,50,51,52,53,54,55,56,57,59,61,91,92,93,96,97,98,99,100,101,102,103,104,105,106 \
                           ,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,256,257,258,259,260,261,262,263,264 \
                           ,265,266,267,268,269,270,271)
        self.active = False

    def handle_event(self, event):
        if event.type == self.pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == self.pygame.KEYDOWN:
            if self.active:
                if event.key == self.pygame.K_RETURN or event.key == self.pygame.K_KP_ENTER:
                    self.active = False
                elif event.key == self.pygame.K_BACKSPACE or event.key == self.pygame.K_DELETE:
                    self.text = self.text[:-1]
                else:
                    if event.key in self.allow_keys and len(self.text) < 20:
                        self.text += event.unicode
        # Change the current color of the input box.
        self.color = self.c_active if self.active else self.c_inactive
        # Re-render the text.
        self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self, x, y):
        # Resize the box if the text is too long.
        width = max(300, self.txt_surface.get_width()+10)
        self.rect.w = width
        
        #In case of resize window we should move the box
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        self.pygame.draw.rect(screen, self.color, self.rect, 2)

class ToggleBox:
    """
    Class for toggle box
    """
    def __init__(self, pygame, x, y, w, h, color, tlist, val = 0):
        self.pygame = pygame
        self.rect = self.pygame.Rect(x, y, w, h)
        ca = tile.Tile.colors(color)
        self.color = self.pygame.Color(ca[0], ca[1], ca[2], 0)
        self.fcolor = self.pygame.Color(0, 0, 0, 0)
        self.font = self.pygame.font.Font(None, 32)
        self.val = val
        self.tlist = tlist
        self.txt_surface = self.font.render(self.tlist[self.val], True, self.fcolor)

    def handle_event(self, event):
        if event.type == self.pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the toggle_box rect.
            if self.rect.collidepoint(event.pos):
                # Change value to the next on the list
                self.val += 1
                try:
                    # Re-render the text.
                    self.txt_surface = self.font.render(self.tlist[self.val], True, self.fcolor)
                except IndexError:
                    self.val = 0
                    # Re-render the text.
                    self.txt_surface = self.font.render(self.tlist[self.val], True, self.fcolor)

    def update(self, x, y):
        #In case of resize window we should move the box
        self.rect.x = x
        self.rect.y = y
        
    def draw(self, screen):
        # Blit the rect.
        self.pygame.draw.rect(screen, self.color, self.rect, 0)
        # Blit the text.
        margin = round((self.rect.w - self.txt_surface.get_width()) / 2)
        screen.blit(self.txt_surface, (self.rect.x + margin, self.rect.y+5))

class KeyScene(SceneBase):
    """
    Scene with Keyboard controls
    """
    def __init__(self, pygame):
        SceneBase.__init__(self, pygame)
        self.myfont = None
        self.texts = []
        self.texts.append(["", ('c', -80, 't', 10)]) #place for title
        self.texts.append(["", ('c', -110, 'b', -40)]) #place for instruction
    
    def set_myfont(self, myfont):
        self.myfont = myfont
        self.texts[0][0] = self.myfont.render("Keyboard controls", 1, (255,255,255))
        self.texts[1][0] = self.myfont.render("Press space to return", 1, (255,255,255))
        start_x = -200
        start_y = 40
        self.texts.append([self.myfont.render("f - flip tile", 1, (255,255,255)), ('c', start_x, 't', start_y)])
        self.texts.append([self.myfont.render("a - rotate tile left", 1, (255,255,255)), ('c', start_x, 't',  start_y+15)])
        self.texts.append([self.myfont.render("d - rotate tile right", 1, (255,255,255)), ('c', start_x, 't',  start_y+30)])
        self.texts.append([self.myfont.render("mouse drag and drop - set tile on position", 1, (255,255,255)), ('c', start_x, 't',  start_y+45)])
        self.texts.append([self.myfont.render("arrows + space - move table", 1, (255,255,255)), ('c', start_x, 't',  start_y+60)])
        
        self.texts.append([self.myfont.render("Points", 1, (255,255,255)), ('c', start_x+170, 't',  start_y+90)])
        self.texts.append([self.myfont.render("1p - for each matching side", 1, (255,255,255)), ('c', start_x, 't',  start_y+105)])
        self.texts.append([self.myfont.render("1p - for each dot on matching side", 1, (255,255,255)), ('c', start_x, 't',  start_y+120)])
        self.texts.append([self.myfont.render("1p - for each small square, when the field is closed", 1, (255,255,255)), ('c', start_x, 't',  start_y+135)])

        self.started = True
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == self.pygame.KEYDOWN:
                if event.key == self.pygame.K_SPACE:
                    self.SwitchToScene(SetScene(self.pygame))

    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill((0, 0, 0))
        
        for i in self.texts:
            screen.blit(i[0], self.find_pos(i[1]))

            
class GameScene(SceneBase):
    """
    The game
    """
    def __init__(self, pygame):
        SceneBase.__init__(self, pygame)
        self.tbl = None
        self.hands = []
        self.hnd = None
        self.move = 0
        self.myfont = None
        self.drag = False
        self.rel_pos = (0, 0)
        self.texts = []
        self.texts.append(["", ('c', -80, 't', 10)]) #place for info for player
        self.texts.append(["", ('r', -140, 't', 10)]) #place for info about left tiles
        self.nav = []
        
        now = datetime.datetime.today()
        self.end_screen = 'games/game_'+now.strftime("%Y%m%d_%H%M%S")+'.jpg'        
    
    def set_data(self, table, hands, myfont):
        self.tbl = table
        self.tbl.pos = self.find_pos(('c', 30, 'c', -20))
        self.tbl.base_pos = self.find_pos(('c', 30, 'c', -20))
        
        self.hands = hands
        if self.hands:
            self.hnd = self.hands[0]
            self.tbl.deal(self.hands, 2)
        else:
            self.tbl.end = True #no hands so the game is end
        self.myfont = myfont
        self.texts[0][0] = self.myfont.render("", 1, (255,255,255))
        
        #players points
        y = 10
        for h in self.hands:
            self.texts.append(["", ('l', 25, 't', y)])
            y += 15
        
        x, y = self.find_pos(('r', -20, 'b', -20))
        self.nav.append(NavButtons(self.pygame, self.tbl, x, y))
        
        self.started = True
    
    def ProcessInput(self, events, pressed_keys):
        if self.hnd.type == 0: #player
            for event in events:
                #table navigations
                for n in self.nav:
                    n.handle_event(event)                
                    
                if event.type == self.pygame.KEYDOWN:
                    # determine if a letter key was pressed 
                    if event.key == self.pygame.K_f: # flip tile
                        self.hnd.get_chosen().flip_tile()
                    elif event.key == self.pygame.K_a: # rotate tile left
                        self.hnd.get_chosen().rotate_tile('l')
                    elif event.key == self.pygame.K_d: # rotate tile right
                        self.hnd.get_chosen().rotate_tile('r')
                
                if event.type == self.pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        for t in range(len(self.hnd)): # change tile
                            if self.hnd.tiles[t].is_clicked(event.pos):
                                self.hnd.set_chosen(t)
                                self.drag = True
                                self.rel_pos = self.hnd.get_chosen().get_mouse_pos(event.pos)
                                break
    
                if event.type == self.pygame.MOUSEBUTTONUP:
                    if event.button == 1: 
                        self.drag = False
                        ret = True
                        pos_move = self.tbl.is_on_pos_move(event.pos)
                        if pos_move:
                            points, pfc = self.tbl.is_on_correct_move(pos_move, self.hnd.get_chosen())
                            if points:
                                ret = False
                                self.tbl.set_on_table(pos_move, self.hnd.get_chosen())
                                self.hnd.add_points(points)
                                self.hnd.rem_chosen_tile()
                                self.tbl.deal([self.hnd], 1)
                                if pfc:
                                    for h in self.hands:
                                        if pfc.get(h.color, False) and h != self.hnd:
                                            h.add_points(pfc[h.color])
                                
                                self.next_hand()
                        self.texts[0][0] = self.myfont.render("", 1, (255,255,255))
                        if ret:
                            self.hnd.get_chosen().set_size(self.hnd.size)
                            pos = self.hnd.get_pos_on_hand(self.hnd.chosen)
                            self.hnd.get_chosen().set_position(pos[0], pos[1])
                            
                
                if event.type == self.pygame.MOUSEMOTION:
                    if self.drag: # move tile
                        position = event.pos
                        pos_move = self.tbl.is_on_pos_move(event.pos)
                        if pos_move:
                            points, pfc = self.tbl.is_on_correct_move(pos_move, self.hnd.get_chosen())
                            if points:
                                self.texts[0][0] = self.myfont.render("Possible points to earn: " + str(points), 1, (255,255,255))
                            else:
                                self.texts[0][0] = self.myfont.render("Incorrect move", 1, (255,255,255))
                            self.hnd.get_chosen().set_size(self.tbl.t_size)
                            self.hnd.get_chosen().set_position(position[0] - self.rel_pos[0]/(self.hnd.size/self.tbl.t_size), position[1] - self.rel_pos[1]/(self.hnd.size/self.tbl.t_size))
                        else:
                            self.hnd.get_chosen().set_size(self.hnd.size)
                            self.hnd.get_chosen().set_position(position[0] - self.rel_pos[0], position[1] - self.rel_pos[1])
                            self.texts[0][0] = self.myfont.render("", 1, (255,255,255))
        elif self.hnd.type == 1: #computer
            pos, points, pfc = self.hnd.find_best_move(self.tbl)
            self.hnd.set_chosen(pos[0])
            if pos[1] == 1:
                self.hnd.get_chosen().flip_tile()
            for i in range(pos[2]):
                self.hnd.get_chosen().rotate_tile('l')
            
            self.tbl.set_on_table(pos[3], self.hnd.get_chosen())
            self.hnd.add_points(points)
            self.hnd.rem_chosen_tile()
            self.tbl.deal([self.hnd], 1)
            if pfc:
                for h in self.hands:
                    if pfc.get(h.color, False) and h != self.hnd:
                        h.add_points(pfc[h.color])
                                
            self.next_hand()
    
    def next_hand(self):
        """Change hands"""
        self.move += 1
        try:
            self.hnd = self.hands[self.move]
        except IndexError:
            self.move = 0
            self.hnd = self.hands[self.move]
            
        
    def Update(self):
        if self.tbl.end:
             self.SwitchToScene(EndScene(self.pygame, self.hands))
        else:
            self.texts[1][0] = self.myfont.render("Left tiles: " + str(self.tbl.get_left_tiles()), 1, (255,255,255)) 
            s = 2
            end = True
            for h in self.hands:
                if not h.is_end():
                    end = False
                    
                if h == self.hnd and not end:
                    self.texts[s][0] = self.myfont.render(h.name + ": " + str(h.points) + " - Your move!", 1, (255,255,255))        
                else:
                    self.texts[s][0] = self.myfont.render(h.name + ": " + str(h.points), 1, (255,255,255))        
                s += 1
            
            if end:
                self.tbl.end = True
                self.texts[1][0] = self.myfont.render("", 1, (255,255,255)) 
                self.SwitchToScene(EndScene(self.pygame, self.hands, self.end_screen))

            self.tbl.base_pos = self.find_pos(('c', 30, 'c', -20))
            
            x, y = self.find_pos(('r', -20, 'b', -20))
            for n in self.nav:
                n.update(x,y)
    
    def Render(self, screen):
        screen.fill((0, 0, 0))
        
        # draw
        if self.tbl.end:
            self.tbl.pos = self.tbl.base_pos[:]

        self.tbl.draw(screen, self.pygame)
        if not self.tbl.end:
            self.hnd.draw(screen, self.pygame)
            
            for n in self.nav:
                n.draw(screen)
            
        y = 13
        for h in self.hands:
            self.pygame.draw.rect(screen, tile.Tile.colors(h.color), self.pygame.Rect(10, y, 10, 10), 0)
            y += 15
        
        for i in self.texts:
            screen.blit(i[0], self.find_pos(i[1]))
        
        if self.tbl.end:
            self.pygame.image.save(screen, self.end_screen)

class NavButtons(object):
    """
    Buttons for table navigation
    """
    def __init__(self, pygame, table, x, y):
        self.pygame = pygame
        self.tbl = table
        self.x = x # menu position x
        self.y = y # menu position y
        self.inactive_color = tile.Tile.colors('gray')
        self.active_color = tile.Tile.colors('white')
        self.ready_color = tile.Tile.colors('gray_light')
        #colors of nav elements arrow up, down, left, right, rectangle
        self.colors = [self.inactive_color, self.inactive_color, self.inactive_color, self.inactive_color, self.inactive_color]
        #objects for menu buttons
        self.buttons = []
        self.buttons.append(self.pygame.Rect(x-7, y-15, 14, 10))
        self.buttons.append(self.pygame.Rect(x-5, y+5, 14, 10))
        self.buttons.append(self.pygame.Rect(x-15, y-5, 10, 14))
        self.buttons.append(self.pygame.Rect(x+5, y-5, 10, 14))
        self.buttons.append(self.pygame.Rect(x-2, y-2, 5, 5))
    
    def handle_event(self, event):
        if event.type == self.pygame.KEYDOWN:        
            if event.key == self.pygame.K_UP: # move table up
                self.tbl.change_position(0, -1)
                self.colors[0] = self.active_color
            elif event.key == self.pygame.K_DOWN: # move table down
                self.tbl.change_position(0, 1)
                self.colors[1] = self.active_color
            elif event.key == self.pygame.K_LEFT: # move table left
                self.tbl.change_position(-1, 0)
                self.colors[2] = self.active_color
            elif event.key == self.pygame.K_RIGHT: # move table right
                self.tbl.change_position(1, 0)
                self.colors[3] = self.active_color
            elif event.key == self.pygame.K_SPACE: # center table
                self.tbl.pos = self.tbl.base_pos[:]
                self.colors[4] = self.active_color
        
        if event.type == self.pygame.KEYUP:
            self.colors = [self.inactive_color, self.inactive_color, self.inactive_color, self.inactive_color, self.inactive_color]
        
        if event.type == self.pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the button rect.
            if self.buttons[0].collidepoint(event.pos):
                self.tbl.change_position(0, -1)
                self.colors[0] = self.active_color                   
            elif self.buttons[1].collidepoint(event.pos):
                self.tbl.change_position(0, 1)
                self.colors[1] = self.active_color                   
            elif self.buttons[2].collidepoint(event.pos):
                self.tbl.change_position(-1, 0)
                self.colors[2] = self.active_color                   
            elif self.buttons[3].collidepoint(event.pos):
                self.tbl.change_position(1, 0)
                self.colors[3] = self.active_color                   
            elif self.buttons[4].collidepoint(event.pos):
                self.tbl.pos = self.tbl.base_pos[:]
                self.colors[4] = self.active_color                   

        if event.type == self.pygame.MOUSEBUTTONUP:
            self.colors = [self.inactive_color, self.inactive_color, self.inactive_color, self.inactive_color, self.inactive_color]

        if event.type == self.pygame.MOUSEMOTION:
            for i in range(len(self.buttons)):
                if self.buttons[i].collidepoint(event.pos):
                    self.colors[i] = self.ready_color
                else:
                    self.colors[i] = self.inactive_color
    def update(self, x, y):
        #In case of resize window we should move navigation
        self.x = x
        self.y = y
        
        self.buttons[0].x = x-7
        self.buttons[0].y = y-15
        self.buttons[1].x = x-5
        self.buttons[1].y = y+5
        self.buttons[2].x = x-15
        self.buttons[2].y = y-5
        self.buttons[3].x = x+5
        self.buttons[3].y = y-5
        self.buttons[4].x = x-2
        self.buttons[4].y = y-2
            
    def draw(self, screen):
        # arrow up
        points = [(self.x-2, self.y-5), (self.x-2, self.y-9), (self.x-7, self.y-9), (self.x, self.y-15), (self.x+7, self.y-9), (self.x+2, self.y-9), (self.x+2, self.y-5)]
        self.pygame.draw.polygon(screen, self.colors[0], points)
        # arrow down
        points = [(self.x-2, self.y+5), (self.x-2, self.y+9), (self.x-5, self.y+9), (self.x, self.y+14), (self.x+5, self.y+9), (self.x+2, self.y+9), (self.x+2, self.y+5)]
        self.pygame.draw.polygon(screen, self.colors[1], points)
        # arrow left
        points = [(self.x-5, self.y-2), (self.x-9, self.y-2), (self.x-9, self.y-5), (self.x-14, self.y), (self.x-9, self.y+5), (self.x-9, self.y+3), (self.x-5, self.y+3)]
        self.pygame.draw.polygon(screen, self.colors[2], points)
        # arrow right
        points = [(self.x+5, self.y-2), (self.x+9, self.y-2), (self.x+9, self.y-5), (self.x+14, self.y), (self.x+9, self.y+5), (self.x+9, self.y+3), (self.x+5, self.y+3)]
        self.pygame.draw.polygon(screen, self.colors[3], points)
        # rectangle
        self.pygame.draw.rect(screen, self.colors[4], self.pygame.Rect(self.x-2, self.y-2, 5, 5))
    
class EndScene(SceneBase):
    """
    The end scene
    """
    def __init__(self, pygame, hands, end_screen):
        SceneBase.__init__(self, pygame)
        self.myfont = None
        self.pickle = None
        self.hands = hands
        self.hs = None
        self.texts = []
        self.texts.append(["", ('c', -120, 'c', -90)]) #place for title
        self.texts.append(["", ('c', -170, 'b', -40)]) #place for instruction
        
        self.end_screen = end_screen
        self.img = None
    
    def set_myfont(self, myfont, pickle):
        self.myfont = myfont
        self.pickle = pickle
        titlefont = self.pygame.font.SysFont("monospace", 50)
        self.texts[0][0] = titlefont.render("Game Over", 1, (255,255,255))
        self.texts[1][0] = self.myfont.render("Press space to start new game or ESC to exit", 1, (255,255,255))

        hs = self.get_high_score(self.pickle)
        y = -20
        for hnd in self.hands:
            self.texts.append([self.myfont.render(str(hnd.name)+" earned "+str(hnd.points)+" points", 1, (255,255,255)), ('c', -100, 'c', y)])
            hs.append([hnd.points, hnd.name])
            y += 15
        
        hs.sort(reverse = True)
        self.hs = hs[:5]
        f = open("hs.dat", "wb")
        self.pickle.dump(self.hs, f, True)
        f.close()        

        try:
            self.img = self.pygame.image.load(self.end_screen)
        except:
            self.img = None
        
        self.started = True

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == self.pygame.KEYDOWN:
                if event.key == self.pygame.K_SPACE:
                    self.SwitchToScene(GameScene(self.pygame))

    def Update(self):
        pass
        
    def Render(self, screen):
        screen.fill((0, 0, 0))
        
        if self.img:
            wi, hi = self.img.get_size()
            w, h = self.pygame.display.get_surface().get_size()
            
            screen.blit(self.img, (round((w-wi)/2), round((h-hi)/2)))

            s = self.pygame.Surface((w, h))
            s.set_alpha(200)
            s.fill((50,50,50))
            screen.blit(s, (0,0))

        x, y = self.find_pos(('c', -115, 'c', -17))
        for h in self.hands:
            self.pygame.draw.rect(screen, tile.Tile.colors(h.color), self.pygame.Rect(x, y, 10, 10), 0)
            y += 15
        
        for i in self.texts:
            screen.blit(i[0], self.find_pos(i[1]))
        
        self.render_high_score(screen, self.hs, self.myfont, ('c', -70, 'b', -180))

if __name__ == "__main__":
    print("This is a module with Scenes for kik game.")
    input("\nPress the enter key to exit.")  
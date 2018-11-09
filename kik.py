# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 11:32:56 2018

@author: Grzegorz Libera
"""

import pygame, pickle
from pygame.locals import *
import tile, hand, table, scene

def main(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height),HWSURFACE|DOUBLEBUF|RESIZABLE)
    clock = pygame.time.Clock()
    myfont = pygame.font.SysFont("monospace", 15)

    active_scene = starting_scene
    active_scene.set_myfont(myfont)
    
    players = [['Red', 0, 'r'],['Green', 0, 'g'],['Blue', 0, 'b'],['Yellow', 0, 'y']]
    
    while active_scene != None:
        
        if not active_scene.started:
            if isinstance(active_scene, scene.SetScene):
                active_scene.set_myfont(myfont, players, pickle)

            if isinstance(active_scene, scene.KeyScene):
                active_scene.set_myfont(myfont)
                
            if isinstance(active_scene, scene.GameScene):
                hands = []
                for player in players:
                    if player[1] != 2:
                        hands.append(hand.Hand([10,100], player))
                
                active_scene.set_data(table.Table('data.txt', tile, [350, 220]), hands, myfont)

            if isinstance(active_scene, scene.EndScene):
                active_scene.set_myfont(myfont, pickle)
        
        pressed_keys = pygame.key.get_pressed()
        
        # Event filtering 
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            elif event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
            
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
            
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        
        if isinstance(active_scene, scene.SetScene):
            players[0][0] = active_scene.input_boxes[0].text.strip()
            players[1][0] = active_scene.input_boxes[1].text.strip()
            players[2][0] = active_scene.input_boxes[2].text.strip()
            players[3][0] = active_scene.input_boxes[3].text.strip()

            players[0][1] = active_scene.toggle_boxes[0].val
            players[1][1] = active_scene.toggle_boxes[1].val
            players[2][1] = active_scene.toggle_boxes[2].val
            players[3][1] = active_scene.toggle_boxes[3].val
        
        active_scene.Render(screen)
        
        active_scene = active_scene.next        

        pygame.display.flip()
        
        clock.tick(fps)


main(640, 480, 60, scene.StartScene(pygame))
pygame.display.quit()
pygame.quit()
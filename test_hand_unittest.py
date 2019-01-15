#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 08:44:08 2019

@author: Grzegorz Libera
"""
import unittest
import hand, tile, table

class TestHand(unittest.TestCase):
    def setUp(self):
        # player needs values: [player name, player type, player color]
        player = ['Red', 0, 'r']
        # hand needs values: start position, player
        self.hand = hand.Hand((0,0), player)
        
    def tearDown(self):
        self.hand = None
        
    # hand.len() count tiles on hand
    
    def test_len_0(self):
        # new created hand should have len = 0
        self.assertEqual(len(self.hand), 0)

    def test_len_2(self):
        # add two hand 2 tiles and check its len
        t1 = tile.Tile(['r','g','g','g','g','b','r','y',1,1,0,0,0,0,1,1])
        t2 = tile.Tile(['r','b','b','b','g','b','y','r',1,1,0,0,1,1,0,0])
        self.hand.add_tile(t1)
        self.hand.add_tile(t2)
        self.assertEqual(len(self.hand), 2)

    # add_tile add tile to hand
    
    def test_add_tile(self):
        # add tile to hand should set some params on tile
        t1 = tile.Tile(['r','g','g','g','g','b','r','y',1,1,0,0,0,0,1,1])
        self.hand.add_tile(t1)
        self.assertEqual(t1.size, self.hand.size)
        pos_on_hand = self.hand.get_pos_on_hand(0)
        self.assertEqual(t1.position[0], pos_on_hand[0])
        self.assertEqual(t1.position[1], pos_on_hand[1])
        self.assertEqual(len(self.hand), 1)
        
    # add_points changes points amount on hand
    
    def test_add_points_0(self):
        # add 0 points shouldn't change amount of points
        points = self.hand.points
        self.hand.add_points(0)
        self.assertEqual(self.hand.points, points)

    def test_add_points_1(self):
        # add 1 points should change amount of points +1
        points = self.hand.points
        points += 1
        self.hand.add_points(1)
        self.assertEqual(self.hand.points, points)

    def test_add_points_m1(self):
        # add -1 points should change amount of points -1
        points = self.hand.points
        points -= 1
        self.hand.add_points(-1)
        self.assertEqual(self.hand.points, points)
        
    # rem_chosen_tile romoves tile from hand
    
    def test_rem_chosen_tile_0(self):
        # no tile on hand
        self.hand.rem_chosen_tile()
        self.assertTrue(self.hand.end)

    def test_rem_chosen_tile_1(self):
        # 1 tile on hand
        t1 = tile.Tile(['r','g','g','g','g','b','r','y',1,1,0,0,0,0,1,1])
        self.hand.add_tile(t1)

        self.hand.rem_chosen_tile()
        self.assertEqual(len(self.hand), 0)
        self.assertTrue(self.hand.end)

    def test_rem_chosen_tile_2(self):
        # 2 tiles on hand
        t1 = tile.Tile(['r','g','g','g','g','b','r','y',1,1,0,0,0,0,1,1])
        t2 = tile.Tile(['r','g','g','g','g','b','r','y',1,1,0,0,0,0,1,1])
        self.hand.add_tile(t1)
        self.hand.add_tile(t2)
        self.hand.set_chosen(1)
        pos_on_hand = self.hand.get_pos_on_hand(0)

        self.hand.rem_chosen_tile()
        self.assertEqual(len(self.hand), 1)
        self.assertEqual(self.hand.chosen, 0)
        self.assertIs(self.hand.get_chosen(), t1)
        self.assertFalse(self.hand.end)
        chosen_tile = self.hand.get_chosen()
        self.assertEqual(chosen_tile.position[0], pos_on_hand[0])
        self.assertEqual(chosen_tile.position[1], pos_on_hand[1])
        
    # set_chosen sets which tile is chosen
    
    def test_set_chosen(self):
        self.hand.set_chosen(1)
        self.assertEqual(self.hand.chosen, 1)
        
    # get_pos_on_hand returns tile position
    
    def test_get_pos_on_hand_0(self):
        self.assertTupleEqual(self.hand.start_position, self.hand.get_pos_on_hand(0))

    def test_get_pos_on_hand_1(self):
        pos_1 = (self.hand.start_position[0], self.hand.start_position[1] + self.hand.size + self.hand.space)
        self.assertTupleEqual(pos_1, self.hand.get_pos_on_hand(1))
        
    # get_chosen returns a chosen tile
    
    def test_get_chosen(self):
        t1 = tile.Tile(['r','g','g','g','g','b','r','y',1,1,0,0,0,0,1,1])
        t2 = tile.Tile(['r','g','g','g','g','b','r','y',1,1,0,0,0,0,1,1])
        self.hand.add_tile(t1)
        self.hand.add_tile(t2)
        
        self.assertIs(self.hand.get_chosen(), t1)  
        self.hand.set_chosen(1)
        self.assertIs(self.hand.get_chosen(), t2)        

    # get_hand returns all tiles from hand
    
    def test_get_hand(self):
        t1 = tile.Tile(['r','g','g','g','g','b','r','y',1,1,0,0,0,0,1,1])
        t2 = tile.Tile(['r','g','g','g','g','b','r','y',1,1,0,0,0,0,1,1])
        self.hand.add_tile(t1)
        self.hand.add_tile(t2)

        self.assertListEqual(self.hand.get_hand(), self.hand.tiles) 
        
    # is_end return ifromation if hand end game
    
    def test_is_end(self):
        self.assertEqual(self.hand.is_end(), self.hand.end)
        
    # find_best_move returns params of best move
    
    def test_find_best_move_1(self):
        # 1 tile
        tab = table.Table('data.txt', tile, [350, 220])
        tab.table = {}
        tt1 = tile.Tile(['b','y','y','y','r','b','y','g',1,0,0,1,1,0,0,1])
        tab.set_on_table((0,0), tt1)
        
        th1 = tile.Tile(['y','b','b','b','y','r','g','g',1,0,0,1,0,1,0,1])
        self.hand.add_tile(th1)
        
        best_pos, best_points, best_pfc = self.hand.find_best_move(tab)
        self.assertEqual(best_pos[0], 0)
        self.assertEqual(best_pos[1], 0)
        self.assertEqual(best_pos[2], 1)
        self.assertTupleEqual(best_pos[3], (0, -1))
        self.assertEqual(best_points, 3)
        self.assertDictEqual(best_pfc, {})

    def test_find_best_move_2(self):
        # field to close
        tab = table.Table('data.txt', tile, [350, 220])
        tab.table = {}
        tt1 = tile.Tile(['b','r','r','g','b','r','y','y',1,0,1,0,1,0,0,1])
        tt2 = tile.Tile(['r','b','g','r','r','r','g','g',1,1,0,0,0,1,1,0])
        tab.set_on_table((0,0), tt1)
        tab.set_on_table((-1,-1), tt2)
        
        th1 = tile.Tile(['b','r','g','b','y','r','g','g',1,0,1,0,0,1,0,1])
        self.hand.add_tile(th1)
        
        best_pos, best_points, best_pfc = self.hand.find_best_move(tab)
        self.assertEqual(best_pos[0], 0)
        self.assertEqual(best_pos[1], 0)
        self.assertEqual(best_pos[2], 1)
        self.assertTupleEqual(best_pos[3], (0, -1))
        self.assertEqual(best_points, 7)
        self.assertDictEqual(best_pfc, {'b':2})
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
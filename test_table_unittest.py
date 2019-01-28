#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 10:02:03 2019

@author: Grzegorz Libera
"""
import unittest
import table, tile, hand

class TestTable(unittest.TestCase):
    def setUp(self):
        # table needs values: data (file with tiles), tile class, position 
        self.table = table.Table('data.txt', tile, [0, 0])
        
    def tearDown(self):
        self.table = None
    
    # new table object should have some parameters
    
    def test_init(self):
        self.assertGreaterEqual(self.table.t_size, 0)
        self.assertListEqual(self.table.pos, [0, 0])
        self.assertListEqual(self.table.base_pos, [0, 0])
        self.assertIsNot(self.table.pos, self.table.base_pos)
        self.assertGreater(len(self.table.tiles), 0)
        self.assertEqual(len(self.table.start_tiles), 4)
        self.assertEqual(len(self.table.table), 4)
        self.assertEqual(len(self.table.posible_moves), 12)
        self.assertFalse(self.table.end)        

    # deal moves tiles from table to hands
    
    def test_deal(self):
        p1 = ['Red', 0, 'r']
        h1 = hand.Hand((0,0), p1)
        p2 = ['Blue', 0, 'b']
        h2 = hand.Hand((0,0), p2)
        
        tile_count = len(self.table.tiles)
        
        self.table.deal([h1, h2], 2)
        
        self.assertEqual(len(self.table.tiles), tile_count - 4)
        self.assertEqual(len(h1), 2)
        self.assertEqual(len(h2), 2)
        
    # set_on_table sets tile on table
    
    def test_set_on_table(self):
        t1 = tile.Tile(['r','g','g','g','g','b','r','y',1,1,0,0,0,0,1,1])
        
        table_count = len(self.table.table)
        pm_count = len(self.table.posible_moves)
        
        self.table.set_on_table((1,0), t1)
        
        self.assertEqual(t1.size, self.table.t_size)
        self.assertEqual(len(self.table.table), table_count + 1)
        self.assertEqual(len(self.table.posible_moves), pm_count + 1)
        self.assertIs(self.table.table[(1,0)], t1)
         
    # change_position moves the table
    
    def test_change_position(self):
        self.table.t_size = 10
        self.table.change_position(1, 0)
        
        self.assertListEqual(self.table.pos, [10, 0])

        self.table.change_position(1, 2)
        self.assertListEqual(self.table.pos, [20, 20])
        
        self.table.change_position(-1, -1)
        self.assertListEqual(self.table.pos, [10, 10])

    # calculate_pm adds possible moves around set coordinates
    
    def test_calculate_pm(self):
        self.table.posible_moves = []
        
        self.table.calculate_pm((1,1))
        self.assertListEqual(self.table.posible_moves, [(0,1), (2,1), (1,0), (1,2)])
        
        self.table.posible_moves.remove((1,0))
        self.table.calculate_pm((1,0))
        self.assertListEqual(self.table.posible_moves, [(0,1), (2,1), (1,2), (0,0), (2,0)])

    # is_on_pos_move checks if set position is on posible move
    
    def test_is_on_pos_move(self):
        self.assertFalse(self.table.is_on_pos_move((10,10)))
        self.assertFalse(self.table.is_on_pos_move((-1,50)))
        self.assertFalse(self.table.is_on_pos_move((41,50)))
        self.assertFalse(self.table.is_on_pos_move((10,39)))
        self.assertFalse(self.table.is_on_pos_move((10,81)))
        self.assertTupleEqual(self.table.is_on_pos_move((10,50)), (0,1))
        self.assertTupleEqual(self.table.is_on_pos_move((0,50)), (0,1))
        self.assertTupleEqual(self.table.is_on_pos_move((40,50)), (0,1))
        self.assertTupleEqual(self.table.is_on_pos_move((10,40)), (0,1))
        self.assertTupleEqual(self.table.is_on_pos_move((10,80)), (0,1))
        
    # is_on_correct_move checks if set tile on coor is correct
    
    def test_is_on_correct_move(self):
        self.table.table = {}
        self.table.posible_moves = []

        t1 = tile.Tile(['g','g','y','y','g','b','r','y',1,0,0,1,0,0,1,1])
        points, pfc = self.table.is_on_correct_move((0,0), t1)
        self.assertEqual(points, 0)
        self.assertDictEqual(pfc, {})
        
        self.table.set_on_table((0,0), t1)
        t2 = tile.Tile(['r','b','g','y','r','r','r','r',0,0,1,1,1,1,0,0])
        points, pfc = self.table.is_on_correct_move((0,1), t2)
        self.assertFalse(points)
        self.assertDictEqual(pfc, {})
        points, pfc = self.table.is_on_correct_move((0,-1), t2)
        self.assertEqual(points, 3)
        self.assertDictEqual(pfc, {})
        
        self.table.set_on_table((0,-1), t2)
        t3 = tile.Tile(['r','b','y','g','r','r','r','r',1,0,0,1,1,1,0,0])
        points, pfc = self.table.is_on_correct_move((1,0), t3)
        self.assertEqual(points, 4)
        self.assertDictEqual(pfc, {'g':2})
        
    # is_field checks if field is closed
    
    def test_is_field(self):
        self.table.table = {}
        self.table.posible_moves = []

        t1 = tile.Tile(['g','g','y','y','g','b','r','y',1,0,0,1,0,0,1,1])
        self.table.set_on_table((0,0), t1)
        t2 = tile.Tile(['r','b','g','y','r','r','r','r',0,0,1,1,1,1,0,0])
        self.table.checked = [] #clear a list of checked tiles
        self.assertFalse(self.table.is_field((0,-1), 2, t2))        

        self.table.set_on_table((0,-1), t2)
        t3 = tile.Tile(['r','b','y','g','r','r','r','r',1,0,0,1,1,1,0,0])
        self.table.checked = [] #clear a list of checked tiles
        self.assertEqual(self.table.is_field((1,0), 3, t3), 2)

        t3.rotate_tile('l')
        t3.rotate_tile('l')
        self.table.checked = [] #clear a list of checked tiles
        self.assertEqual(self.table.is_field((0,-2), 2, t3), 1)

        self.table.table = {}
        self.table.posible_moves = []
        
        t1 = tile.Tile(['g','g','y','y','g','b','r','y',1,0,0,1,0,0,1,1])
        t2 = tile.Tile(['g','g','y','y','g','b','r','y',1,0,0,1,0,0,1,1])
        t3 = tile.Tile(['g','g','y','y','g','b','r','y',1,0,0,1,0,0,1,1])
        t4 = tile.Tile(['g','g','y','y','g','b','r','y',1,0,0,1,0,0,1,1])
        self.table.set_on_table((0,0), t1)
        t2.rotate_tile('r')
        self.table.set_on_table((0,-1), t2)
        t3.rotate_tile('l')
        self.table.set_on_table((1,0), t3)
        t4.rotate_tile('l')
        t4.rotate_tile('l')
        self.table.checked = [] #clear a list of checked tiles
        self.assertEqual(self.table.is_field((1,-1), 3, t4), 4)

    # get_coor_to_check
    
    def test_get_coor_to_check(self):
        self.assertTupleEqual(self.table.get_coor_to_check((0,0), 0), (0, -1))
        self.assertTupleEqual(self.table.get_coor_to_check((0,0), 1), (1, 0))
        self.assertTupleEqual(self.table.get_coor_to_check((0,0), 2), (0, 1))
        self.assertTupleEqual(self.table.get_coor_to_check((0,0), 3), (-1, 0))
        
        with self.assertRaises(ValueError):
            self.table.get_coor_to_check((0,0), 4)
            
    # get_side
    
    def test_get_side(self):
        self.assertEqual(self.table.get_side(0, 1), 1)
        self.assertEqual(self.table.get_side(2, 2), 0)
        self.assertEqual(self.table.get_side(0, -1), 3)

if __name__ == '__main__':
    unittest.main(verbosity=2)
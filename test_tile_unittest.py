#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 09:49:56 2019

@author: Grzegorz Libera
"""

import unittest
import tile

class TestTile(unittest.TestCase):
    def setUp(self):
        # tile needs some data
        self.tile = tile.Tile(['r','g','g','g','g','b','r','y',1,1,0,0,0,0,1,1])
        
    def tearDown(self):
        self.tile = None

    # new tile object should have some parameters
    
    def test_init(self):
        self.assertListEqual(self.tile.colors_1, ['r','g','g','g'])
        self.assertListEqual(self.tile.colors_2, ['g','b','r','y'])
        self.assertListEqual(self.tile.dots_1, [1,1,0,0])
        self.assertListEqual(self.tile.dots_2, [0,0,1,1])
        self.assertGreaterEqual(self.tile.size, 0)
        self.assertEqual(self.tile.side, 1)
        self.assertEqual(self.tile.rotate, 0)
        self.assertListEqual(self.tile.position, [0, 0])

    # flip_tile should change tile.side
    
    def test_flip_tile(self):
        self.tile.flip_tile()
        self.assertEqual(self.tile.side, 2)
        self.tile.flip_tile()
        self.assertEqual(self.tile.side, 1)

    # rotate_tile should change tile.rotate
    
    def test_rotate_tile_l(self):
        self.tile.rotate_tile('l')
        self.assertEqual(self.tile.rotate, 1)
        self.tile.rotate_tile('l')
        self.assertEqual(self.tile.rotate, 2)
        self.tile.rotate_tile('l')
        self.assertEqual(self.tile.rotate, 3)
        self.tile.rotate_tile('l')
        self.assertEqual(self.tile.rotate, 0)

    def test_rotate_tile_r(self):
        self.tile.rotate_tile('r')
        self.assertEqual(self.tile.rotate, 3)
        self.tile.rotate_tile('r')
        self.assertEqual(self.tile.rotate, 2)
        self.tile.rotate_tile('r')
        self.assertEqual(self.tile.rotate, 1)
        self.tile.rotate_tile('r')
        self.assertEqual(self.tile.rotate, 0)
        
    # get_tile should return 2 lists necessary to draw tile
    
    def test_get_tile(self):
        cs, ds = self.tile.get_tile()
        self.assertListEqual(cs, ['r','g','g','g'])
        self.assertListEqual(ds, [1,1,0,0])

        self.tile.rotate_tile('l')
        cs, ds = self.tile.get_tile()
        self.assertListEqual(cs, ['g','g','g','r'])
        self.assertListEqual(ds, [1,0,0,1])
        
        self.tile.flip_tile()
        cs, ds = self.tile.get_tile()
        self.assertListEqual(cs, ['b','r','y','g'])
        self.assertListEqual(ds, [0,1,1,0])
        
    # set_position should change tile.position
    
    def test_set_position(self):
        self.tile.set_position(2, 3)
        self.assertListEqual(self.tile.position, [2, 3])
        
    # set_size should change tile.size
    
    def test_set_size(self):
        self.tile.set_size(40)
        self.assertEqual(self.tile.size, 40)
        
    # is_clicked checks if pos is on tile
    
    def test_is_clicked(self):
        self.tile.set_position(0, 0)
        self.tile.set_size(40)
        self.assertFalse(self.tile.is_clicked([-1,-1]))
        self.assertFalse(self.tile.is_clicked([-1,1]))
        self.assertFalse(self.tile.is_clicked([1,-1]))
        self.assertFalse(self.tile.is_clicked([41,41]))
        self.assertFalse(self.tile.is_clicked([41,30]))
        self.assertFalse(self.tile.is_clicked([30,41]))
        
        self.assertTrue(self.tile.is_clicked([0, 0]))
        self.assertTrue(self.tile.is_clicked([40, 40]))
        self.assertTrue(self.tile.is_clicked([40, 0]))
        self.assertTrue(self.tile.is_clicked([0, 40]))
        self.assertTrue(self.tile.is_clicked([10, 20]))
        
    # get_mouse_pos returns relative pos on tile
    
    def test_get_mouse_pos(self):
        self.tile.set_position(0, 0)
        x, y = self.tile.get_mouse_pos([10,5])
        self.assertListEqual([x,y], [10,5])

        self.tile.set_position(10, 20)
        x, y = self.tile.get_mouse_pos([20,50])
        self.assertListEqual([x,y], [10,30])
            
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
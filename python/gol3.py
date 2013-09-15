#!/usr/bin/env python
# encoding: utf-8
"""
gol3.py

Use numpy array to store grid state

Created by Mahmood Hanif on 2013-09-13.
Copyright (c) 2013 Teknifi. All rights reserved.
"""

import unittest
import numpy as np


class GameOfLife:
    def __init__(self, gridSize=0):
        self.grid = np.zeros((gridSize, gridSize), np.bool_)
        self.ALIVE_SYMBOL = 'x'
        self.DEAD_SYMBOL  = '.'
        
    def gridSize(self):
        return self.grid.shape[0]
        
    def setAlive(self, alivePoints):
        for pt in alivePoints:
            self.grid[pt] = True
            
    def isAlive(self, x, y):
        return self.grid[x,y]
        
    def numLivingNeighbors(self,x,y):
        count = 0
        xminus1 = max(0, x-1)
        yminus1 = max(0, y-1)
        xplus1  = min(self.gridSize()-1, x+1)
        yplus1  = min(self.gridSize()-1, y+1)
        for nx in range(xminus1, xplus1+1):
            for ny in range(yminus1, yplus1+1):
                if nx!=x or ny!=y:
                    count += 1 if self.grid[nx,ny] else 0
        return count
        
    def next(self):
        toDead = []
        toAlive = []
        it = np.nditer(self.grid, flags=['multi_index'])
        while not it.finished:
            x, y = it.multi_index
            neighbors = self.numLivingNeighbors(x,y)
            isLiving = it[0]
            if isLiving and (neighbors < 2 or neighbors > 3):
                toDead.append((x,y))
            if not isLiving and neighbors == 3:
                toAlive.append((x,y))
            it.iternext()
        for cell in toDead:
            self.grid[cell] = False
        for cell in toAlive:
            self.grid[cell] = True
            
    def __repr__(self):
        count = 0
        r = ''
        for cell in np.nditer(self.grid):
            if count and (count % self.gridSize()) == 0:
                r += '\n'
            count += 1
            r += self.ALIVE_SYMBOL if cell else self.DEAD_SYMBOL
        return r+'\n'

class TestGameOfLife(unittest.TestCase):
    def setUp(self):
        pass

    def shouldEqual(self, expected, received):
        s = "Expected: %s, Received: %s" % (str(expected), str(received))
        self.assertEqual(expected, received, msg=s)
        
    def testDefaultGrid(self):
        game = GameOfLife()
        self.shouldEqual(0, game.gridSize())

    def testEmptyGrid3(self):
        game = GameOfLife(3)
        self.shouldEqual(3, game.gridSize())
        
    def testPrintEmptyGrid3(self):
        game = GameOfLife(3)
        self.shouldEqual('...\n...\n...\n', repr(game))

    def testInitializedGrid(self):
        game = GameOfLife(3)
        game.setAlive([(0,0),(1,1),(2,2)])
        self.shouldEqual('x..\n.x.\n..x\n', repr(game))

    def testOutOfBoundsThrows(self):
        game = GameOfLife(3)
        self.assertRaises(IndexError, game.setAlive, [(4,4)])

    def testUnderpopulation(self):
        game = GameOfLife(3)
        game.setAlive([(0,0),(1,1),(2,2)])
        game.next()
        self.shouldEqual(False, game.isAlive(0,0))
        self.shouldEqual(False, game.isAlive(2,2))
        
    def testOvercrowding(self):
        game = GameOfLife(3)
        game.setAlive([(0,0),(0,1),(0,2),(1,0),(1,1)])
        game.next()
        self.shouldEqual(False, game.isAlive(0,1))
        self.shouldEqual(False, game.isAlive(1,1))

    def testBirth(self):
        game = GameOfLife(3)
        game.setAlive([(0,0),(0,1),(0,2)])
        game.next()
        self.shouldEqual(True, game.isAlive(1,1))
        
if __name__ == '__main__':
    unittest.main()
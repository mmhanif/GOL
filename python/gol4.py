#!/usr/bin/env python
# encoding: utf-8
"""
gol4.py

Use numpy array to store grid state. Use strides to define neighbor windows for each cell.
Create grid one cell bigger in each direction in order to handle edge conditions (iteration starts from 1,1 rather than 0,0)

Created by Mahmood Hanif on 2013-09-13.
Copyright (c) 2013 Teknifi. All rights reserved.
"""

import unittest
import numpy as np
from numpy.lib import stride_tricks

class GameOfLife:
    def __init__(self, gridSize=0):
        "Create internal grid with 2 extra elements in x and y directions, to allow for easy windowing"
        self.grid = np.zeros((gridSize+2, gridSize+2), np.bool_)
        if gridSize > 0:
            self._initWindows()
        self.ALIVE_SYMBOL = 'x'
        self.DEAD_SYMBOL  = '.'
        
    def _initWindows(self):
        '''Create a matrix of 3x3 windows in to self.grid. 
        Center of first window is grid cell (1,1). Center of last window is (gridSize-1,gridSize-1)'''
        strides = self.grid.strides
        windowXSize = 3
        windowYSize = 3
        numWindowsX = self.grid.shape[0] - 2
        numWindowsY = self.grid.shape[0] - 2
        self.windows = stride_tricks.as_strided(
                            self.grid, 
                            shape=(numWindowsX, numWindowsY, windowXSize, windowYSize), 
                            strides=strides + strides)
        
    def gridSize(self):
        "Returns gridSize as far as user is concerned"
        return self.grid.shape[0]-2

    def _toInternalPoint(self, x,y):
        return (x+1,y+1)
        
    def setAlive(self, alivePoints):
        for x,y in alivePoints:
            self.grid[self._toInternalPoint(x,y)] = True
            
    def isAlive(self, x, y):
        ix, iy = self._toInternalPoint(x,y)
        return self._isAlive(ix,iy)
        
    def _isAlive(self, ix, iy):
        return self.grid[ix,iy]

    def _windowFor(self, ix, iy):
        return self.windows[ix-1,iy-1,:]

    def _numLivingNeighbors(self,ix,iy):
        window = self._windowFor(ix,iy)
        numLiving = np.count_nonzero(window)
        if self._isAlive(ix,iy):
            numLiving -= 1
        return numLiving
        
    def isUnderpopulated(self, neighborCount, isLiving):
        return isLiving and neighborCount < 2
        
    def isOvercrowded(self, neighborCount, isLiving):
        return isLiving and neighborCount > 3
        
    def isReborn(self, neighborCount, isLiving):
        return (not isLiving) and neighborCount == 3
        
    def next(self):
        toDead = []
        toAlive = []
        maxIndex = self.gridSize()+1
        for ix,iy in self._gridPoints():
            neighbors = self._numLivingNeighbors(ix,iy)
            isLiving = self._isAlive(ix,iy)
            if self.isUnderpopulated(neighbors, isLiving) or self.isOvercrowded(neighbors, isLiving):
                toDead.append((ix,iy))
            if self.isReborn(neighbors, isLiving):
                toAlive.append((ix,iy))
        for cell in toDead:
            self.grid[cell] = False
        for cell in toAlive:
            self.grid[cell] = True

    def _gridPoints(self):
        maxIndex = self.gridSize()+1
        return [(x,y) for x in range(1,maxIndex) for y in range(1,maxIndex)]
            
    def __repr__(self):
        count = 0
        r = ''
        sz = self.gridSize()
        for ix,iy in self._gridPoints():
            if count and (count % sz) == 0:
                r += '\n'
            count += 1
            r += self.ALIVE_SYMBOL if self._isAlive(ix,iy) else self.DEAD_SYMBOL
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
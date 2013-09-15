#!/usr/bin/env python
# encoding: utf-8
"""
gol.py

Created by Mahmood Hanif on 2013-09-06.
Copyright (c) 2013 Teknifi. All rights reserved.

Naive implementation of Conway's Game of Life. Allocates a list of lists to represent the game grid.
"""

import sys
import os
import unittest


class GameOfLife:
    ALIVE_SYMBOL = 'x'
    ALIVE = 1
    DEAD = 0
    
    def __init__(self, gridSize=0):
        self.gridSize = gridSize
        self.grid = []
        for nRows in range(gridSize):
            self.grid.append([self.DEAD] * gridSize)
    
    def setAlive(self, alivePoints):
        for (x,y) in alivePoints:
            self.grid[x][y] = self.ALIVE
    
    def nRows(self):
        return len(self.grid)
    
    def nCols(self):
        return len(self.grid[0]) if self.grid else 0
    
    def isAlive(self, x, y):
        return bool(self.grid[x][y])

    def isUnderpopulated(self, neighborCount):
        return neighborCount < 2
        
    def isOvercrowded(self, neighborCount):
        return neighborCount > 3
        
    def isReborn(self, x, y, neighborCount):
        return (not self.isAlive(x, y)) and (neighborCount == 3)
        
    def next(self):
        toDead = []
        toAlive = []
        for nRow in range(self.nRows()):
            for nCol in range(self.nCols()):
                nc = self.neighborCount(nRow, nCol)
                if self.isUnderpopulated(nc) or self.isOvercrowded(nc):
                    toDead.append((nRow,nCol))
                if self.isReborn(nRow, nCol, nc):
                    toAlive.append((nRow,nCol))
        for (x,y) in toDead:
            self.grid[x][y] = self.DEAD
        for (x,y) in toAlive:
            self.grid[x][y] = self.ALIVE

    def neighbors(self, x, y):
        minx = max(0,x-1)
        miny = max(0,y-1)
        maxx = min(x+1, self.nRows()-1)
        maxy = min(y+1, self.nCols()-1)
        neighbors = []
        for nx in range(minx, maxx+1):
            for ny in range(miny, maxy+1):
                if nx!=x or ny!=y:
                    neighbors.append((nx,ny))
        return neighbors

    def neighborCount(self, x, y):
        neighborCount = 0
        for (nx, ny) in self.neighbors(x,y):
            if self.isAlive(nx, ny):
                neighborCount += 1
        return neighborCount 
    
    def __repr__(self):
        r = ""
        for row in self.grid:
            for cell in row:
                r += self.ALIVE_SYMBOL if cell else "."
            r += "\n"
        return r



class TestGameOfLife(unittest.TestCase):
    def setUp(self):
        pass
    
    def shouldEqual(self, expected, received):
        s = "Expected: %s, Received: %s" % (str(expected), str(received))
        self.assertEqual(expected, received, msg=s)
    
    def testDefaulGridCreation(self):
        game = GameOfLife()
        grid = game.grid
        assert(grid == [])
    
    def testGridCreationSize6(self):
        sz = 6
        game = GameOfLife(sz)
        grid = game.grid
        self.assertEqual(len(grid),sz)
        for row in grid:
            self.assertEqual(len(row),sz)
    
    def testGridInitialization(self):
        game = GameOfLife(6)
        alive = [(1,1), (1,2), (2,1), (2,2)]
        game.setAlive(alive)
        for nRow in range(game.nRows()):
            for nCol in range(game.nCols()):
                self.shouldEqual((nRow, nCol) in alive, game.isAlive(nRow,nCol))
    
    def testPrintDefaultGrid(self):
        game = GameOfLife()
        r = repr(game)
        self.assertEqual(r, "")
    
    def testPrintEmptyGrid3(self):
        game = GameOfLife(3)
        r = repr(game)
        self.assertEqual(r, '...\n...\n...\n')
    
    def testPrintSinglePointGrid3(self):
        game = GameOfLife(3)
        game.setAlive([(1,1)])
        r = repr(game)
        e = '...\n.%s.\n...\n' % game.ALIVE_SYMBOL
        self.shouldEqual(e, r)

    def testUnderpopulation(self):
        # Any live cell with fewer than 2 live neighbors dies
        game = GameOfLife(3)
        points = [(0,0), (1,1), (2,2)]
        game.setAlive(points)
        
        game.next()
        
        self.shouldEqual(False, game.isAlive(0, 0))
        self.shouldEqual(True,  game.isAlive(1, 1))
        self.shouldEqual(False, game.isAlive(2, 2))

    def testOvercrowding(self):
        # Any live cell with more than 3 live neighbors dies
        game = GameOfLife(3)
        points = [(0,0), (0,1), (0,2), (1,0), (1,1)]
        game.setAlive(points)
        
        game.next()
        
        self.shouldEqual(True,  game.isAlive(0, 0))
        self.shouldEqual(False, game.isAlive(0, 1))
        self.shouldEqual(True,  game.isAlive(0, 2))
        self.shouldEqual(True,  game.isAlive(1, 0))
        self.shouldEqual(False, game.isAlive(1, 1))

    def testResurrection(self):
        # Any dead cell with exactly 3 live neighbors comes alive
        game = GameOfLife(3)
        points = [(0,0), (0,1), (0,2)]
        game.setAlive(points)
        
        game.next()
        
        self.shouldEqual(True, game.isAlive(1, 1))


if __name__ == '__main__':
    unittest.main()
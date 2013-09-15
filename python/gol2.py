#!/usr/bin/env python
# encoding: utf-8
"""
gol2.py

A second implementation of Conway's Game of Life. Uses a list to keep track of only those cells that are alive.

Created by Mahmood Hanif on 2013-09-12.
Copyright (c) 2013 Teknifi. All rights reserved.
"""

import unittest


class GameOfLife:
    def __init__(self, gridSize=0):
        self.grid_size = gridSize
        self.living = []
        self.ALIVE = 'x'
        self.DEAD = '.'
        
    def gridSize(self):
        return self.grid_size
        
    def isAlive(self, x, y):
        return (x, y) in self.living
        
    def cellRepr(self, x, y):
        return self.ALIVE if self.isAlive(x,y) else self.DEAD

    def setAlive(self, points):
        minPt = (0,0)
        maxPt = (self.grid_size-1, self.grid_size-1)
        for pt in points:
            if pt >= minPt and pt <= maxPt:
                self.living.append(pt)
            else:
                raise IndexError(pt)

    def neighbors(self, x, y):
        neighborList = []
        xminus1 = max(0, x-1)
        yminus1 = max(0, y-1)
        xplus1  = min(x+1, self.grid_size-1)
        yplus1  = min(y+1, self.grid_size-1)
        for nx in range(xminus1, xplus1+1):
            for ny in range(yminus1, yplus1+1):
                if nx!=x or ny!=y:
                    neighborList.append((nx, ny))
        return neighborList

    def livingNeighbors(self, x, y):
        return [(nx, ny) for (nx, ny) in self.neighbors(x, y) if self.isAlive(nx,ny)]

    def deadNeighbors(self, x, y):
        return [(nx, ny) for (nx, ny) in self.neighbors(x, y) if not self.isAlive(nx,ny)]

    def neighborCount(self, x, y):
        return len(self.livingNeighbors(x,y))
        
    def next(self):
        toDead = []
        birthCandidates = {}
        for (x, y) in self.living:
            if self.neighborCount(x,y) < 2:
                toDead.append((x,y))
            if self.neighborCount(x,y) > 3:
                toDead.append((x,y))
            for pt in self.deadNeighbors(x, y):
                livingNeighborCount = birthCandidates.setdefault(pt, 0)
                birthCandidates[pt] = livingNeighborCount + 1
        for pt in toDead:
            self.living.remove(pt)
        for pt, livecount in birthCandidates.iteritems():
            if livecount == 3:
                self.living.append(pt)
        
    def __repr__(self):
        r = ''
        for nRow in range(self.grid_size):
            r += ''.join([self.cellRepr(nRow, nCol) for nCol in range(self.grid_size)])
            r += '\n'
        return r
                    


class TestGameOfLife(unittest.TestCase):
    def setUp(self):
        pass
    
    def shouldEqual(self, expected, received):
        s = "Expected: %s, Received: %s" % (str(expected), str(received))
        self.assertEqual(expected, received, msg=s)
        
    def testInitializeEmptyGrid(self):
        game = GameOfLife()
        self.shouldEqual(0, game.gridSize())

    def testPrintEmptyGrid(self):
        game = GameOfLife()
        self.shouldEqual('', repr(game))
        
    def testPrintInitializedGrid(self):
        game = GameOfLife(3)
        game.setAlive([(0,0), (0,1), (1,1)])
        self.shouldEqual('xx.\n.x.\n...\n', repr(game))

    def testOutOfBoundsPointThrows(self):
        game = GameOfLife(3)
        self.assertRaises(IndexError, game.setAlive, [(4,4)])

    def testNeighbors(self):
        game = GameOfLife(3)
        neighbors = game.neighbors(0,0)
        self.assertListEqual([(0,1), (1,0), (1,1)], neighbors)

    def testUnderpopulation(self):
        game = GameOfLife(3)
        game.setAlive([(1,1), (1,2)])
        game.next()
        self.shouldEqual(False, game.isAlive(1,1))
        self.shouldEqual(False, game.isAlive(1,2))
        
    def testOvercrowding(self):
        game = GameOfLife(3)
        game.setAlive([(0,0), (0,1), (0,2), (1,0), (1,2)])
        game.next()
        self.shouldEqual(False, game.isAlive(0,1))
        
    def testBirth(self):
        print "testBirth\n"
        game = GameOfLife(3)
        game.setAlive([(0,0), (0,1), (0,2)])
        game.next()
        self.shouldEqual(True, game.isAlive(1,1))
        
if __name__ == '__main__':
    unittest.main()
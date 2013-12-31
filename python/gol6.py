#!/usr/bin/env python
# encoding: utf-8
"""
gol6.py

Implementation of Conway's Game of Life that supports an infinite grid.
Uses a list to keep track of only those cells that are alive.

Created by Mahmood Hanif on 2013-12-14.
Copyright (c) 2013 Teknifi. All rights reserved.
"""

from collections import namedtuple
import unittest

class Cell(namedtuple('Cell', ['x', 'y'], verbose=False)):

    def neighbors(self):
        return [Cell(self.x-xd,self.y-yd) for xd in range(-1,2) for yd in range(-1,2) if (xd,yd) != (0,0)]

    def numLivingNeighbors(self, game):
        return len(self.livingNeighbors(game))

    def livingNeighbors(self, game):
        return [neighbor for neighbor in self.neighbors() if game.isAlive(neighbor)]

    def isLonely(self, game):
        return self.numLivingNeighbors(game) < 2

    def isOvercrowded(self, game):
        return self.numLivingNeighbors(game) > 3


def shouldLive(livingNeighborCount, isAlive):
    return (livingNeighborCount == 3) or ((livingNeighborCount ==2) if isAlive else False)

class GameOfLife(object):

    def __init__(self, initialLiving=[]):
        self.living = list()
        self.living.extend(initialLiving)
        self.ALIVE = 'x'
        self.DEAD = '.'

    def numLivingCells(self):
        return len(self.living)

    def isAlive(self, cell):
        return cell in self.living

    def allLivingCellsAndNeighbors(self):
        allCells = set([neighbor for cell in self.living for neighbor in cell.neighbors()])
        allCells.update(self.living)
        return allCells

    def allCellsWithCounts(self):
        return [(cell, cell.numLivingNeighbors(self)) for cell in self.allLivingCellsAndNeighbors()]

    def next(self):
        self.living = [cell for (cell, count) in self.allCellsWithCounts() if shouldLive(count, self.isAlive(cell))]

    def gridBounds(self):
        xs = [cell.x for cell in self.living]
        ys = [cell.y for cell in self.living]
        return ( Cell( min(xs), min(ys) ), Cell( max(xs), max(ys)) )

    def printGrid(self):
        (bottomRight, topLeft) = self.gridBounds()
        for cell in sorted(self.living):
            print cell

    def cellRepr(self, cell):
        return self.ALIVE if self.isAlive(cell) else self.DEAD

    def __repr__(self):
        r = ''
        (br, tl) = self.gridBounds()
        for nRow in range(tl.x, br.x-1, -1):
            for nCol in range(br.y, tl.y+1, 1):
                r += self.cellRepr(Cell(nRow, nCol))
            r += '\n'
        return r




class TestGameOfLife(unittest.TestCase):
    def setUp(self):
        pass

    def shouldEqual(self, expected, received):
        s = "Expected: %s, Received: %s" % (str(expected), str(received))
        self.assertEqual(expected, received, msg=s)

    def testEmptyGrid(self):
        game = GameOfLife()
        self.assertEqual(game.numLivingCells(), 0)

    def testGridInitialization(self):
        game = GameOfLife([Cell(0,0), Cell(1, 0), Cell(-1, -1)])
        self.shouldEqual(3, game.numLivingCells())
        self.shouldEqual(True, game.isAlive(Cell(0,0)))
        self.shouldEqual(True, game.isAlive(Cell(1,0)))
        self.shouldEqual(True, game.isAlive(Cell(-1,-1)))
        self.shouldEqual(False, game.isAlive(Cell(0,1)))

    def testLonelyCellDies(self):
        lonely = Cell(0,0)
        game = GameOfLife([lonely])

        self.shouldEqual(True, game.isAlive(lonely))
        game.next()
        self.shouldEqual(False, game.isAlive(lonely))

    def testOvercrowdedCellDies(self):
        '''
                X            X
              X X X   ->   X . X
                X            X
        '''
        game = GameOfLife([ Cell(0,0), Cell(0,1), Cell(0,-1), Cell(1,0), Cell(-1,0) ])
        print("\n")
        print(game)
        game.next()
        print("\n")
        print(game)
        self.shouldEqual(False, game.isAlive(Cell(0,0)))
        self.shouldEqual(True, game.isAlive(Cell(1,0)))

    def testDeadCellComesToLife(self):
        '''
                X            X
              X . X   ->   . X .

        '''
        game = GameOfLife([ Cell(0,1), Cell(0,-1), Cell(1,0)])
        print("\n")
        print(game)
        game.next()
        print("\n")
        print(game)
        self.shouldEqual(True, game.isAlive(Cell(0,0)))
        self.shouldEqual(False, game.isAlive(Cell(-1,0)))

if __name__ == '__main__':
    unittest.main()
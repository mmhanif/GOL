#!/usr/bin/env python
# encoding: utf-8
"""
gol7.py

Implementation of Conway's Game of Life that supports an infinite grid.
Uses a list to keep track of only those cells that are alive.

Only does one pass through all living cells and their neighbors in order
to optimize performance.

Created by Mahmood Hanif on 2013-12-14.
Copyright (c) 2013 Teknifi. All rights reserved.
"""

from collections import namedtuple, Counter
import unittest

class Cell(namedtuple('Cell', ['x', 'y'], verbose=False)):

    def neighbors(self):
        return [Cell(self.x-xd,self.y-yd) for xd in range(-1,2) for yd in range(-1,2) if (xd,yd) != (0,0)]

    def livingAndDeadNeighbors(self, game):
        living, dead = ([], [])
        for cell in self.neighbors():
            living.append(cell) if game.isAlive(cell) else dead.append(cell)
        return (living, dead)

def shouldLive(livingNeighborCount, isAlive):
    '''
        Game of life rules:

        1. If cell is alive and has less than 2 living neighbors it dies
        2. If cell is alive and has more than 3 living neighbors it dies
        3. If cell is alive and has either 2 or 3 living neighbors it lives
        4. If cell is dead and has exactly 3 living neighbors it lives

        This translates to:
        num living neighbors = <2 => Dead
                                2 => Alive if already Alive else Dead
                                3 => Alive
                               >3 => Dead

    '''
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

    def allCellsWithCounts(self):
        '''
        Return dictionary where:
            key = (cell, alive) where alive is a boolean flag indicating if cell is alive
            value = count of living neighbors of cell

        Note that the dictionary can never contain both a (cell, True) and (cell, False)
        key at the same time for any given cell.
        '''
        cellCount = Counter()
        for cell in self.living:
            ln, dn = cell.livingAndDeadNeighbors(self)
            cellCount[(cell, True)] = len(ln)
            for deadCell in dn:
                cellCount[(deadCell, False)] += 1
        return cellCount

    def next(self):
        self.living = [cell for ((cell, alive), count) in self.allCellsWithCounts().iteritems() if shouldLive(count, alive)]

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
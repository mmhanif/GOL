#!/usr/bin/env python
# encoding: utf-8
"""
gol8.py

Functional implementation of Conway's Game of Life that supports an infinite grid.

Uses a list to keep track of only those cells that are alive. Only does one pass through
all living cells and their neighbors in order to optimize performance.

Created by Mahmood Hanif on 2013-12-14.
Copyright (c) 2013 Teknifi. All rights reserved.
"""

from collections import namedtuple, Counter
import unittest

class Cell(namedtuple('Cell', ['x', 'y'], verbose=False)):
    pass


def neighbors(cell):
    return [Cell(cell.x-xd,cell.y-yd) for xd in range(-1,2) for yd in range(-1,2) if (xd,yd) != (0,0)]

def isAlive(cell, board):
    return cell in board

def _livingAndDeadNeighbors(homeCell, board):
    return [ (cell, isAlive(cell, board)) for cell in neighbors(homeCell)]

def livingAndDeadNeighbors(homeCell, board):
    allN = _livingAndDeadNeighbors(homeCell, board)
    living = [cell for (cell, alive) in allN if alive]
    dead   = [cell for (cell, alive) in allN if not alive]
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

def allCellsWithCounts(livingCells):
    '''
    Return dictionary where:
        key = (cell, alive) where alive is a boolean flag indicating if cell is alive
        value = count of living neighbors of cell

    Note that the dictionary can never contain both a (cell, True) and (cell, False)
    key at the same time for any given cell.

    Note 2 - This uses a mutable data structure, so is not strictly FP
    '''
    cellCount = Counter()
    for cell in livingCells:
        ln, dn = livingAndDeadNeighbors(cell, livingCells)
        cellCount[(cell, True)] = len(ln)
        for deadCell in dn:
            cellCount[(deadCell, False)] += 1
    return cellCount

def nextBoard(livingCells=[]):
    return [cell for ((cell, alive), count) in allCellsWithCounts(livingCells).iteritems() if shouldLive(count, alive)]


class TestGameOfLife(unittest.TestCase):
    def setUp(self):
        pass

    def shouldEqual(self, expected, received):
        s = "Expected: %s, Received: %s" % (str(expected), str(received))
        self.assertEqual(expected, received, msg=s)

    def testEmptyGrid(self):
        self.assertEqual(len(nextBoard()), 0)

    def testLonelyCellDies(self):
        lonely = [Cell(0,0)]
        self.shouldEqual(0, len(nextBoard(lonely)))

    def testCellsWithThreeNeighborsLive(self):
        initial = [Cell(0,0), Cell(0,1), Cell(1,0), Cell(1,1)]
        self.shouldEqual(set(initial), set(nextBoard(initial)))

    def testOvercrowdedCellDies(self):
        '''
                X          X X X
              X X X   ->   X . X
                X          X X X
        '''
        initial  = [ Cell(0,0), Cell(0,1), Cell(0,-1), Cell(1,0), Cell(-1,0) ]
        expected = [ Cell(1,-1), Cell(1,0), Cell(1,1), Cell(0,1), Cell(0,-1), Cell(-1,-1), Cell(-1,0), Cell(-1,1)]
        self.shouldEqual(set(expected), set(nextBoard(initial)))

    def testDeadCellComesToLife(self):
        '''
                X            X
              X . X   ->   . X .

        '''
        initial  = [ Cell(0,1), Cell(0,-1), Cell(1,0)]
        expected = [ Cell(0,0), Cell(1,0)]
        self.shouldEqual(set(expected), set(nextBoard(initial)))



if __name__ == '__main__':
    unittest.main()
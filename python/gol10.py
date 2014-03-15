#!/usr/bin/env python
# encoding: utf-8
"""
gol10.py

Functional implementation of Conway's Game of Life that supports an infinite grid.
Uses only immutable structures - use functional style linked list

Uses a list to keep track of only those cells that are alive. Only does one pass through
all living cells and their neighbors in order to optimize performance.

Created by Mahmood Hanif on 2014-03-14.
Copyright (c) 2014 Teknifi. All rights reserved.
"""

from collections import namedtuple
from lst import Nil, cons, head, tail, is_empty, to_list
import unittest

class Cell(namedtuple('Cell', ['x', 'y'], verbose=False)):
    pass


def neighbors(cell):
    return [Cell(cell.x-xd,cell.y-yd) for xd in range(-1,2) for yd in range(-1,2) if (xd,yd) != (0,0)]

def isAlive(cell, board):
    return cell in board

def neighborsWithLivingFlag(homeCell, board):
    return [ (cell, isAlive(cell, board)) for cell in neighbors(homeCell)]

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

def updateCellCount(cells, cell, isAlive):
    if is_empty(cells):
        return cons((cell, isAlive, 1))
    else:
        (headCell, headIsAlive, headCount) = head(cells)
        if cell == headCell:
            newHead = (headCell, headIsAlive, headCount+1)
            return cons(newHead, tail(cells))
        else:
            return cons(head(cells), updateCellCount(tail(cells), cell, isAlive))

def updateCount(count, cellNbrFlag):
    cell, neighbor, neighborIsAlive = cellNbrFlag
    return updateCellCount(count, cell, True) if neighborIsAlive else updateCellCount(count, neighbor, False)

def allCellsWithCounts(livingCells):
    '''
    Return list of (cell, isAlive, count) tuples where:
        isAlive = boolean flag indicating if cell is alive
        value = count of living neighbors of cell
    '''
    cellsAndNbrs = [ (cell, nbr, isAlive) for cell in livingCells
                                          for nbr, isAlive in neighborsWithLivingFlag(cell, livingCells)]
    cellCount = Nil
    return reduce(updateCount, cellsAndNbrs, cellCount)

def nextBoard(livingCells=[]):
    return [cell for (cell, alive, count) in to_list(allCellsWithCounts(livingCells),[]) if shouldLive(count, alive)]


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
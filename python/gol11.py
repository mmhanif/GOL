#!/usr/bin/env python
# encoding: utf-8
"""
gol11.py

Alternate implementation of Conway's Game of Life that supports an infinite grid.

"""

import itertools
import time
import unittest

NEIGH_CELL = tuple(set(itertools.product((-1, 0, 1), (-1, 0, 1))) - set([(0, 0)]))
assert((0, 0) not in NEIGH_CELL)

def neighbors(cell):
    x, y = cell
    return set((x + xd, y + yd) for xd, yd in NEIGH_CELL)

def count_living(potential, living_cells):
    return len(living_cells.intersection(potential))
    
def nextBoard(living_cells):
    new_cells = set()
    potential_spawns = set()
    for cell in living_cells:
        cell_neighbors = neighbors(cell)
        if count_living(cell_neighbors, living_cells) in (2, 3):
            new_cells.add(cell)
        potential_spawns.update(cell_neighbors - living_cells)
        
    new_cells.update(
        cell for cell in potential_spawns 
        if count_living(neighbors(cell), living_cells) == 3
    )
    return new_cells

class TestGameOfLife(unittest.TestCase):
    def setUp(self):
        pass

    def shouldEqual(self, expected, received):
        s = "Expected: %s, Received: %s" % (str(expected), str(received))
        self.assertEqual(expected, received, msg=s)

    def testEmptyGrid(self):
        self.assertEqual(len(nextBoard(set())), 0)

    def testLonelyCellDies(self):
        lonely = set([(0,0)])
        self.shouldEqual(0, len(nextBoard(lonely)))

    def testCellsWithThreeNeighborsLive(self):
        initial = set([(0,0), (0,1), (1,0), (1,1)])
        self.shouldEqual(initial, nextBoard(initial))

    def testOvercrowdedCellDies(self):
        '''
                X          X X X
              X X X   ->   X . X
                X          X X X
        '''
        initial  = set([ (0,0), (0,1), (0,-1), (1,0), (-1,0) ])
        expected = set([ (1,-1), (1,0), (1,1), (0,1), (0,-1), (-1,-1), (-1,0), (-1,1)])
        self.shouldEqual(expected, nextBoard(initial))

    def testDeadCellComesToLife(self):
        '''
                X            X
              X . X   ->   . X .

        '''
        initial  = set([ (0,1), (0,-1), (1,0)])
        expected = set([ (0,0), (1,0)])
        self.shouldEqual(expected, nextBoard(initial))



if __name__ == '__main__':
    unittest.main()
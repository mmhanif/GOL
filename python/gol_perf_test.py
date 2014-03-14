#!/usr/bin/env python
# encoding: utf-8
"""
gol_perf_test.py

Created by Mahmood Hanif on 2013-09-12.
Copyright (c) 2013 Teknifi. All rights reserved.
"""

import timeit

import gol1
import gol2
import gol3
import gol4
import gol5
import gol6
import gol7
import gol8


def test(modName, gridSize, numIterations):
    setup = "import %s; g = %s.GameOfLife(%d); g.setAlive([(25,25), (24,25), (24,26), (25, 24), (26, 25)])" % (modName, modName, gridSize)
    stmt  = "g.next()"
    print modName, ": ", timeit.timeit(stmt=stmt, setup=setup, number=numIterations)

def testInfiniteGrid(modName, numIterations):
    setup = "import %s; c = %s.Cell; g = %s.GameOfLife([c(25,25), c(24,25), c(24,26), c(25, 24), c(26, 25)])" % (modName, modName, modName)
    stmt  = "g.next()"
    print modName, ": ", timeit.timeit(stmt=stmt, setup=setup, number=numIterations)

def testFunctionalGrid(modName, numIterations):
    setup = "from %s import Cell, nextBoard; c = Cell; b = [c(25,25), c(24,25), c(24,26), c(25, 24), c(26, 25)]" % modName
    stmt  = "b = nextBoard(b)"
    print modName, ": ", timeit.timeit(stmt=stmt, setup=setup, number=numIterations)

def main():
    gridSize = 500
    numIterations = 50
    #test("gol1", gridSize, numIterations)
    test("gol2", gridSize, numIterations)
    #test("gol3", gridSize, numIterations)
    #test("gol4", gridSize, numIterations)
    #test("gol5", gridSize, numIterations)
    testInfiniteGrid("gol6", numIterations)
    testInfiniteGrid("gol7", numIterations)
    testFunctionalGrid("gol8", numIterations)

if __name__ == '__main__':
    main()


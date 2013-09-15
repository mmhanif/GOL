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

def test(modName, gridSize, numIterations):
    setup = "import %s; g = %s.GameOfLife(%d); g.setAlive([(25,25), (24,25), (24,26), (25, 24), (26, 25)])" % (modName, modName, gridSize)
    stmt  = "g.next()"
    print modName, ": ", timeit.timeit(stmt=stmt, setup=setup, number=numIterations)

def main():
    gridSize = 500
    numIterations = 50
    test("gol1", gridSize, numIterations)
    test("gol2", gridSize, numIterations)
    test("gol3", gridSize, numIterations)
    test("gol4", gridSize, numIterations)
    test("gol5", gridSize, numIterations)

if __name__ == '__main__':
    main()


#!/usr/bin/env python
# encoding: utf-8
"""
gol_perf_test.py

Created by Mahmood Hanif on 2013-09-12.
Copyright (c) 2013 Teknifi. All rights reserved.
"""

import unittest

import gol1
import gol2
import gol3
import gol4
import gol5

PIMENTO = [(25,25), (24,25), (24,26), (25, 24), (26, 25)]

def iterate(mod, gridSize, numIterations):
    game = mod.GameOfLife(gridSize)
    game.setAlive(PIMENTO)
    for i in range(numIterations):
        game.next()
    return repr(game)
    
class TestGamesOfLife(unittest.TestCase):
    def setUp(self):
        pass

    def compare(self, mod1, mod2):
        gridSize = 50
        numIterations = 500
        res1 = iterate(mod1,gridSize,numIterations)
        res2 = iterate(mod2,gridSize,numIterations)
        self.assertEqual(res1, res2)
        print res1
        
    #def testGol1and2(self):
    #    self.compare(gol1,gol2)

    #def testGol2and3(self):
    #    self.compare(gol3,gol2)

    #def testGol3and4(self):
    #    self.compare(gol4,gol3)

    def testGol2and5(self):
        self.compare(gol5,gol2)

if __name__ == '__main__':
    unittest.main()


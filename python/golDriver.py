#!/usr/bin/env python
# encoding: utf-8
"""
golDriver.py

Created by Mahmood Hanif on 2013-09-10.
Copyright (c) 2013 Teknifi. All rights reserved.
"""

import sys
import os

import gol3 as gol

BAD_POINT = (-1, -1)

PIMENTO = [(25,25), (24,25), (24,26), (25,24), (26,25)]

def readPoints(gridSize):
    points = []
    while True:
        inp = raw_input("Enter point,  e.g. 1, 1 (hit X or Q to finish): ")
        if inp and inp.upper() in "XQ":
            break
        if inp and inp.upper() == "P":
            points.extend(PIMENTO)
            break
        pt = readPoint(gridSize, inp)
        if pt:
            if pt == BAD_POINT:
                continue
            else:
                points.append(pt)
        else:
            continue
    return points

def readPoint(gridSize, inp):
    try:
        p = inp.strip().split(',')
        pt = [int(elem) for elem in p]
        for elem in pt:
            if (elem < 0) or (elem >= gridSize):
                raise IndexError(elem)
        return tuple(pt[:2])
    except ValueError as error:
        print "Bad input, try again: ", error
        return BAD_POINT
    except IndexError as error:
        print "Value out of range, try again: ", error
        return BAD_POINT

def iterate(game):
    while True:
        inp = raw_input("Enter point to bring to life (e.g. 1, 1), hit any enter or space to iterate, X or Q to exit: ")
        if not inp.strip():
            game.next()
        elif inp.upper() in "XQ":
            exit()
        else:
            pt = readPoint(game.gridSize, inp)
            if pt:
                if pt == BAD_POINT:
                    continue
                else:
                    game.setAlive([pt])
            else:
                continue
        print game

def main():
    gridSize = int(raw_input("Enter grid size: "))
    game = gol.GameOfLife(gridSize)
    
    points = readPoints(gridSize)
    print "Initialized with: %s" % points
    game.setAlive(points)
    print game
    
    iterate(game)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# encoding: utf-8
"""
lst.py

Simple immutable list implementation, inspired by Scala lists,
copied from http://dbader.org/blog/functional-linked-lists-in-python

Created by Mahmood Hanif on 2014-03-14.
Copyright (c) 2014 Teknifi. All rights reserved.
"""

Nil = None

def cons(x, xs=Nil):
    return (x, xs)

def lst(*xs):
    if not xs:
        return Nil
    else:
        return cons(xs[0], lst(*xs[1:]))

def head(xs):
    return xs[0]

def tail(xs):
    return xs[1]

def is_empty(xs):
    return xs is Nil

def length(xs):
    if is_empty(xs):
        return 0
    else:
        return 1 + length(tail(xs))

def concat(xs, ys):
    if is_empty(xs):
        return ys
    else:
        return cons(head(xs), concat(tail(xs), ys))

def take(n, xs):
    if n == 0:
        return Nil
    else:
        return cons(head(xs), take(n-1, tail(xs)))

def drop(n, xs):
    if n == 0:
        return xs
    else:
        return drop(n-1, tail(xs))

'''
Following function has side-effects!

Append each element of the lst into the give Python built-in list instance
'''
def to_list(xs, aList):
    if is_empty(xs):
        return aList
    else:
        aList.append(head(xs))
        to_list(tail(xs), aList)
        return aList

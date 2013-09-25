GOL
===

Game of Life katas in various languages. Inspired by reading "Modern C++ with Test Driven Development" by Jeff Langr.

gol/python
-----------
gol<n>.py - A few different Python implementations of the Game of Life. Contain both the algorithm and test cases.
  gol1.py - Simple implementation using list of lists to describe state of grid.
  gol2.py - Just keep track of living cells
  gol3.py - Use numpy 2-D array to describe state of grid
  gol4.py - Use numpy 2-D array to describe state of grid, but use strides to determine neighbors
  gol5.py - Use numpy 2-D array to describe state of grid, but use strides to determine neighbors, 
            and only iterate over living cells.
golDriver.py - Display grid, set cells and iterate through generations
gol_comp_test.py - Compare output from different algorithms
gol_perf_test.py - Compare performance of different algorithms
performance.txt  - Performance test results. gol2 is the performance winner!


gol/cpp
-----------
C++ implementation of GOL. Uses same algorithm as python/gol2.py but implemented in C++. Performance is approximately 
5x faster than the python implementation.

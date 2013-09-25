/*------------------------------------------------
GolTest.cpp

Created by Mahmood Hanif
Copyright (c) 2013 Teknifi. All rights reserved.

Tests for GameOfLife class.
--------------------------------------------------*/

#include "gol.h"
#include "gmock/gmock.h"
#include <time.h>     

using testing::Eq;

TEST(GameOfLifeInitialization, DefaultGridHasZeroGridSize) { 
   GameOfLife game;   
   ASSERT_THAT(game.gridSize(), Eq(0));
}

TEST(GameOfLifeInitialization, DefaultGridPrintsToEmptyString) { 
   GameOfLife game;   
   std::string emptyStr;
   ASSERT_THAT(game.toString(), Eq(emptyStr));
}

TEST(GameOfLifeInitialization, InitializedGridPrintsToCorrectString) { 
   GameOfLife game (3);
   game.setAlive(Point(0,0));
   game.setAlive(Point(0,1));
   game.setAlive(Point(1,1));
   
   std::string expectedStr ("xx.\n.x.\n...\n");
   ASSERT_THAT(game.toString(), Eq(expectedStr));
}

TEST(GameOfLifeInitialization, OutOfBoundsThrows) { 
   GameOfLife game (3);   
   ASSERT_THROW(game.setAlive(Point(4,4)), OutOfBoundsException);
}

TEST(GameOfLifeLogic, CalculateNeighborsForEdgeCase) { 
   GameOfLife game (3);
   auto res = game.neighbors(Point(0,0));
   
   std::vector<Point> expected;
   expected.push_back(Point(0,1));
   expected.push_back(Point(1,0));
   expected.push_back(Point(1,1));

   ASSERT_THAT(res, Eq(expected));
}

TEST(GameOfLifeLogic, CellDiesDueToUnderpopulation) { 
   GameOfLife game (3);
   game.setAlive(Point(1,1));
   game.setAlive(Point(1,2));
   
   game.next();
   
   ASSERT_THAT(game.isAlive(Point(1,1)), Eq(false));
   ASSERT_THAT(game.isAlive(Point(1,2)), Eq(false));
}

TEST(GameOfLifeLogic, CellDiesDueToOvercrowding) { 
   GameOfLife game (3);
   game.setAlive(Point(0,0));
   game.setAlive(Point(0,1));
   game.setAlive(Point(0,2));
   game.setAlive(Point(1,0));
   game.setAlive(Point(1,2));
   
   game.next();
   
   ASSERT_THAT(game.isAlive(Point(0,1)), Eq(false));
}

TEST(GameOfLifeLogic, CellComesAliveIfExactlyThreeLivingNeighbors) { 
   GameOfLife game (3);
   game.setAlive(Point(0,0));
   game.setAlive(Point(0,1));
   game.setAlive(Point(0,2));
   
   game.next();
   
   ASSERT_THAT(game.isAlive(Point(1,1)), Eq(true));
}

float _runtime(int gridSize, int numIters) {
   GameOfLife game (gridSize);
   game.setAlive(Point(25,25));
   game.setAlive(Point(24,25));
   game.setAlive(Point(24,26));
   game.setAlive(Point(25,24));
   game.setAlive(Point(26,25));

   clock_t t1 = clock();

   for (int i=0; i<numIters; i++) {
       game.next();
   }
   
   clock_t t2 = clock();
   return ((float)(t2-t1))/CLOCKS_PER_SEC;    
}

TEST(GameOfLifePerformance, 50x50x500) { 
   int gridSize = 50;
   int numIters = 500;
   float runtime = _runtime(gridSize, numIters);
   
   std::cout << " Game Of Life: Grid size = " << gridSize << ", Iterations = " << numIters << ", time = " << runtime << "\n";
}

TEST(GameOfLifePerformance, 500x500x50) { 
   int gridSize = 500;
   int numIters = 50;
   float runtime = _runtime(gridSize, numIters);
   
   std::cout << " Game Of Life: Grid size = " << gridSize << ", Iterations = " << numIters << ", time = " << runtime << "\n";
}



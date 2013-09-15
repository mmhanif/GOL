#include <string>
#include <unordered_map>

class GameOfLife {
public:
    unsigned int gridSize(void) const {
        return 0;
    }
    
   std::string encodedDigit(char letter) const {
      const std::unordered_map<char,std::string> encodings {
         {'b', "1"},
         {'c', "2"},
         {'d', "3"}
      };
      return encodings.find(letter)->second;
   }    
    
};

#include "gmock/gmock.h"    

using testing::Eq;

TEST(GameOfLifeInitialization, DefaultGridHasZeroGridSize) { 
   GameOfLife game;   
   ASSERT_THAT(game.gridSize(), Eq(0));
}


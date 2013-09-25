/*------------------------------------------------
gol.h

Created by Mahmood Hanif on 2013-09-18.
Copyright (c) 2013 Teknifi. All rights reserved.

Simple-ish implementation of Conway's Game of Life. 
Allocates a list of lists to represent the game grid.

See tests in GolTest.cpp
--------------------------------------------------*/

#include <string>
#include <vector>
#include <algorithm>    // std::find, std::max, std::min
#include <exception>    // std::exception
#include <sstream>      // std::ostringstream
#include <iostream>     // std::cout
#include <utility>      // std::pair
#include <map>          // std::map

class Point {
public:
    Point (int x, int y) : x (x), y (y) {}
    
    int x;
    int y;
};

inline std::ostream &operator<<(std::ostream &os, const Point &pt) { 
    return os << "(" << pt.x << "," << pt.y << ")";
}

inline bool operator==(const Point& lhs, const Point& rhs) {
    return (lhs.x == rhs.x) && (lhs.y == rhs.y);
    }

inline bool operator<(const Point& lhs, const Point& rhs) {
    if (lhs.x < rhs.x) {
        return true;
    }
    else if (lhs.x == rhs.x) {
        return (lhs.y < rhs.y);
    }
    else return false;
}

class OutOfBoundsException : public std::exception {
public:
    OutOfBoundsException (const Point& pt, int gridSize) {
        std::ostringstream oss;
        oss << "(" << pt.x << "," << pt.y << ") out of bounds for grid size "<< gridSize;
        msg = oss.str();
    }
    
    std::string msg;
};

const char ALIVE_SYM {'x'};
const char DEAD_SYM  {'.'};    

class GameOfLife {
public:
    GameOfLife (int gridSize = 0):
        _gridSize (gridSize) {
    }
    
    int gridSize(void) const {
        return _gridSize;
    }

    void setAlive(const Point& pt) {
        if (isInBounds(pt))
            _livingPoints.push_back(pt);
        else
            throw OutOfBoundsException(pt, _gridSize);
    }

    void setDead(const Point& pt) {
        if (isInBounds(pt)) {
            auto position = std::find(_livingPoints.begin(), _livingPoints.end(), pt);
            if (position != _livingPoints.end()) {
                _livingPoints.erase(position);
            }
        }
        else
            throw OutOfBoundsException(pt, _gridSize);
    }

    bool isAlive(const Point& pt) const {
        if (std::find(_livingPoints.begin(), _livingPoints.end(), pt) != _livingPoints.end())
            return true;
        else
            return false;
    }

    bool isInBounds(const Point& pt) const {
        return (pt.x < _gridSize) && (pt.y < _gridSize);
    }

    std::vector<Point> neighbors(const Point& pt) const {
        std::vector<Point> neighbors;
        auto xminus1 = std::max(0, pt.x - 1);
        auto yminus1 = std::max(0, pt.y - 1);
        auto xplus1  = std::min(pt.x+1, _gridSize-1);
        auto yplus1  = std::min(pt.y+1, _gridSize-1);
        for (int nx = xminus1; nx <= xplus1; nx++) {
            for (int ny = yminus1; ny <= yplus1; ny++) {
                if ((pt.x != nx) or (pt.y != ny)) {
                    Point neighbor(nx, ny);
                    neighbors.push_back(neighbor);
                }
            }
        }
        return neighbors;
    }

    int numLivingNeighbors(const Point& pt, const std::vector<Point>& ptNeighbors) const {
        return numNeighbors(pt, ptNeighbors).first;
    }

    std::pair<int,int> numNeighbors(const Point& pt, const std::vector<Point>& ptNeighbors) const {
        int numAlive {0};
        int numDead  {0};
        for (auto it = ptNeighbors.begin(); it != ptNeighbors.end(); ++it) {
            if (isAlive(*it)) { 
                numAlive += 1;
            }
            else {
                numDead += 1;
            }
        }
        return std::pair<int, int> (numAlive, numDead);
    }

    bool isOverCrowdedOrUnderPopulated(const Point& cell, const std::vector<Point>& neighbors) {
        auto neighborCount = numLivingNeighbors(cell, neighbors);
        return ((neighborCount < 2) || (neighborCount > 3));
    }

    void update_dead_neighbors_with_living_neighbor_count(const std::vector<Point>& neighbors, std::map<Point, int>& deadNeighbors) {
        for (auto neighbor_it = neighbors.begin(); neighbor_it != neighbors.end(); ++neighbor_it) {
            if (isAlive(*neighbor_it) == false) {
                deadNeighbors.insert(std::make_pair<Point, int> (*neighbor_it, 0));
                deadNeighbors[*neighbor_it] = deadNeighbors[*neighbor_it] + 1;
            }
        }        
    }

    void process_cell(const Point& cell, std::vector<Point>& toDead, std::map<Point, int>& deadNeighbors) {
        auto allNeighbors = neighbors(cell);
        if (isOverCrowdedOrUnderPopulated(cell, allNeighbors)) {
            toDead.push_back(cell);
        }
        
        update_dead_neighbors_with_living_neighbor_count(allNeighbors, deadNeighbors);
    }

    void next(void) {
        std::vector<Point> toDead;
        std::map<Point, int> deadNeighbors;
        for (auto it = _livingPoints.begin(); it != _livingPoints.end(); ++it) {
            process_cell(*it, toDead, deadNeighbors);
        }
        
        for (auto it = toDead.begin(); it != toDead.end(); ++it) {
            setDead(*it);
        }

        for (auto map_it = deadNeighbors.begin(); map_it != deadNeighbors.end(); ++map_it) {
            if (map_it->second == 3)
                setAlive(map_it->first);
        }

    }

    std::string toString(void) const {
        std::string str;
        for (int i=0; i < _gridSize; i++) {
            for (int j=0; j < _gridSize; j++) {
                Point pt (i,j);
                if (isAlive(pt))
                    str += ALIVE_SYM;
                else 
                    str += DEAD_SYM;
            }
            str += '\n';
        }
        return str;
    }
    
private:
    int                _gridSize;
    std::vector<Point> _livingPoints;
};

#pragma once

#include "../runner.h"

using Grid = std::vector<std::string>;

class Day18Part2 : Runner {
public:
    virtual void run(std::string inputFile);

private:
    Grid stepGrid(Grid in);
    char stepLight(Grid in, int x, int y);
    char stateAt(Grid in, int x, int y);
    void printGrid(Grid grid);
};

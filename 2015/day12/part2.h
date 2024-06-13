#pragma once

#include <vector>

#include "../runner.h"

class Day12Part2 : Runner {
public:
    virtual void run(std::string inputFile);

private:
    int totalRecursive(json jsonObj);
};

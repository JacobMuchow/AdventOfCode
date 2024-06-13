#pragma once

#include <vector>

#include "../runner.h"

class Day13Part2 : Runner {
public:
    virtual void run(std::string inputFile);

private:
    std::string edgeKey(std::string p1, std::string p2);
};

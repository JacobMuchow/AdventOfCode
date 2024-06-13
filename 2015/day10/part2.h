#pragma once

#include <vector>

#include "../runner.h"

class Day10Part2 : Runner {
public:
    virtual void run(std::string inputFile);

private:
    std::string lookAndSay(std::string line);
};

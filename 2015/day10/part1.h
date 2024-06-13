#pragma once

#include <vector>

#include "../runner.h"

class Day10Part1 : Runner {
public:
    virtual void run(std::string inputFile);

private:
    std::string lookAndSay(std::string line);
};

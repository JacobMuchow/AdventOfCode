#pragma once

#include "../runner.h"

class Day17Part1 : Runner {
public:
    virtual void run(std::string inputFile);

private:
    int variations(const int desired);
    int variationsRecursive(int i, int total, const int desired);

private:
    std::vector<int> containers = {};
};

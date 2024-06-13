#pragma once

#include "../runner.h"

class Day20Part2 : Runner {
private:
    std::vector<int> computeFactors(int number);
    int sumFactors(int num);
    int findLower(int goal);
    int findUpper(int goal, int lower);
    int searchLowest(int lower, int upper, int goal, int precision);

public:
    virtual void run(std::string inputFile);
};

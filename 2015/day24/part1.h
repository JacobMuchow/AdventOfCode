#pragma once

#include "../runner.h"

class Day24Part1 : Runner {
private:
    std::vector<int> boxes;

private:
    void findCombosRecursive(std::vector<int> &boxes, int targetWeight, int index, std::vector<std::vector<int>> &allCombos, std::vector<int> &combo);
    std::vector<std::vector<int>> findCombinations(std::vector<int> &boxes, int targetWeight);

public:
    virtual void run(std::string inputFile);
};

#pragma once

#include <vector>

#include "../runner.h"

struct Reindeer {
    std::string name;
    int velocity;
    int flyTime;
    int restTime;
};

class Day14Part1 : Runner {
public:
    virtual void run(std::string inputFile);

private:
    int calculateDistance(Reindeer deer, int time);
};

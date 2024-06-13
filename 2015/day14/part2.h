#pragma once

#include <vector>

#include "../runner.h"

struct Reindeer {
    std::string name;
    int velocity;
    int flyTime;
    int restTime;

    int points = 0;
    int distance = 0;
    int isResting = false;
    int cooldown = 0;

    Reindeer(std::string name, int velocity, int flyTime, int restTime) {
        this->name = name;
        this->velocity = velocity;
        this->flyTime = flyTime;
        this->restTime = restTime;
        this->cooldown = flyTime;
        this->distance = 0;
    }
};

class Day14Part2 : Runner {
public:
    virtual void run(std::string inputFile);

private:
    void advance(std::shared_ptr<Reindeer> deer);
};

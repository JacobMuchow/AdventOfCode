#pragma once

#include <vector>

#include "../runner.h"

struct Ingredient {
    std::string name;
    int capacity;
    int durability;
    int flavor;
    int texture;
    int calories;

    Ingredient(std::string name, int capacity, int durability, int flavor, int texture, int calories) {
        this->name = name;
        this->capacity = capacity;
        this->durability = durability;
        this->flavor = flavor;
        this->texture = texture;
        this->calories = calories;
    }
};

class Day15Part1 : Runner {
public:
    virtual void run(std::string inputFile);

private:
    long long getScore(std::vector<int> dist);
    long long findBestScoreRecursive(std::vector<int> dist, int idx, int tspAvailable, long long bestScore);

private:
    std::vector<std::shared_ptr<Ingredient>> ingredients = {};
};

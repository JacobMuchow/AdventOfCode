#pragma once

#include <vector>
#include <unordered_map>

#include "../runner.h"

struct Sue {
    std::string name;
    std::unordered_map<std::string, int> props;

    Sue(std::string name, std::unordered_map<std::string, int> props) {
        this->name = name;
        this->props = props;
    }
};

class Day16Part1 : Runner {
public:
    virtual void run(std::string inputFile);
};

#pragma once

#include "../runner.h"

class Day19Part2 : Runner {
private:
    std::vector<std::pair<std::string, std::string>> replacements = {};

public:
    virtual void run(std::string inputFile);
};

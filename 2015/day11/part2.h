#pragma once

#include <vector>

#include "../runner.h"

class Day11Part2 : Runner {
public:
    virtual void run(std::string inputFile);

private:
    std::string nextPassword(std::string password);
    std::string incrementAt(std::string, int pos);
    int passwordValid(std::string password);
    bool invalidChar(char val);
};

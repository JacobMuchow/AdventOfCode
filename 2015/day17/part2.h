#pragma once

#include "../runner.h"

struct Results {
    int min = INT_MAX;
    int numVariants = 0;
};

class Day17Part2 : Runner {
public:
    virtual void run(std::string inputFile);

private:
    Results minContainers(const int spaceDesired);
    void minContainersRecursive(int i, int count, int spaceTotal, const int spaceDesired, std::shared_ptr<Results>);

private:
    std::vector<int> containers = {};
};

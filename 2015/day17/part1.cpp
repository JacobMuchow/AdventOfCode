#include "part1.h"

#include <regex>
#include <unordered_map>

using namespace std;

int Day17Part1::variations(const int desired) {
    int variations = 0;
    for (int i = 0; i < containers.size(); i++) {
        variations += variationsRecursive(i, 0, desired);
    }

    return variations;
}

int Day17Part1::variationsRecursive(int i, int total, const int desired) {
    if (i >= containers.size()) {
        return 0;
    }

    total += containers[i];

    if (total > desired) {
        return 0;
    } else if (total == desired) {
        return 1;
    }

    int variations = 0;
    for (int j = i+1; j < containers.size(); j++) {
        variations += variationsRecursive(j, total, desired);
    }

    return variations;
}

void Day17Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    for (string& line : lines) {
        containers.push_back(stoi(line));
    }

    int numVariations = variations(150);

    cout << "Total variations: " << numVariations << endl;
}

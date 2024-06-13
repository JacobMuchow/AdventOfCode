#include "part2.h"

#include <regex>
#include <unordered_map>

using namespace std;

Results Day17Part2::minContainers(const int spaceDesired) {
    auto results = make_shared<Results>();

    int variations = 0;
    for (int i = 0; i < containers.size(); i++) {
        minContainersRecursive(i, 0, 0, spaceDesired, results);
    }

    return *results;
}

void Day17Part2::minContainersRecursive(int i, int count, int spaceTotal, const int spaceDesired, shared_ptr<Results> results) {
    if (i >= containers.size()) {
        return;
    }

    spaceTotal += containers[i];
    count += 1;

    if (spaceTotal > spaceDesired || count > results->min) {
        return;
    } else if (spaceTotal == spaceDesired) {
        if (count == results->min) {
            results->numVariants++;
        } else {
            results->min = count;
            results->numVariants = 1;
        }
        return;
    }

    for (int j = i+1; j < containers.size(); j++) {
        minContainersRecursive(j, count, spaceTotal, spaceDesired, results);
    }
}

void Day17Part2::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    for (string& line : lines) {
        containers.push_back(stoi(line));
    }

    Results results = minContainers(150);

    cout << "Min number: " << results.min << ", variants: " << results.numVariants << endl;
}

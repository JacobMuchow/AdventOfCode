#include "part2.h"

using namespace std;

int calcRequiredRibbon(vector<int> dims) {
    int lwPerim = dims[0]*2 + dims[1]*2;
    int whPerim = dims[1]*2 + dims[2]*2;
    int lhPerim = dims[0]*2 + dims[2]*2;
    int smallest = min(lwPerim, min(whPerim, lhPerim));

    int volume = dims[0] * dims[1] * dims[2];

    return smallest + volume;
}

void Day02Part2::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    long totalLength = 0;

    for (string line : lines) {
        auto dimsRaw = split(line, "x");
        vector<int> dims;
        dims.reserve(dimsRaw.size());
        for (string dimRaw : dimsRaw) { dims.push_back(stoi(dimRaw)); }

        int required = calcRequiredRibbon(dims);
        totalLength += required;
        cout << "Length required: " << required << endl;
    }

    cout << endl << "Total length required: " << totalLength << endl;
}

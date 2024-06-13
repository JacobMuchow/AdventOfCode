#include "part1.h"

using namespace std;

int calcRequiredPaper(vector<int> dims) {
    int lwArea = dims[0] * dims[1];
    int whArea = dims[1] * dims[2];
    int lhArea = dims[0] * dims[2];
    int smallest = min(lwArea, min(whArea, lhArea));

    return lwArea*2 + whArea*2 + lhArea*2 + smallest;
}

void Day02Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    long totalArea = 0;

    for (string line : lines) {
        auto dimsRaw = split(line, "x");
        vector<int> dims;
        dims.reserve(dimsRaw.size());
        for (string dimRaw : dimsRaw) { dims.push_back(stoi(dimRaw)); }

        int required = calcRequiredPaper(dims);
        totalArea += required;
        cout << "Area required: " << required << endl;
    }

    cout << endl << "Total area required: " << totalArea << endl;
}

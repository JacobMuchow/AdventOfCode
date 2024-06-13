#include "part1.h"

#include <regex>

using namespace std;

void Day12Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    string line = lines[0];
    cout << line << endl;

    regex re("([-]?[0-9]+)");
    auto iterBegin = sregex_iterator(line.begin(), line.end(), re);
    auto iterEnd = sregex_iterator();

    int numTotal = 0;

    for (auto iter = iterBegin; iter != iterEnd; iter++) {
        smatch sm = *iter;
        numTotal += stoi(sm.str());
    }

    cout << "num total: " << numTotal << endl;
}

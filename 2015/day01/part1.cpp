#include "part1.h"

#include <vector>

using namespace std;

void Day01Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    // Only 1 line in this one.
    auto line = lines[0];

    int floor = 0;

    for (char c : line) {
        if (c == '(') {
            floor++;
        } else if (c == ')') {
            floor--;
        }
    }

    cout << "Final floor: " << floor << endl;
}

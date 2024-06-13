#include "part2.h"

#include <vector>

using namespace std;

void Day01Part2::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    // Only 1 line in this one.
    auto line = lines[0];

    int floor = 0;
    int pos = 1;

    for (char c : line) {
        if (c == '(') {
            floor++;
        } else if (c == ')') {
            floor--;
        }

        if (floor == -1) {
            break;
        }

        pos++;
    }

    cout << "Santa enters floor -1 at pos: " << pos << endl;
}

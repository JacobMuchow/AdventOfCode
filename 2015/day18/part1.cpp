#include "part1.h"

#include <regex>
#include <unordered_map>

using namespace std;

char Day18Part1::stateAt(Grid grid, int x, int y) {
    // Out-of-bounds points are effectively "off".
    if (x < 0 || x >= grid[0].length() || y < 0 || y >= grid.size()) {
        return '.';
    }

    return grid[y][x];
}

char Day18Part1::stepLight(vector<string> in, int x, int y) {
    bool isOn = stateAt(in, x, y) == '#';
    int onNeighbors = 0;

    onNeighbors += stateAt(in, x-1, y-1) == '#' ? 1 : 0;
    onNeighbors += stateAt(in, x,   y-1) == '#' ? 1 : 0;
    onNeighbors += stateAt(in, x+1, y-1) == '#' ? 1 : 0;
    onNeighbors += stateAt(in, x-1, y)   == '#' ? 1 : 0;
    onNeighbors += stateAt(in, x+1, y)   == '#' ? 1 : 0;
    onNeighbors += stateAt(in, x-1, y+1) == '#' ? 1 : 0;
    onNeighbors += stateAt(in, x,   y+1) == '#' ? 1 : 0;
    onNeighbors += stateAt(in, x+1, y+1) == '#' ? 1 : 0;

    return isOn
        ? onNeighbors == 2 || onNeighbors == 3 ? '#' : '.'
        : onNeighbors == 3 ? '#' : '.';
}

vector<string> Day18Part1::stepGrid(vector<string> in) {
    vector<string> out(in);

    for (int y = 0; y < in.size(); y++) {
        for (int x = 0; x < in[y].length(); x++) {
            out[y][x] = stepLight(in, x, y);
        }
    }

    return out;
}

void Day18Part1::run(std::string inputFile) {
    Grid grid = readLinesFromFile(inputFile);

    for (int i = 0; i < 100; i++) {
        cout << "Step " << i << endl;
        grid = stepGrid(grid);
    }

    int numLightsOn = 0;
    for (int y = 0; y < grid.size(); y++) {
        for (int x = 0; x < grid[y].length(); x++) {
            numLightsOn += stateAt(grid, x, y) == '#' ? 1 : 0;
        }
    }

    cout << "Num lights left on: " << numLightsOn << endl;
}

void Day18Part1::printGrid(Grid grid) {
    for (string& line : grid) {
        cout << line << endl;
    }
    cout << endl;
}

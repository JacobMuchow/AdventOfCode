#include "part2.h"

#include <regex>

#include "../elements/pos2d.h"

using namespace std;

void Day06Part2::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);
    string line = lines[0];

    regex e("^(turn on|turn off|toggle) ([0-9]+),([0-9]+) through ([0-9]+),([0-9]+)");
    int grid[1000][1000] = { 0 };

    for (string line : lines) {
        smatch sm;
        bool hasMatch = regex_match(line, sm, e);
        if (!hasMatch) {
            throw runtime_error("Failed to match line: " + line);
        }

        string command = sm[1];
        Pos2D p1 { stoi(sm[2]), stoi(sm[3]) };
        Pos2D p2 { stoi(sm[4]), stoi(sm[5]) };

        cout << command << " " << p1.key() << " - " << p2.key() << endl;

        int minX = min(p1.x, p2.x);
        int maxX = max(p1.x, p2.x);
        int minY = min(p1.y, p2.y);
        int maxY = max(p1.y, p2.y);

        for (int y = minY; y <= maxY; y++) {
            for (int x = minX; x <= maxX; x++) {
                if (command == "turn on") {
                    grid[y][x] += 1;
                } else if (command == "turn off") {
                    grid[y][x] = max(grid[y][x]-1, 0);
                } else if (command == "toggle") {
                    grid[y][x] += 2;
                } else {
                    throw runtime_error("Unrecognized command: " + command);
                }
            }
        }
    }

    int totalBrightness = 0;

    for (int y = 0; y < 1000; y++) {
        for (int x = 0; x < 1000; x++) {
            totalBrightness += grid[y][x];
        }
    }

    cout << "Total brightness: " << totalBrightness << endl;
}

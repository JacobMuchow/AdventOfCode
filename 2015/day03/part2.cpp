#include "part2.h"

#include "../elements/pos2d.h"

using namespace std;

void Day03Part2::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    // Only 1 line for this one.
    auto line = lines[0];

    Pos2D posA { 0, 0 }, posB { 0, 0 };
    unordered_map<string, bool> visited {
        { posA.key(), true }
    };

    for (int i = 0; i < line.length(); i++) {
        char c = line[i];

        auto pos = i % 2 == 0 ? &posA : &posB;
        switch (c) {
        case '>': pos->x++; break;
        case '<': pos->x--; break;
        case '^': pos->y++; break;
        case 'v': pos->y--; break;
        }

        visited[pos->key()] = true;
    }

    cout << "Visited points:\n";

    for (auto iter : visited) {
        cout << iter.first << endl;
    }

    cout << "Total houses visited: " << visited.size() << endl;
}

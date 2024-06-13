#include "part1.h"

#include "../elements/pos2d.h"

using namespace std;

void Day03Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    // Only 1 line for this one.
    auto line = lines[0];

    Pos2D pos { 0, 0 };
    unordered_map<string, bool> visited {
        { pos.key(), true }
    };

     for (char c : line) {
         switch (c) {
         case '>': pos.x++; break;
         case '<': pos.x--; break;
         case '^': pos.y++; break;
         case 'v': pos.y--; break;
         }

         visited[pos.key()] = true;
     }

     cout << "Visited points:\n";

     for (auto iter : visited) {
         cout << iter.first << endl;
     }

     cout << "Total houses visited: " << visited.size() << endl;
}

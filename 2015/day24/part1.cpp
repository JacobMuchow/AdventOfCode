#include "part1.h"

using namespace std;

void Day24Part1::findCombosRecursive(vector<int> &boxes, int targetWeight, int index, vector<vector<int>> &allCombos, vector<int> &combo) {
    if (index >= boxes.size()) {
        return;
    }

    for (int i = index; i < boxes.size(); i++) {
        int box = boxes[i];

        if (box > targetWeight) continue;

        if (box == targetWeight) {
            combo.push_back(box);
            allCombos.push_back(vector(combo));
            combo.pop_back();
        } else {
            combo.push_back(box);
            findCombosRecursive(boxes, targetWeight - box, i+1, allCombos, combo);
            combo.pop_back();
        }
    }
}

vector<vector<int>> Day24Part1::findCombinations(vector<int> &boxes, int targetWeight) {
    vector<vector<int>> allCombos = {};
    vector<int> combo = {};

    findCombosRecursive(boxes, targetWeight, 0, allCombos, combo);

    return allCombos;
}

void Day24Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    // Parse box sizes and sort greatest -> smallest
    for (auto& line : lines) {
        boxes.insert(boxes.begin(), stoi(line));
    }
    sort(boxes.begin(), boxes.end(), [](int a, int b) {
        return a > b;
    });

    int totalWeight = 0;
    cout << "Boxes:" << endl;
    for (auto box : boxes) {
        totalWeight += box;
        cout << box << endl;
    }

    int targetWeight = totalWeight / 3;
    cout << "Total weight: " << totalWeight << endl;
    cout << "Target weight: " << targetWeight << endl;

    // Find all combinations from list that can add up to the target weight.
    cout << "\nComputing combinations to fill " << targetWeight << "...\n";
    auto combinations = findCombinations(boxes, targetWeight);
    cout << endl << "Combinations: " << combinations.size() << endl;

    // Sort by # in group.
    cout << "Sorting by size...\n";
    sort(combinations.begin(), combinations.end(), [](auto& a, auto &b) {
        return a.size() < b.size();
    });


    int frontSize = -1;
    long long bestEntanglement = LONG_LONG_MAX;

    for (int i = 0; i < combinations.size(); i++) {
        auto& combo = combinations[i];

        if (frontSize > 0 && combo.size() > frontSize) {
            break;
        }

        auto subset = vector(boxes);
        for (auto box : combo) {
            subset.erase(remove(subset.begin(), subset.end(), box));
        }

        auto subsetCombos = findCombinations(subset, targetWeight);
        if (subsetCombos.size() > 0) {
            frontSize = combo.size();

            long long entanglement = 1;
            for (auto val : combo) {
                entanglement *= (long long) val;
            }

            bestEntanglement = min(bestEntanglement, entanglement);
        }
    }

    cout << "Best entanglement: " << bestEntanglement << endl;
}

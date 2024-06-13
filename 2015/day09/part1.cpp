#include "part1.h"

#include <regex>
#include <set>

using namespace std;

void Day09Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    set<string> placeSet = {};
    unordered_map<string, int> edges = {};

    for (string line : lines) {
        smatch sm;
        bool hasMatch = regex_match(line, sm, regex("^(.*) to (.*) = ([0-9]+)"));
        if (!hasMatch) {
            throw invalid_argument("Failed to parse line from input: " + line);
        }

        string place1 = sm[1];
        string place2 = sm[2];
        int dist = stoi(sm[3]);

        placeSet.insert(place1);
        placeSet.insert(place2);
        edges[edgeKey(place1, place2)] = dist;
        edges[edgeKey(place2, place1)] = dist;

        cout << place1 << " -> " << place2 << " (" << dist << ")" << endl;
    }

    // Created ordered list of places so we can use next_permutation std iter function.
    vector<string> places(placeSet.begin(), placeSet.end());
    std::sort(places.begin(), places.end());

    // Calculate total for each permutation and track shortest.
    int shortest = INT_MAX;
    do {
        int total = 0;
        for (int i = 0; i < places.size()-1; i++) {
            total += edges[edgeKey(places[i], places[i+1])];
        }

        shortest = min(total, shortest);

    } while(next_permutation(places.begin(), places.end()));

    cout << "\nShortest path: " << shortest << endl;
}

std::string Day09Part1::edgeKey(std::string p1, std::string p2) {
    return p1 + "|" + p2;
}

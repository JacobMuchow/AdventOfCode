#include "part1.h"

#include <regex>
#include <set>

using namespace std;

void Day14Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    vector<Reindeer> reindeers = {};

    for (string& line : lines) {
        smatch sm;
        bool hasMatch = regex_match(line, sm, regex("^([A-Za-z]+) can fly ([0-9]+) km/s for ([0-9]+) seconds, but then must rest for ([0-9]+) seconds."));
        if (!hasMatch) {
            throw invalid_argument("Failed to parse info from line: " + line);
        }

        Reindeer deer { sm[1], stoi(sm[2]), stoi(sm[3]), stoi(sm[4]) };
        reindeers.push_back(deer);

        cout << deer.name << ": " << deer.velocity << " km/s, " << deer.flyTime << "s, rest " << deer.restTime << "s" << endl;
    }

    int longest = 0;
    for (auto& deer : reindeers) {
        int dist = calculateDistance(deer, 2503);
        cout << deer.name << " travels " << dist << " km" << endl;
        longest = max(dist, longest);
    }

    cout << "Longest: " << longest << endl;
}

int Day14Part1::calculateDistance(Reindeer deer, int time) {
    int fullLength = deer.flyTime + deer.restTime;
    int numFullLengths = time / fullLength;
    int timeRemaining = time % fullLength;

    int firstStretch = numFullLengths * deer.flyTime * deer.velocity;
    int lastStretch = min(timeRemaining, deer.flyTime) * deer.velocity;

    return firstStretch + lastStretch;
}

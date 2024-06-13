#include "part2.h"

#include <regex>
#include <set>

using namespace std;

void Day14Part2::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    vector<shared_ptr<Reindeer>> reindeers = {};

    for (string& line : lines) {
        smatch sm;
        bool hasMatch = regex_match(line, sm, regex("^([A-Za-z]+) can fly ([0-9]+) km/s for ([0-9]+) seconds, but then must rest for ([0-9]+) seconds."));
        if (!hasMatch) {
            throw invalid_argument("Failed to parse info from line: " + line);
        }
        reindeers.push_back(make_shared<Reindeer>(sm[1], stoi(sm[2]), stoi(sm[3]), stoi(sm[4])));
    }

    for (int time = 0; time < 2503; time++) {
        // Advance each deer 1 clock tick
        for (auto& deer : reindeers) {
            advance(deer);
        }

        // Determine what is leading distance...
        int leadDist = 0;
        for (auto& deer : reindeers) {
            leadDist = max(leadDist, deer->distance);
        }

        // Award 1 points to each deer in lead.
        for (auto& deer : reindeers) {
            if (deer->distance == leadDist) {
                deer->points++;
            }
        }
    }

    int mostPoints = 0;
    for (auto& deer : reindeers) {
        cout << deer->name << " has " << deer->points << " points." << endl;
        mostPoints = max(deer->points, mostPoints);
    }

    cout << "Most points: " << mostPoints << endl;
}

void Day14Part2::advance(shared_ptr<Reindeer> deer) {
    if (deer->cooldown == 0) {
        deer->isResting = !deer->isResting;
        deer->cooldown = deer->isResting ? deer->restTime : deer->flyTime;
    }

    if (!deer->isResting) {
        deer->distance += deer->velocity;
    }

    deer->cooldown--;
}

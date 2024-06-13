#include "part2.h"

#include <regex>
#include <set>

using namespace std;

void Day13Part2::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    set<string> peopleSet = {};
    unordered_map<string, int> edges = {};

    for (string& line : lines) {
        smatch sm;
        bool hasMatch = regex_match(line, sm, regex("^(.*) would (gain|lose) ([0-9]+) happiness units by sitting next to (.*)."));
        if (!hasMatch) {
            throw invalid_argument("Failed to parse line from input: " + line);
        }

        string p1 = sm[1];
        string effect = sm[2];
        int value = stoi(sm[3]);
        string p2 = sm[4];

        if (effect == "lose") {
            value *= -1;
        }

        peopleSet.insert(p1);
        peopleSet.insert(p2);
        edges[edgeKey(p1, p2)] = value;
    }

    // Add yourself with edge values 0 to everyone.
    // This is the only difference from pt 1 solution.
    peopleSet.insert("Myself");
    for (auto& p : peopleSet) {
        edges[edgeKey(p, "Myself")] = 0;
        edges[edgeKey("Myself", p)] = 0;
    }

    // Created ordered list of places so we can use next_permutation std iter function.
    vector<string> people(peopleSet.begin(), peopleSet.end());
    std::sort(people.begin(), people.end());

    // Calculate total for each permutation and track shortest.
    int optimalHappiness = 0;
    do {
        // Emplace first person in back to complete circular arrangement.
        // This will make for an easy totalling for loop.
        vector<string> arrangement(people);
        arrangement.push_back(arrangement.front());

        int total = 0;
        for (int i = 0; i < arrangement.size()-1; i++) {
            total += edges[edgeKey(arrangement[i], arrangement[i+1])];
            total += edges[edgeKey(arrangement[i+1], arrangement[i])];
        }

        optimalHappiness = max(total, optimalHappiness);

    } while(next_permutation(people.begin(), people.end()));

    cout << "\nOptimal happiness: " << optimalHappiness << endl;
}

string Day13Part2::edgeKey(string p1, string p2) {
    return p1 + "," + p2;
}

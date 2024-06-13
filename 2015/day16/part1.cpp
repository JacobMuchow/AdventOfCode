#include "part1.h"

#include <regex>
#include <unordered_map>

using namespace std;

void Day16Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    vector<shared_ptr<Sue>> sues = {};

    for (string& line : lines) {
        smatch sm;
        bool hasMatch = regex_match(line, sm, regex("^(.*?): (.*)"));
        if (!hasMatch) {
            throw invalid_argument("Unable to parse line: " + line);
        }

        string name = sm[1];
        line = sm[2];

        regex re("([a-z]+): ([0-9]+)");
        auto iterBegin = sregex_iterator(line.begin(), line.end(), re);
        auto iterEnd = sregex_iterator();

        unordered_map<string, int> props = {};

        for (auto it = iterBegin; it != iterEnd; it++) {
            smatch sm = *it;
            props[sm[1]] = stoi(sm[2]);
        }

        sues.push_back(make_shared<Sue>(name, props));
    }

    unordered_map<string, int> analysis = {
        { "children", 3 },
        { "cats", 7 },
        { "samoyeds", 2 },
        { "pomeranians", 3 },
        { "akitas", 0 },
        { "vizslas", 0 },
        { "goldfish", 5 },
        { "trees", 3 },
        { "cars", 2 },
        { "perfumes", 1 }
    };

    for (auto& sue : sues) {
        bool validSue = true;

        for (auto& entry : sue->props) {
            auto found = analysis.find(entry.first);
            if (found == analysis.end()) {
                throw invalid_argument("Could not find key in analysis: " + entry.first);
            }

            if (entry.second != analysis[entry.first]) {
                validSue = false;
                break;
            }
        }

        if (validSue) {
            cout << "Sue found! ~ " << sue->name << endl;
            break;
        }
    }
}

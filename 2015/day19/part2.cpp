#include "part2.h"

#include <regex>
#include <queue>

using namespace std;

void Day19Part2::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    for (string& line : lines) {
        if (line.empty()) break;

        smatch sm;
        bool hasMatch = regex_match(line, sm, regex("^(.*) => (.*)"));
        if (!hasMatch) {
            throw invalid_argument("Failed to parse line from input: " + line);
        }

        replacements.push_back(pair(sm[1], sm[2]));
    }

    string molecule = lines[lines.size()-1];
    cout << molecule << endl;

    int count = 0;

    while (molecule != "e") {
        for (auto &rep : replacements) {
            size_t idx = molecule.find(rep.second);
            if (idx != string::npos) {
                molecule.replace(idx, rep.second.length(), rep.first);
                count++;
            }
        }
    }

    cout << "Steps: " << count << endl;
}

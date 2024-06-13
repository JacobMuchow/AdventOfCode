#include "part1.h"

#include <regex>
#include <set>

using namespace std;

void Day19Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    vector<pair<string, string>> replacements = {};

    for (string& line : lines) {
        if (line.empty()) break;

        smatch sm;
        bool hasMatch = regex_match(line, sm, regex("^(.*) => (.*)"));
        if (!hasMatch) {
            throw invalid_argument("Failed to parse line from input: " + line);
        }

        replacements.push_back(pair(sm[1], sm[2]));
    }

    string inputMoleculde = lines[lines.size()-1];
    set<string> variants = {};

    for (auto& rep : replacements) {
        size_t pos = 0;
        do {
            pos = inputMoleculde.find(rep.first, pos);
            if (pos == string::npos) {
                break;
            }

            string out(inputMoleculde);
            out.replace(pos, rep.first.length(), rep.second);
            variants.insert(out);

            pos++;

        } while(true);
    }

    cout << "Num variants: " << variants.size() << endl;
}

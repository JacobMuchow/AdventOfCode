#include "part2.h"

#include <regex>
#include <sstream>

using namespace std;

string encoderStr(string word) {
    stringstream ss;
    ss << '"';

    for (int i = 0; i < word.length(); i++) {
        if (word[i] == '\\') {
            ss << "\\\\";
        } else if (word[i] == '"') {
            ss << "\\\"";
        } else {
            ss << word[i];
        }
    }

    ss << '"';
    return ss.str();
}

void Day08Part2::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    int totalDiff = 0;

    for (string line : lines) {
        string encoded = encoderStr(line);

        cout << line << " -> " << encoded << endl;

        totalDiff += encoded.length() - line.length();
    }

    cout << "\ntotal diff: " << totalDiff << endl;
}

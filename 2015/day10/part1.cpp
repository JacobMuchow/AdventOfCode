#include "part1.h"

#include <sstream>

using namespace std;

void Day10Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);
    string line = lines[0];

    cout << line << endl;

    for (int i = 0; i < 40; i++) {
        line = lookAndSay(line);
    }

    cout << "\nfinal length: " << line.length() << endl;
}

std::string Day10Part1::lookAndSay(std::string line) {
    stringstream ss;

    for (int i = 0; i < line.length();) {
        char digit = line[i];

        int j = i+1;
        for (; j < line.length() && line[j] == digit; j++) {}

        int length = j-i;

        ss << length << digit;
        i = j;
    }

    return ss.str();
}

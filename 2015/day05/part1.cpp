#include "part1.h"

#include "../elements/md5.h"

using namespace std;

bool isNice2(string word) {
    int vowelCount = 0;
    int doubleCharCount = 0;

    char lastChar = '\0';

    for (char c : word) {
        if (
            c == 'a' ||
            c == 'e' ||
            c == 'i' ||
            c == 'o' ||
            c == 'u'
        ) {
            vowelCount++;
        }

        if (c == lastChar) {
            doubleCharCount++;
        }

        if (lastChar == 'a' && c == 'b') return false;
        if (lastChar == 'c' && c == 'd') return false;
        if (lastChar == 'p' && c == 'q') return false;
        if (lastChar == 'x' && c == 'y') return false;

        lastChar = c;
    }

    return vowelCount >= 3 && doubleCharCount >= 1;
}

void Day05Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    int niceWords = 0;

    for (string line : lines) {
        bool nice = isNice2(line);

        cout << line << " is " << (nice ? "nice" : "naughty") << endl;

        if (nice) {
            niceWords++;
        }
    }

    cout << "Nice word count: " << niceWords << endl;
}

#include "part1.h"

#include <regex>

using namespace std;

int numCodeCharacters(string word) {
    return word.length();
}

int numRealCharacters(string word) {
    int counter = 0;

    for (int i = 1; i < word.length()-1; i++) {
        cout << "step: " << i << endl;

        if (word[i] == '\\') {
            if (word[i+1] == '\\' || word[i+1] == '"') {
                cout << "escaped \\ or \" encountered." << endl << endl;
                counter++;
                i++;
            } else if (word[i+1] == 'x') {
                cout << "escaped ascii encountered" << endl;

                // The ascii value doesn't really matter right now, it should always be of the form "\x.."
                counter++;
                i += 3;
            } else {
                throw invalid_argument("Some invalid escape ecountered. Next char: " + to_string(word[i+1]));
            }
        } else {
            counter++;
        }
    }

    return counter;
}

void Day08Part1::run(std::string inputFile) {
    auto lines = readLinesFromFile(inputFile);

    int totalCode = 0;
    int totalReal = 0;

    for (string line : lines) {
        cout << "line: " << line << endl;

        totalCode += numCodeCharacters(line);
        totalReal += numRealCharacters(line);
    }

    cout << "\n\n";
    cout << "total code: " << totalCode << endl;
    cout << "total real: " << totalReal << endl;

    int diff = totalCode - totalReal;
    cout << "diff: " << diff << endl;
}
